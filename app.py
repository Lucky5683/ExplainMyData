import asyncio
import os

# ---------------------------------------------------
# Fix event loop issue in Streamlit thread
# ---------------------------------------------------
try:
    asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import streamlit as st
from dotenv import load_dotenv
from data_engine import load_file, get_data_context
from agent_logic import create_agent

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="ExplainMyData",
    layout="wide"
)

st.title("ExplainMyData")
st.subheader("AI-Powered Data Analytics Platform")

# ---------------------------------------------------
# Session State Initialization
# ---------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = None

if "python_tool" not in st.session_state:
    st.session_state.python_tool = None

if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------
with st.sidebar:

    st.header("Configuration")

    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key and api_key != "your_api_key_here":
        st.success("API Key Configured")
    else:
        st.error("API Key Missing")

    st.markdown("---")

    st.header("Upload Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel File",
        type=["csv", "xlsx"]
    )

# ---------------------------------------------------
# File Processing
# ---------------------------------------------------
if uploaded_file is not None:

    if st.session_state.uploaded_filename != uploaded_file.name:

        try:
            with st.spinner("Processing dataset..."):

                df = load_file(uploaded_file, uploaded_file.name)

                df_metadata = get_data_context(df)

                st.session_state.df = df
                st.session_state.df_metadata = df_metadata
                st.session_state.uploaded_filename = uploaded_file.name

                agent, python_tool = create_agent(df, df_metadata)

                st.session_state.agent = agent
                st.session_state.python_tool = python_tool

                st.session_state.messages = []

            st.sidebar.success("Dataset loaded successfully")

            with st.sidebar.expander("Preview"):
                st.dataframe(
                    df.head(10).to_pandas(),
                    use_container_width=True
                )

            with st.sidebar.expander("Dataset Information"):
                st.write(df_metadata)

        except Exception as e:
            st.sidebar.error(f"Error reading file: {str(e)}")

# ---------------------------------------------------
# Display Chat History
# ---------------------------------------------------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if "fig" in msg and msg["fig"] is not None:
            st.plotly_chart(
                msg["fig"],
                use_container_width=True
            )

# ---------------------------------------------------
# Chat Input
# ---------------------------------------------------
prompt = st.chat_input("Ask questions about your data")

if prompt:

    if st.session_state.agent is None:
        st.error("Please upload a dataset first.")

    elif not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "your_api_key_here":
        st.error("Please configure your API key in the .env file.")

    else:

        # User Message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant Response
        with st.chat_message("assistant"):

            with st.spinner("Analyzing dataset..."):

                try:
                    # Clear previous chart
                    if st.session_state.python_tool:
                        st.session_state.python_tool.locals.pop("fig", None)

                    result = st.session_state.agent.invoke({
                        "input": prompt
                    })

                    response_text = result.get(
                        "output",
                        str(result)
                    )

                    st.markdown(response_text)

                    fig = None

                    if st.session_state.python_tool:
                        fig = st.session_state.python_tool.locals.get("fig")

                    if fig is not None:

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text,
                            "fig": fig
                        })

                    else:

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response_text
                        })

                except Exception as e:

                    error_message = f"Error while analyzing data:\n\n{str(e)}"

                    st.error(error_message)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_message
                    })