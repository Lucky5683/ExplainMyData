# ExplainMyData

ExplainMyData is an AI-powered data analytics platform that preprocesses Excel and CSV datasets, analyzes structured data, answers natural language queries, and generates intelligent insights with interactive visualizations. The system is designed to make data understanding simple, fast, and accessible for all users, including those without technical expertise.

## Features

- Upload Excel (`.xlsx`) and CSV (`.csv`) files
- Automatic data preprocessing and cleaning
- Natural language query support
- AI-generated insights and summaries
- Interactive charts and graphs
- Trend, comparison, and anomaly detection
- User-friendly web interface

## Technologies Used

- Python
- Streamlit
- Pandas / Polars
- Plotly
- LangChain
- Google Gemini API
- Natural Language Processing (NLP)

## How It Works

1. Upload a structured dataset.
2. Ask questions in plain English.
3. The system processes the data.
4. AI analyzes the dataset.
5. Results are displayed with charts and explanations.

## Example Queries

- Which product has the highest sales?
- Show monthly revenue trend.
- Which assets are losing value today?
- Plot top 5 records by value.
- Detect anomalies in the dataset.

## Installation

```bash
git clone https://github.com/yourusername/ExplainMyData.git
cd ExplainMyData
pip install -r requirements.txt
streamlit run app.py
