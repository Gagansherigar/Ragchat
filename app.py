import streamlit as st
from ragcore import process_pdf, retrieve, generate_answer, summarize_chunks

st.set_page_config(page_title="PDF AI Assistant", layout="wide")

st.title("📄 AI PDF Summarizer & Q&A")


uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if "processed" not in st.session_state:
    st.session_state.processed = False


if uploaded_file and not st.session_state.processed:
    with st.spinner("Processing PDF..."):
        text, chunks, index = process_pdf(uploaded_file)

        st.session_state.text = text
        st.session_state.chunks = chunks
        st.session_state.index = index
        st.session_state.processed = True

    st.success("✅ PDF processed successfully!")


if st.session_state.processed:

    st.divider()

    mode = st.radio("Choose Mode", ["📄 Summarize", "❓ Ask Questions"])

    if mode == "📄 Summarize":
        if st.button("Generate Summary"):
            with st.spinner("Summarizing..."):
                summary = summarize_chunks(st.session_state.chunks)

                st.subheader("📌 Summary")
                st.write(summary)

    elif mode == "❓ Ask Questions":
        question = st.text_input("Ask a question about the document:")

        if question:
            with st.spinner("Thinking..."):
                results = retrieve(
                    question,
                    st.session_state.index,
                    st.session_state.chunks
                )

                context = "\n".join(results)
                answer = generate_answer(context, question)

                st.subheader("🤖 Answer")
                st.write(answer)

                with st.expander("🔍 Retrieved Context"):
                    st.write(context)