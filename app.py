import streamlit as st
import pandas as pd

from database import get_schema, get_relationships, execute_query
from sql_generator import generate_sql, explain_sql
from sql_validator import validate_sql

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🗄️",
    layout="wide"
)

# ============================================================
# SESSION STATE
# (keeps the generated SQL around across Streamlit reruns so the
#  "Execute Query" button below still works after "Generate SQL")
# ============================================================
if "sql" not in st.session_state:
    st.session_state.sql = None
if "is_safe" not in st.session_state:
    st.session_state.is_safe = False
if "validation_message" not in st.session_state:
    st.session_state.validation_message = ""

# ============================================================
# TITLE
# ============================================================
st.title("AI SQL Query Generator & Database Assistant")
st.write(
    """
    Ask questions about your MySQL database using natural language.
    The AI converts your question into SQL and executes the query safely.
    """
)

# ============================================================
# LOAD DATABASE INFORMATION
# ============================================================
try:
    schema = get_schema()
    relationships = get_relationships()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("Database")
    st.success("Connected to MySQL")
    st.divider()
    st.subheader("Available Tables")
    for table in schema:
        st.write(f"• {table}")
    st.divider()
    st.subheader("Relationships")
    for relationship in relationships:
        st.caption(relationship)

# ============================================================
# DATABASE SCHEMA
# ============================================================
with st.expander("View Database Schema"):
    for table, columns in schema.items():
        st.subheader(table)
        for column in columns:
            st.write(f"- {column}")

# ============================================================
# QUESTION INPUT
# ============================================================
st.header("Ask Your Database")
question = st.text_area(
    "Enter your question",
    placeholder="Example: Show the top 5 customers by total purchase amount.",
    height=100
)

# ============================================================
# SAMPLE QUESTIONS
# ============================================================
st.subheader("Sample Questions")
sample_col1, sample_col2, sample_col3 = st.columns(3)
with sample_col1:
    st.write("• Show all customers from Pune.")
    st.write("• Show all products.")
with sample_col2:
    st.write("• Show top 5 customers by sales.")
    st.write("• What is the total sales?")
with sample_col3:
    st.write("• Show sales by city.")
    st.write("• Which product generated the most revenue?")

# ============================================================
# GENERATE BUTTON
# ============================================================
generate_button = st.button("Generate SQL", type="primary", use_container_width=True)

if generate_button:
    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Generating SQL..."):
        try:
            sql = generate_sql(question, schema, relationships)
        except Exception as e:
            st.error(f"AI error: {e}")
            st.stop()

    is_safe, validation_message = validate_sql(sql)

    # Store in session_state so it survives the rerun triggered by
    # the "Execute Query" button click below.
    st.session_state.sql = sql
    st.session_state.is_safe = is_safe
    st.session_state.validation_message = validation_message

# ============================================================
# SHOW GENERATED SQL (persists across reruns via session_state)
# ============================================================
if st.session_state.sql:
    st.subheader("Generated SQL")
    st.code(st.session_state.sql, language="sql")

    if not st.session_state.is_safe:
        st.error(st.session_state.validation_message)
    else:
        st.success(st.session_state.validation_message)

        # ========================================================
        # EXECUTE QUERY
        # ========================================================
        execute_button = st.button("Execute Query", type="primary")

        if execute_button:
            with st.spinner("Executing query..."):
                try:
                    dataframe = execute_query(st.session_state.sql)
                except Exception as e:
                    st.error(f"SQL execution error: {e}")
                    st.stop()

            # ====================================================
            # RESULTS
            # ====================================================
            st.subheader("Query Results")
            if dataframe.empty:
                st.info("Query executed successfully, but no records were found.")
            else:
                st.dataframe(dataframe, use_container_width=True)

                # ================================================
                # RESULT STATISTICS
                # ================================================
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Rows", len(dataframe))
                with col2:
                    st.metric("Columns", len(dataframe.columns))

                # ================================================
                # CHART
                # ================================================
                numeric_columns = dataframe.select_dtypes(include="number").columns.tolist()
                if len(numeric_columns) >= 1:
                    st.subheader("Visualization")
                    selected_column = st.selectbox("Select numeric column", numeric_columns)
                    chart_data = dataframe[[selected_column]]
                    st.bar_chart(chart_data)

                # ================================================
                # DOWNLOAD
                # ================================================
                csv = dataframe.to_csv(index=False)
                st.download_button(
                    "Download Results as CSV",
                    csv,
                    "query_results.csv",
                    "text/csv"
                )

            # ====================================================
            # EXPLANATION
            # ====================================================
            with st.expander("Explain SQL Query"):
                with st.spinner("Generating explanation..."):
                    try:
                        explanation = explain_sql(st.session_state.sql)
                        st.write(explanation)
                    except Exception as e:
                        st.error(f"Explanation error: {e}")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("AI SQL Assistant | Python + Streamlit + Groq + MySQL")
