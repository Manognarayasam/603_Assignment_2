# Big Data Processing Assignment 2

## Overview
This project extracts specific pages from the **Harry_Potter_(www.ztcprep.com).pdf** PDF based on user input (birth date and year) and saves the content into two text files (`file1.txt` and `file2.txt`). The extraction is based on page numbers written in the PDF (e.g., "P a g e | 6") and uses Python for automating the process.

In this assignment, we utilized Hadoop Streaming to perform a MapReduce operation using custom Python scripts as the mapper and reducer. The task involved processing text files(extracted from above process) stored on HDFS with Python scripts that rely on external dependencies packaged within a virtual environment.

### Pre-requisites
1. **Python**: Ensure python installed and accessible
2. **Hadoop Setup:** Ensure that Hadoop is properly set up and running on your local or cluster environment.
3. **Python Virtual Environment:** Use a Python virtual environment to manage dependencies required for the mapper and reducer scripts (e.g., PyEnchant).
4. **HDFS:** Files should be uploaded to HDFS for processing by the MapReduce job.
5. Windows Subsystem for Linux: 

### Files:
- `Index_Extractor.py`: Extracts the Table of Contents (TOC) from the provided PDF and stores it in a `table_of_contents.json` file.
- `Content_Extractor.py`: Uses the TOC and user input (birth date and year) to generate `file1.txt` and `file2.txt`. These files are uploaded to HDFS for the MapReduce job.
- `requirements.txt`: Lists required Python packages.
- `Harry_Potter_(www.ztcprep.com).pdf`: The PDF used for extraction (you'll need to download and place it in the appropriate folder).
- `table_of_contents.json`: Auto-generated JSON file that holds the table of contents.
- ```mapper1.py:``` The mapper script reads each line from the input, splits it into words, and outputs key-value pairs where the key is the word and the value is 1.
- ```reducer1.py:``` The reducer script aggregates the occurrences of each word and outputs the total count for each word
- ```mapper2.py```: This mapper reads file2.txt, uses PyEnchant to check if each word is an English word, and emits key-value pairs for non-English words with a count of 1. 
- ```myenv_dependencies.zip:```The zip file containing the virtual environment and all necessary dependencies (such as pyenchant) for the MapReduce jobs.

---

## How to Download and Set Up

### 1. Clone or Download the Repository
First, clone this repository or download it as a zip file.

```bash
git clone https://github.com/Manognarayasam/603_Assignment_2.git
```
### 2. Virtual Environment
You can optionally create a virtual environment using below command, to run the project

```bash
python -m venv .venv
```

Activate .venv

```bash
 .\.venv\Scripts\activate
 ```




### 3. Install Dependencies
Ensure you have Python installed (version 3.7 or higher is recommended). Then, navigate to the project folder and install the required Python packages using the requirements.txt file:

```bash
pip install -r requirements.txt

```

---
## How to Run the Project

### 1. Extract the Table of Contents
Run the Index_Extractor.py file to extract the Table of Contents from the PDF (which is inside Data Gathering directory)

```bash
python .\Index_Extractor.py
```
This will generate a table_of_contents.json file inside the Data folder, which contains the structure of the book and the page numbers.



### 2. Generate file1.txt and file2.txt
Run the Content_Extractor.py file, which will prompt you to enter your birth date:

```bash
python .\Content_Extractor.py

```

Input your birth date in the YYYY-MM-DD format. The program will:

- Use your birth date to select the appropriate book and internal pages.
- Extract the relevant content from the PDF into file1.txt and file2.txt.

The extracted content will be saved as:

- ```file1.txt:``` Extracts 10 pages starting from the page corresponding to your birth date.
- ```file2.txt:``` Extracts 10 pages starting from the page corresponding to the last two digits of your birth year.


> Note: Used Windows Subsystem for Linux to run the Hadoop


### 3. Upload Files to HDFS

```bash
# Create a directory for the assignment in HDFS
hdfs dfs -mkdir /user/manogna/assignment2/

# Upload the input files (file1.txt and file2.txt) to HDFS
hdfs dfs -put file1.txt /user/manogna/assignment2/
hdfs dfs -put file2.txt /user/manogna/assignment2/

# Upload the dependency package to HDFS
hdfs dfs -put myenv_dependencies.zip /user/manogna/assignment2/
```

Run mapper 1 code 

```bash
hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
-input /user/manogna/assignment2/file1.txt \
-output /user/manogna/assignment2/output1 \
-mapper "python3 /home/manogna/mapper1.py" \
-reducer "python3 /home/manogna/reducer1.py"
```

Run Mapper 2 code

```bash
 hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar 
 -files myenv_dependencies.zip,mapper2.py,reducer1.py 
 -archives myenv_dependencies.zip#myenv_dependencies 
 -input /user/manogna/assignment2/file2.txt 
 -output /user/manogna/assignment2/output2 
 -mapper "python3 myenv_dependencies/mapper2.py" 
 -reducer "python3 myenv_dependencies/reducer1.py"
```



 Check the word count output for Task 1 and Task 2
 
 ```bash
hdfs dfs -cat /user/manogna/assignment2/output1/part-00000

hdfs dfs -cat /user/manogna/assignment2/output2/part-00000
```