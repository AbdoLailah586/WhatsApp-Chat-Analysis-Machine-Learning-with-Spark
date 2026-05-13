# WhatsApp Chat Analysis & Classification (Big Data with Spark)

This project is a powerful Big Data solution designed to process, analyze, and classify WhatsApp chat logs using **Apache Spark**. It leverages Spark DataFrames for large-scale data processing and Spark MLlib for machine learning classification.

## 🚀 Features
- **Scalable Data Processing**: Uses PySpark to handle massive amounts of chat data across multiple files.
- **Automated Parsing**: Regex-based parsing of standard WhatsApp export formats.
- **Deep Insights**:
  - Message frequency per category.
  - Peak activity hours analysis.
  - Top contributor identification.
- **Machine Learning**:
  - **Algorithm**: Random Forest Classifier.
  - **Feature Engineering**: TF-IDF (Term Frequency-Inverse Document Frequency).
  - **Classification**: Automatically categorizes chats into labels like *Work*, *Friends*, *Studying*, etc.

## 🛠️ Requirements
- Python 3.8+
- [Apache Spark](https://spark.apache.org/downloads.html) (with Java 8/11/17)
- PySpark (`pip install pyspark`)

## 📂 Project Structure
```text
├── dataset/               # Organized chat files (.txt)
│   ├── work/              # Professional/Important chats
│   ├── friends/           # Personal/Semi-important chats
│   └── studying/          # Academic chats
├── spark_processor.py      # Main PySpark processing & ML script
├── check_spark.py         # Environment verification script
└── README.md              # Project documentation
```

## 📖 How to Use

### 1. Prepare Your Data
Export your WhatsApp chats as `.txt` files (without media) and place them in the corresponding subfolders inside the `dataset/` directory.

### 2. Verify Environment
Run the check script to ensure Spark and Java are correctly configured:
```bash
python check_spark.py
```

### 3. Run Analysis & Training
Execute the main processor to see insights and train the model:
```bash
python spark_processor.py
```

## 📊 Machine Learning Model
The project uses a **Random Forest** algorithm with a pipeline consisting of Tokenization, StopWords removal, and TF-IDF vectorization. 

- **Accuracy**: High precision achieved by learning vocabulary patterns specific to each chat category.
- **Evaluation**: Evaluated using Accuracy and F1-Score metrics.

## 📄 License
This project is for educational purposes as part of a Big Data course.
