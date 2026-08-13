import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai


# =========================================================
# Load Environment Variables
# =========================================================

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="PaperMind AI",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# Header
# =========================================================

st.title("📄 PaperMind AI")

st.write(
    "An AI-powered research paper assistant that analyzes "
    "academic papers and provides summaries, insights, "
    "important questions, and answers."
)


# =========================================================
# API Key Check
# =========================================================

if not API_KEY:
    st.error(
        "❌ Google API key not found. "
        "Please add GOOGLE_API_KEY to your .env file."
    )
    st.stop()


# =========================================================
# Gemini Client
# =========================================================

client = genai.Client(api_key=API_KEY)


# =========================================================
# PDF Upload
# =========================================================

st.sidebar.header("📄 Upload Research Paper")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)


# =========================================================
# Main Application
# =========================================================

if uploaded_file:

    # -----------------------------------------------------
    # Extract PDF Text
    # -----------------------------------------------------

    reader = PdfReader(uploaded_file)

    paper_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            paper_text += text + "\n"


    # -----------------------------------------------------
    # Check PDF Content
    # -----------------------------------------------------

    if not paper_text.strip():

        st.error(
            "❌ Could not extract text from this PDF."
        )

        st.stop()


    # -----------------------------------------------------
    # Paper Information
    # -----------------------------------------------------

    st.success(
        "✅ Research paper uploaded successfully!"
    )

    st.subheader("📄 Paper Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Pages",
            len(reader.pages)
        )

    with col2:

        st.metric(
            "Characters Extracted",
            f"{len(paper_text):,}"
        )


    # =====================================================
    # AI Research Paper Analysis
    # =====================================================

    st.subheader(
        "🤖 AI Research Paper Analysis"
    )


    if st.button(
        "✨ Analyze Research Paper",
        type="primary"
    ):

        prompt = f"""
You are an expert research paper analysis assistant.

Analyze the following research paper and provide a clear,
structured response.

Research Paper:

{paper_text}

Provide the following sections:

1. 📖 Summary
Give a concise summary of the research paper.

2. 🎯 Research Objective
Explain the main objective or problem addressed.

3. 🔬 Methodology
Explain the methods, techniques, datasets, or models used.

4. 📊 Key Findings
List the important findings and results.

5. ⚠️ Limitations
Identify the limitations mentioned or apparent from the paper.

6. 💡 Key Insights
Provide the most important insights from the research.

7. 🔑 Important Keywords
List important technical keywords.

8. 🧠 Simple Explanation
Explain the research in simple language suitable for a student.

Use clear headings and bullet points.

Do not invent information that is not supported by the paper.
"""

        try:

            with st.spinner(
                "🤖 AI is analyzing your research paper..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

                analysis = response.text


            st.subheader(
                "📚 Research Paper Analysis"
            )

            st.markdown(analysis)

            st.success(
                "🎉 Research paper analysis completed successfully!"
            )


        except Exception as e:

            st.error(
                "❌ Unable to analyze the research paper."
            )

            st.warning(
                f"Error details: {e}"
            )


    # =====================================================
    # Generate Important Questions
    # =====================================================

    st.divider()

    st.subheader(
        "📚 Generate Important Questions"
    )

    st.write(
        "Generate important questions based on the uploaded "
        "research paper for study and revision."
    )


    if st.button(
        "📚 Generate Questions"
    ):

        question_generation_prompt = f"""
You are an academic study assistant.

Read the following research paper carefully.

Research Paper:
{paper_text}

Generate 10 important questions based ONLY on the
information available in the research paper.

Include a mixture of:

- Conceptual questions
- Methodology questions
- Dataset or experiment questions
- Results and findings questions
- Limitation questions

Do not provide answers.

Number the questions clearly from 1 to 10.
"""


        try:

            with st.spinner(
                "📚 Generating important questions..."
            ):

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=question_generation_prompt
                )

                questions = response.text


            st.subheader(
                "📝 Important Questions"
            )

            st.markdown(questions)


        except Exception as e:

            st.error(
                "❌ Unable to generate questions."
            )

            st.warning(
                f"Error details: {e}"
            )


    # =====================================================
    # Ask Questions About the Paper
    # =====================================================

    st.divider()

    st.subheader(
        "💬 Ask Questions About the Paper"
    )

    question = st.text_input(
        "Enter your question",
        placeholder="e.g. What methodology was used in this research?"
    )


    if st.button(
        "🔍 Ask AI"
    ):

        if not question.strip():

            st.warning(
                "⚠️ Please enter a question."
            )

        else:

            question_prompt = f"""
You are an AI research assistant.

Answer the user's question using ONLY the information
available in the research paper below.

Research Paper:

{paper_text}

User Question:

{question}

Provide a clear and accurate answer.

If the answer cannot be found in the paper, clearly say
that the information is not available in the uploaded paper.
"""


            try:

                with st.spinner(
                    "🤖 Finding the answer..."
                ):

                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=question_prompt
                    )

                    answer = response.text


                st.markdown(
                    "### 💡 AI Answer"
                )

                st.markdown(answer)


            except Exception as e:

                st.error(
                    "❌ Unable to generate an answer."
                )

                st.warning(
                    f"Error details: {e}"
                )


else:

    st.info(
        "👈 Upload a research paper PDF from the sidebar "
        "to get started."
    )


# =========================================================
# Footer
# =========================================================

st.divider()

st.caption(
    "📄 PaperMind AI | Powered by Google Gemini & Streamlit"
)