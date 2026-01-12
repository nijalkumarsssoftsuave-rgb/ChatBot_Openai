#run using this in a separate port and outside the project directory


# import streamlit as st
# import requests
#
# API_BASE_URL = "http://127.0.0.1:8000"
#
# st.set_page_config(page_title="RAG PDF Chat")
#
# # -----------------------------
# # Session state
# # -----------------------------
# if "uploaded" not in st.session_state:
#     st.session_state.uploaded = False
#
# if "upload_key" not in st.session_state:
#     st.session_state.upload_key = 0
#
#
# st.title("📄 RAG PDF Question Answering")
#
# # -----------------------------
# # Upload Section
# # -----------------------------
# st.header("Upload PDF Document")
#
# upload_container = st.container()
#
# with upload_container:
#     uploaded_file = st.file_uploader(
#         "Choose a PDF file",
#         type=["pdf"],
#         key=f"uploader_{st.session_state.upload_key}"
#     )
#
# if uploaded_file and not st.session_state.uploaded:
#     with st.spinner("Uploading and indexing document..."):
#         response = requests.post(
#             f"{API_BASE_URL}/upload/pdf",
#             files={
#                 "file": (
#                     uploaded_file.name,
#                     uploaded_file,
#                     "application/pdf"
#                 )
#             }
#         )
#
#     if response.status_code == 200:
#         st.session_state.uploaded = True
#
#         # 🔑 Reset uploader safely
#         st.session_state.upload_key += 1
#
#         st.success(f"Uploaded: {uploaded_file.name}")
#     else:
#         st.error(response.json().get("detail", "Upload failed"))
#
# # -----------------------------
# # Ask Section
# # -----------------------------
# st.header("Ask a Question")
#
# if not st.session_state.uploaded:
#     st.info("Please upload a PDF first")
# else:
#     question = st.text_input(
#         "Enter your question",
#         placeholder="Ask something from the uploaded document"
#     )
#
#     if st.button("Ask"):
#         if not question.strip():
#             st.warning("Please enter a question")
#         else:
#             with st.spinner("Generating answer..."):
#                 response = requests.post(
#                     f"{API_BASE_URL}/ask",
#                     params={"question": question}
#                 )
#
#             if response.status_code == 200:
#                 st.subheader("Answer")
#                 st.write(response.json().get("answer"))
#             else:
#                 st.error("Failed to get answer")
