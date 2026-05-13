import os
import re
import sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from pyspark.ml import Pipeline
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Set environment variables for Spark workers on Windows
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# 1. Initialize Spark Session
spark = SparkSession.builder \
    .appName("WhatsAppBigDataAnalysis") \
    .config("spark.driver.memory", "4g") \
    .getOrCreate()

# 2. Define Regex for WhatsApp format: "dd/mm/yyyy, hh:mm - Sender: Message"
# This regex captures Date, Time, Sender, and the Message content.
CHAT_REGEX = r"(\d{2}/\d{2}/\d{4}), (\d{2}:\d{2}) - ([^:]+): (.+)"

def parse_chat_line(line):
    match = re.match(CHAT_REGEX, line)
    if match:
        return match.groups()
    return (None, None, None, line)

def load_and_parse_data(base_path):
    """
    Loads data from a directory structure: base_path/category/file.txt
    Uses standard Python reading to avoid Hadoop/Winutils issues on Windows.
    """
    all_rows = []
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".txt"):
                category = os.path.basename(root)
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    lines = content.split("\n")
                    for line in lines:
                        if not line.strip(): continue
                        date_str, time_str, sender, message = parse_chat_line(line)
                        if date_str:
                            all_rows.append((category, date_str, time_str, sender, message))

    # Define Schema
    schema = StructType([
        StructField("category", StringType(), True),
        StructField("date", StringType(), True),
        StructField("time", StringType(), True),
        StructField("sender", StringType(), True),
        StructField("message", StringType(), True)
    ])
    
    return spark.createDataFrame(all_rows, schema)

# 3. Feature Engineering & Aggregation
def extract_insights(df):
    print("\n--- Data Insights ---")
    
    # Message count per category
    df.groupBy("category").count().show()
    
    # Top Senders per category
    df.groupBy("category", "sender").count().sort(F.desc("count")).show(10)
    
    # Peak Hours Analysis
    df.withColumn("hour", F.split(F.col("time"), ":")[0]) \
      .groupBy("hour").count().sort("hour").show(24)

# 4. Machine Learning Pipeline
def build_ml_pipeline(df):
    # Preprocessing
    indexer = StringIndexer(inputCol="category", outputCol="label")
    tokenizer = Tokenizer(inputCol="message", outputCol="words")
    remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
    hashingTF = HashingTF(inputCol="filtered_words", outputCol="rawFeatures", numFeatures=2000)
    idf = IDF(inputCol="rawFeatures", outputCol="features")
    
    # Classifier
    rf = RandomForestClassifier(labelCol="label", featuresCol="features", numTrees=50, maxDepth=10)
    
    # Convert labels back to strings
    from pyspark.ml.feature import IndexToString
    labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=indexer.fit(df).labels)
    
    # Pipeline
    pipeline = Pipeline(stages=[indexer, tokenizer, remover, hashingTF, idf, rf, labelConverter])
    
    # Split data
    (train_data, test_data) = df.randomSplit([0.8, 0.2], seed=42)
    
    # Train model
    print("\nTraining Model... (This may take a minute with Spark)")
    model = pipeline.fit(train_data)
    
    # Predictions
    predictions = model.transform(test_data)
    
    # Evaluation
    evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
    accuracy = evaluator.evaluate(predictions)
    
    f1_evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="f1")
    f1_score = f1_evaluator.evaluate(predictions)

    print("\n" + "="*30)
    print("MODEL EVALUATION RESULTS")
    print("="*30)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"F1-Score: {f1_score:.4f}")
    print("="*30)
    
    # Show some sample predictions
    print("\nSample Predictions (Actual vs Predicted):")
    predictions.select("category", "message", "predictedLabel").show(20, truncate=50)
    
    return model

if __name__ == "__main__":
    DATASET_PATH = "dataset"
    
    if not os.path.exists(DATASET_PATH):
        print(f"Error: {DATASET_PATH} directory not found.")
        print("Please follow the instructions in implementation_plan.md to provide data.")
    else:
        df = load_and_parse_data(DATASET_PATH)
        if df.count() > 0:
            extract_insights(df)
            build_ml_pipeline(df)
        else:
            print("No data found in the dataset directory.")
