# SQL Generator With Prompt

## Project Description

This project provides simple web-based interface built with Flask that allows users to convert natural language sentences into executable SQL queries with example of data. Simply type your question in plain text, and the application will generate the corresponding SQL, making database interaction more intuitive and accessible.

In the example, the dataset is a [**Netflix Movies and TV Shows**](https://www.kaggle.com/datasets/shivamb/netflix-shows) from Kaggle which is free to download and try both simple and complex query on SQL generator

## Features
- **Natural Language Input**: Users can easily type questions about their data using everyday language.
- **SQL Query Generation**: Converting natural language sentences into an executable and accurate SQL queries.
- **Simple Web Interface**: A clean and simple UI input and output.

## Technology Stacks
- **Python**: The core programming language.
- **Flask**: Web framework for developing the application.
- **HTML/CSS**: For the front-end interface.
- **OpenAI API**: A Natural Language Processing (NLP) library that integrated to perform the actual NL-to-SQL conversion.

## Setup and Installation
Follow these steps to project up and running on the local machine

### Prerequisites
- Python3 3.x installed on your system.
- `pip` (Python package installer).
- Data loaded in your local database.

### Steps
1. **Clone the repository to your local machine**
```
git clone [repo_url] 
cd [your-repo-name]
```

2. **Create a virtual environment**
```
python3 -m venv venv
```

4. **Activate the existed virtual environment**
- **On Windows**
```
venv\Scripts\activate
```
- **On Mac**
```
source venv/bin/activate
```

4. **Install dependencies**
`pip3 install -r requirements.txt`

5. **Create .env file to collect all secret values**
In `.env` should contain all of these values
```
# LLM
API_KEY=[your-OpenAI-API-key]

# Database
DB_HOST=[your-database-host]
DB_PORT=[your-database-port]
DB_USER=[your-database-username]
DB_PASSWORD=[your-database-password]
DB_NAME=postgres # In this version allow only PostgreSQL

# Flask Secret Key
SECRET_KEY=[your-generated-flask-secret-key]
```

6. Change the data input and few-shot example for LLM (_Additional: If you want to change data_)
Files to be changed are in the list below:
- `data/schema/database_schema.sql`: Provided the `CREATE TABLE` of SQL query to let LLM understand the data schema.
- `data/schema/table_descriptions.json`: Description of the database and table as well as given some examples of data.
- `prompts/examples/few_shot_examples.json`: Given an example of query from your database to LLM.

## Usage
1. **Run the Flask application**
```
python3 app.py
```
You will see output indicating at the Flase server is running, usually on `http://127.0.0.1:5000/`.

3. **Open in browser**
Navigate to `http://127.0.0.1:5000/` in the web browser.

4. **Enter you question**
Type your natural language sentence to get insights what you want from your data.

5. **Generate SQL**
Click the "Generate SQL Query" button to retrieve the executable SQL query and given example of the data with maximum 100 rows.

## Example

### Input
```
Show me director and title for first 100 rows
```

### Output
```
SELECT director, title FROM netflix_titles LIMIT 100;
```
