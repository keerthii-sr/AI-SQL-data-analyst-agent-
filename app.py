import streamlit as st
import pandas as pd
import sqlite3
from groq import Groq

# Initialize Groq

client = Groq(api_key="API_KEY_HERE")
st.title("🧠 AI SQL Data Analyst")

file = st.file_uploader("Upload CSV")

if file:
    df = pd.read_csv(file)
    st.write(df.head())

    conn = sqlite3.connect("data.db")
    df.to_sql("data", conn, if_exists="replace", index=False)

    question = st.text_input("Ask in English")

    if st.button("Get Answer"):
        # Convert question to SQL
        prompt = f"""
        Convert this question into SQL query for table named data:
        {question}
        Only return SQL query.
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )

        sql_query = response.choices[0].message.content

        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

        st.write("Generated SQL:", sql_query)

        result = pd.read_sql_query(sql_query, conn)
        st.write(result)
