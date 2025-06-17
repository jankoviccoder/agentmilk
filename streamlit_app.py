import streamlit as st
import openai
import time

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("🐄 Milk Health Agent – Excel Analyzer")
uploaded_file = st.file_uploader("Upload Excel file (KU)", type=["xlsx"])

if uploaded_file:
    st.success("✅ Excel file uploaded")
    
    # 1. Nahrát soubor na OpenAI
    file_obj = openai.files.create(file=uploaded_file, purpose="assistants")

    # 2. Vytvořit vlákno
    thread = openai.beta.threads.create()

    # 3. Poslat zprávu se souborem
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Please analyze the uploaded milk yield Excel file.",
        file_ids=[file_obj.id],
    )

    # 4. Spustit asistenta
    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=st.secrets["ASSISTANT_ID"],
    )

    # 5. Počkat na odpověď
    with st.spinner("🧠 Agent is analyzing..."):
        while True:
            run = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run.status == "completed":
                break
            time.sleep(1)

    # 6. Získat odpověď
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
        if msg.role == "assistant":
            st.subheader("🧠 Assistant’s Reply:")
            st.markdown(msg.content[0].text.value)
