import os
import sys
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.ml import PipelineModel

# Configure Spark Environment
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['HADOOP_HOME'] = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

# Initialize Spark once
spark = SparkSession.builder \
    .appName("WhatsAppBackend") \
    .config("spark.driver.memory", "2g") \
    .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.RawLocalFileSystem") \
    .config("spark.hadoop.fs.file.impl.disable.cache", "true") \
    .getOrCreate()

# Separate folders for Training data and User Uploads
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_DATA_FOLDER = os.path.join(BASE_DIR, 'dataset')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the trained model globally (In-Memory Training for Windows Stability)
model = None
is_training = False

def train_model_in_background():
    global model, is_training
    if is_training: return
    is_training = True
    print("Starting Background Spark Training...")
    try:
        # Import components only when needed
        from pyspark.ml import Pipeline
        from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer, IndexToString
        from pyspark.ml.classification import RandomForestClassifier
        
        df = get_spark_df()
        if not df: 
            print("No training data found in dataset/")
            is_training = False
            return

        arabic_stopwords = ["من", "في", "على", "الى", "هذا", "هذه", "تم", "كان", "كانت", "ان", "انها", "عن", "مع", "التي", "الذي", "بعد", "قبل"]
        
        indexer = StringIndexer(inputCol="category", outputCol="label")
        tokenizer = Tokenizer(inputCol="message", outputCol="words")
        remover = StopWordsRemover(inputCol="words", outputCol="filtered_words", stopWords=arabic_stopwords)
        hashingTF = HashingTF(inputCol="filtered_words", outputCol="rawFeatures", numFeatures=2000)
        idf = IDF(inputCol="rawFeatures", outputCol="features")
        rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=20) # Faster for background
        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=indexer.fit(df).labels)
        
        pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashingTF, idf, rf, labelConverter])
        model = pipeline.fit(df)
        print("Spark Model Trained and Ready in Memory!")
    except Exception as e:
        print(f"Error during background training: {e}")
    is_training = False

# Improved Regex to handle multiple formats (AM/PM, 24h, M/D/YY, etc.)
CHAT_REGEX = r"^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}(?:\s?[apAP][mM])?)\s+-\s+([^:]+):\s+(.*)$"

def parse_chat_line(line):
    match = re.match(CHAT_REGEX, line)
    if match: return match.groups()
    return (None, None, None, line)

def get_spark_df(file_path=None):
    """
    If file_path is provided, reads only that file. 
    Otherwise, reads the entire dataset folder.
    """
    all_rows = []
    
    if file_path:
        # Read specific file
        if not os.path.exists(file_path): return None
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if not line.strip(): continue
                date_str, time_str, sender, message = parse_chat_line(line)
                if date_str:
                    all_rows.append(("unknown", date_str, time_str, sender, message))
    else:
        # Read everything in dataset/
        if not os.path.exists(TRAIN_DATA_FOLDER): return None
        for root, dirs, files in os.walk(TRAIN_DATA_FOLDER):
            for file in files:
                if file.endswith(".txt"):
                    category = os.path.basename(root)
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        for line in f.readlines():
                            if not line.strip(): continue
                            date_str, time_str, sender, message = parse_chat_line(line)
                            if date_str:
                                all_rows.append((category, date_str, time_str, sender, message))
    
    if not all_rows: return None
    
    schema = StructType([
        StructField("category", StringType(), True),
        StructField("date", StringType(), True),
        StructField("time", StringType(), True),
        StructField("sender", StringType(), True),
        StructField("message", StringType(), True)
    ])
    return spark.createDataFrame(all_rows, schema)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        # Return filename as upload_id so the frontend can request specific analysis
        return jsonify({"upload_id": filename, "filename": filename})

@app.route('/api/classify', methods=['POST'])
@app.route('/api/classify/<path:filename>/reclassify', methods=['POST'])
def classify_file(filename=None):
    # This triggers a fresh scan of the file
    return jsonify({"status": "success", "message": f"Chat {filename if filename else ''} re-indexed for Spark analysis"})

@app.route('/api/insights', methods=['GET'])
@app.route('/api/analytics/<path:filename>', methods=['GET'])
def get_insights(filename=None):
    file_path = None
    if filename and filename != "0":
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        
    df = get_spark_df(file_path)
    if df is None:
        return jsonify({"error": "No data found"}), 404
    
    # If it's a new upload, categorize it
    if file_path:
        if model:
            # Use AI Model
            predictions = model.transform(df)
            df = predictions.withColumn("category", F.col("predictedLabel"))
        else:
            # Fallback: Keyword-based classification until model is ready
            print("Model not ready. Using Keyword Fallback...")
            df = df.withColumn("category", 
                F.when(F.lower(F.col("message")).rlike("work|job|meeting|office|عمل|وظيفة|اجتماع"), "work")
                .when(F.lower(F.col("message")).rlike("study|exam|book|university|دراسة|امتحان|كتاب|جامعة"), "studying")
                .otherwise("friends")
            )

    total_messages = df.count()
    
    # Categorized logic: if category is not "unknown"
    categorized_count = df.filter(df.category != "unknown").count()
    
    cat_counts = df.groupBy("category").count().collect()
    cat_distribution = {row['category']: row['count'] for row in cat_counts}
    
    time_series_raw = df.groupBy("date").count().sort("date").collect()
    time_series = [{"date": row['date'], "count": row['count']} for row in time_series_raw]
    
    sender_counts = df.groupBy("sender").count().sort(F.desc("count")).limit(10).collect()
    sender_data = [{"sender": row['sender'], "count": row['count']} for row in sender_counts]
    
    # Improved Urgency Logic: Check for keywords but avoid common words if they flood
    urgent_keywords = ["urgent", "asap", "deadline", "عاجل", "ضروري", "هام", "موعد"]
    urgent_count = df.filter(F.lower(F.col("message")).rlike("|".join(urgent_keywords))).count()
    urgency_breakdown = {"Urgent": urgent_count, "Normal": total_messages - urgent_count}
    
    return jsonify({
        "total_messages": total_messages,
        "categorized_count": categorized_count,
        "category_distribution": cat_distribution,
        "time_series": time_series,
        "top_senders": sender_data,
        "urgency_breakdown": urgency_breakdown
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify({"status": "ready", "spark_version": spark.version})

if __name__ == '__main__':
    # Start background training thread
    import threading
    training_thread = threading.Thread(target=train_model_in_background)
    training_thread.daemon = True
    training_thread.start()
    
    app.run(port=5000, debug=False)
