import os
import sys
import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

# Configure Spark Environment
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

app = Flask(__name__)
CORS(app)

# Initialize Spark once
spark = SparkSession.builder \
    .appName("WhatsAppBackend") \
    .config("spark.driver.memory", "2g") \
    .getOrCreate()

# Fix paths to point to the parent directory's dataset folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'dataset', 'work')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

CHAT_REGEX = r"(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}) - ([^:]+): (.+)"

def parse_chat_line(line):
    match = re.match(CHAT_REGEX, line)
    if match: return match.groups()
    return (None, None, None, line)

def get_spark_df():
    all_rows = []
    base_path = os.path.join(BASE_DIR, "dataset")
    if not os.path.exists(base_path): return None
    
    for root, dirs, files in os.walk(base_path):
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
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({"upload_id": 1, "filename": filename})

@app.route('/api/classify', methods=['POST'])
def classify_file():
    # In this Spark version, we just return success as the data is already in the dataset folder
    return jsonify({"status": "success", "message": "Chat indexed for Spark analysis"})

@app.route('/api/insights', methods=['GET'])
@app.route('/api/analytics/<int:upload_id>', methods=['GET'])
def get_insights(upload_id=None):
    df = get_spark_df()
    if df is None:
        return jsonify({"error": "No data found"}), 404
    
    total_messages = df.count()
    categorized_count = df.filter(df.category != "unknown").count()
    
    cat_counts = df.groupBy("category").count().collect()
    cat_distribution = {row['category']: row['count'] for row in cat_counts}
    
    time_series_raw = df.groupBy("date").count().sort("date").collect()
    time_series = [{"date": row['date'], "count": row['count']} for row in time_series_raw]
    
    sender_counts = df.groupBy("sender").count().sort(F.desc("count")).limit(10).collect()
    sender_data = [{"sender": row['sender'], "count": row['count']} for row in sender_counts]
    
    urgent_keywords = ["urgent", "asap", "now", "important", "deadline"]
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
    app.run(port=5000, debug=False)
