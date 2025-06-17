import streamlit as st
import openai
import time

openai.api_key = st.secrets.get("OPENAI_API_KEY")

st.title("🤖 Excel AI Agent")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded_file:
    file_obj = openai.files.create(file=uploaded_file, purpose="assistants")
    st.success("✅ File uploaded to OpenAI")

    st.info("Asking assistant to analyse your spreadsheet...")

    assistant_id = st.secrets["ASSISTANT_ID"]
    thread = openai.beta.threads.create()
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Please analyse the uploaded Excel file.",
        file_ids=[file_obj.id],
    )
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    with st.spinner("💡 Thinking..."):
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
            time.sleep(1)

    messages = openai.beta.t
