import sys
try:
    import pyspark
    from pyspark.sql import SparkSession
    print(f"PySpark version: {pyspark.__version__}")
    
    spark = SparkSession.builder.master("local[*]").appName("EnvironmentCheck").getOrCreate()
    print("Spark Session created successfully.")
    print(f"Spark version: {spark.version}")
    spark.stop()
    print("Environment check passed!")
except ImportError:
    print("Error: PySpark is not installed. Please run: pip install pyspark")
except Exception as e:
    print(f"Error initializing Spark: {e}")
    print("Please ensure Java (JDK 8/11/17) is installed and JAVA_HOME is set.")
