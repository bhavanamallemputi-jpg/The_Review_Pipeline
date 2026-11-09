import streamlit as st
import json
from pathlib import Path

from ai_reviewer import review_code
from refactoring import refactor_code
from analyzer import analyze_code
from scoring import calculate_quality_score
from report import generate_report


# Page configuration
st.set_page_config(
    page_title="AI Code Review Pipeline",
    page_icon="🤖",
    layout="wide"
)

# Website title
st.title("🤖 AI-Assisted Code Review Pipeline")

st.write(
    "Analyze your code, detect bugs, improve code quality "
    "and generate automated reports."
)

st.divider()

# Sidebar
st.sidebar.title("Project Dashboard")
st.sidebar.write("Upload your source code to begin.")

# File upload
uploaded_file = st.file_uploader(
    "Upload your Python file",
    type=["py"]
)

if uploaded_file is not None:

    source_code = uploaded_file.getvalue().decode("utf-8")

    st.success("File uploaded successfully!")

    st.subheader("📄 Uploaded File")
    st.write("File Name:", uploaded_file.name)

    # Display source code
    st.subheader("💻 Original Source Code")

    st.code(source_code, language="python")

    if st.button("Start Code Analysis", type="primary"):

        # AI Code Review
        st.subheader("🔍 AI Code Review")

        review_results = []

        with st.spinner("Reviewing your code..."):

            try:
                review_results = review_code(source_code)

                if review_results:
                    st.json(review_results)
                else:
                    st.success("No issues reported by AI.")

            except Exception as error:
                st.warning(
                    f"AI Review temporarily unavailable: {error}"
                )

        # AI Refactoring
        st.subheader("🛠️ AI Code Refactoring")

        refactoring_results = {}

        with st.spinner("Refactoring your code..."):

            try:
                refactoring_results = refactor_code(source_code)

                st.code(
                    refactoring_results["refactored_code"],
                    language="python"
                )

                st.write("Explanation:")
                st.write(refactoring_results["explanation"])

            except Exception as error:
                st.warning(
                    f"AI Refactoring temporarily unavailable: {error}"
                )

        # Static Analysis
        st.subheader("📊 Static Code Analysis")

        try:
            analysis_results = analyze_code(source_code)

            col1, col2 = st.columns(2)

            col1.metric(
                "Lines of Code",
                analysis_results["lines_of_code"]
            )

            col2.metric(
                "Logical Lines",
                analysis_results["logical_lines"]
            )

            col3, col4 = st.columns(2)

            col3.metric(
                "Average Complexity",
                analysis_results["average_complexity"]
            )

            col4.metric(
                "Maintainability Index",
                analysis_results["maintainability_index"]
            )

            # Quality Score
            st.subheader("⭐ Code Quality Score")

            quality_score = calculate_quality_score(
                analysis_results,
                review_results
            )

            st.metric(
                "Final Quality Score",
                f"{quality_score}/100"
            )

            st.progress(quality_score / 100)

            # Report Generation
            st.subheader("📑 Generated Reports")

            json_report, markdown_report, html_report = generate_report(
                filename=uploaded_file.name,
                language="Python",
                analysis_results=analysis_results,
                quality_score=quality_score,
                review_results=review_results,
                refactoring_results=refactoring_results
            )

            st.success("Reports generated successfully!")

            # Download buttons
            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    "Download JSON",
                    data=Path(json_report).read_bytes(),
                    file_name="review_report.json",
                    mime="application/json"
                )

            with col2:
                st.download_button(
                    "Download Markdown",
                    data=Path(markdown_report).read_bytes(),
                    file_name="review_report.md",
                    mime="text/markdown"
                )

            with col3:
                st.download_button(
                    "Download HTML",
                    data=Path(html_report).read_bytes(),
                    file_name="review_report.html",
                    mime="text/html"
                )

        except Exception as error:
            st.error(f"Static analysis failed: {error}")

st.divider()

st.caption("AI-Assisted Code Review Pipeline | Python Project")