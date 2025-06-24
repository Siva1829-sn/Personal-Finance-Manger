import streamlit as st
import pandas as pd
import openai

# Set your OpenAI API key
openai.api_key = "your-api-key-here"  # Replace this with your real key

# Function to ask GPT
def ask_gpt(question, summary):
    prompt = f"""You are a smart finance assistant. 
Here is the user's expense summary:

{summary}

Now answer this question based on the data: "{question}"
If you don't find relevant info, say 'Sorry, I couldn't find that in your data.'
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

# Streamlit App UI
st.set_page_config(page_title="Personal Finance LLM Tracker")
st.title("💰 Personal Finance Tracker with LLM (OpenAI GPT)")

upload = st.file_uploader("📂 Upload your expenses CSV", type="csv")

if upload:
    df = pd.read_csv(upload, parse_dates=["Date"])

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Spending by Category")
    category_total = df.groupby("Category")["Amount"].sum()
    st.bar_chart(category_total)

    question = st.text_input("❓ Ask a question about your expenses (e.g., 'How much did I spend on food in May?')")

    if question:
        # Group by summary (for LLM)
        summary = df.groupby(["Category", pd.Grouper(key="Date", freq="M")])["Amount"].sum().to_string()

        with st.spinner("Thinking... 🤖"):
            answer = ask_gpt(question, summary)
            st.success(answer)
