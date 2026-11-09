from ingestion import read_source_file
from ai_reviewer import review_code
from refactoring import refactor_code
from analyzer import analyze_code
from scoring import calculate_quality_score
from report import generate_report

# Step 1: Read source file
file_data = read_source_file("sample.py")

print("File Name:", file_data["filename"])
print("Language:", file_data["language"])

source_code = file_data["source_code"]

# Step 2: AI Code Review
print("\nStarting AI Code Review...")

review_results = []

try:
    review_results = review_code(source_code)
    print("\nAI Review Results:")
    print(review_results)

except Exception as error:
    print("\nAI Code Review temporarily unavailable:")
    print(error)

# Step 3: AI Code Refactoring
print("\nStarting AI Code Refactoring...")

refactoring_results = {}

try:
    refactoring_results = refactor_code(source_code)

    print("\nRefactored Code:")
    print(refactoring_results["refactored_code"])

    print("\nExplanation:")
    print(refactoring_results["explanation"])

except Exception as error:
    print("\nAI Refactoring temporarily unavailable:")
    print(error)

# Step 4: Static Code Analysis
print("\nStarting Static Code Analysis...")

analysis_results = analyze_code(source_code)

print("\nStatic Analysis Results:")

for metric, value in analysis_results.items():
    print(f"{metric}: {value}")

# Step 5: Calculate Quality Score
print("\nCalculating Code Quality Score...")

quality_score = calculate_quality_score(
    analysis_results,
    review_results
)

print("\nFinal Code Quality Score:")
print(f"{quality_score}/100")

# Step 6: Generate Reports
print("\nGenerating Reports...")

json_report, markdown_report, html_report = generate_report(
    filename=file_data["filename"],
    language=file_data["language"],
    analysis_results=analysis_results,
    quality_score=quality_score,
    review_results=review_results,
    refactoring_results=refactoring_results
)

print("\nAll Reports Generated Successfully!")

print("JSON Report:", json_report)
print("Markdown Report:", markdown_report)
print("HTML Report:", html_report)

print("\nThe Review Pipeline Completed Successfully!")