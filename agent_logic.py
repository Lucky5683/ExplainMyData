import os
import json
import polars as pl
import plotly.express as px

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_experimental.tools.python.tool import PythonAstREPLTool


def create_agent(df: pl.DataFrame, df_metadata: dict):
    """
    Fast and professional AI Data Analyst Agent
    Optimized for:
    - Faster responses
    - Better chart generation
    - Stable execution
    """

    # ---------------------------------------------------------
    # Validate API Key
    # ---------------------------------------------------------
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found. Please add it in .env file"
        )

    # ---------------------------------------------------------
    # FAST GEMINI MODEL
    # ---------------------------------------------------------
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=api_key
    )

    # ---------------------------------------------------------
    # Python Tool
    # ---------------------------------------------------------
    python_repl = PythonAstREPLTool(
        locals={
            "df": df,
            "pl": pl,
            "px": px
        }
    )

    tools = [
        Tool(
            name="Python_REPL",
            func=python_repl.run,
            description="""
Use this tool for dataset analysis.

Available:
- df = Polars DataFrame
- pl = Polars
- px = Plotly Express

Rules:
1. Use valid Python code
2. Use print() for outputs
3. For charts:
   fig = px.bar(...)
4. Never use fig.show()
"""
        )
    ]

    # ---------------------------------------------------------
    # Safe Metadata
    # ---------------------------------------------------------
    metadata_text = json.dumps(
        df_metadata,
        indent=2
    )

    metadata_text = metadata_text.replace("{", "{{")
    metadata_text = metadata_text.replace("}", "}}")

    # ---------------------------------------------------------
    # FAST SYSTEM PROMPT
    # ---------------------------------------------------------
    system_prompt = f"""
You are an expert data analyst.

Dataset is loaded as `df`.

Metadata:
{metadata_text}

Use Python_REPL only when required.

Instructions:
1. Be fast and accurate.
2. Prefer single tool call.
3. Use Polars syntax.
4. Keep answers concise.
5. If graph needed:
   create Plotly chart as `fig`
6. Never call fig.show()

For insights:
- trends
- anomalies
- correlations
- recommendations
"""

    # ---------------------------------------------------------
    # Create Agent
    # ---------------------------------------------------------
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,                 # Faster
        handle_parsing_errors=True,
        max_iterations=2,             # Faster
        early_stopping_method="generate",
        agent_kwargs={
            "prefix": system_prompt
        }
    )

    return agent, python_repl


# ---------------------------------------------------------
# TEST MODE
# ---------------------------------------------------------
if __name__ == "__main__":

    df = pl.DataFrame({
        "Product": ["A", "B", "C"],
        "Sales": [100, 200, 150]
    })

    metadata = {
        "rows": df.height,
        "columns": df.columns,
        "dtypes": [str(i) for i in df.dtypes]
    }

    agent, tool = create_agent(df, metadata)

    result = agent.invoke({
        "input": "Which product has highest sales?"
    })

    print(result["output"])