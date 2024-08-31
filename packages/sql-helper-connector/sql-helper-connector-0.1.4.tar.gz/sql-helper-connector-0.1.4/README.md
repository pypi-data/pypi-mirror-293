# SQL Helper Tool

## Project Background

This project is built upon `ClustroAI` technology, aiming to provide a `SQL Helper` tool that enables users to interact with databases using natural language. Once a database connection is established, users can start querying without the need to write complex SQL queries. The tool understands natural language requests and returns accurate data analysis results along with the corresponding SQL statements. To ensure database information security, the project supports private database connection creation, keeping all database information confidential.

## Key Features

- **Database Connection Creation**: Users can create database connections in a private manner, ensuring no credential leakage.
- **Natural Language Querying**: Users can query the database through natural language without directly writing SQL statements.
- **Data Analysis and SQL Generation**: The system automatically generates data analysis results and corresponding SQL statements based on natural language queries.
- **Security**: Supports private connection methods to protect database information.

## Deployment

### Local Deployment

1. Clone the repository to your local machine:

```bash
git clone <repository-url>
cd sql_helper
pip install -r requirements.txt
python main.py
````

### Docker Deployment
Ensure you have Docker and Docker-compose installed. Then, follow these steps:
```bash
docker-compose build
docker-compose up -d
```
# tortoise-cli
```bash
cd backend
tortoise-cli -c app.setting.TORTOISE_ORM shell

或者 export TORTOISE_ORM=app.setting.TORTOISE_ORM
tortoise-cli shell
```