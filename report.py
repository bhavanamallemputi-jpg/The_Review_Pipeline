import json
from pathlib import Path
from datetime import datetime
import html


def generate_report(
    filename,
    language,
    analysis_results,
    quality_score,
    review_results=None,
    refactoring_results=None
):

    report_data = {
        "filename": filename,
        "language": language,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "static_analysis": analysis_results,
        "quality_score": quality_score,
        "review_findings": review_results or [],
        "refactoring": refactoring_results or {}
    }

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    # JSON Report
    json_path = reports_folder / "review_report.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(report_data, file, indent=4)

    # Markdown Report
    markdown_path = reports_folder / "review_report.md"

    with open(markdown_path, "w", encoding="utf-8") as file:
        file.write("# AI Code Review Report\n\n")
        file.write(f"**File:** {filename}\n\n")
        file.write(f"**Language:** {language}\n\n")
        file.write(f"**Date:** {report_data['date']}\n\n")

        file.write("## Static Analysis Results\n\n")

        for metric, value in analysis_results.items():
            file.write(f"- **{metric}:** {value}\n")

        file.write(f"\n## Quality Score\n\n**{quality_score}/100**\n")

        file.write("\n## AI Review Findings\n\n")

        if review_results:
            for issue in review_results:
                file.write(
                    f"- Line {issue.get('line')}: "
                    f"{issue.get('description')} "
                    f"(Severity: {issue.get('severity')})\n"
                )
        else:
            file.write("No review findings available.\n")

    # HTML Report
    html_path = reports_folder / "review_report.html"

    metrics_html = ""

    for metric, value in analysis_results.items():
        metrics_html += (
            f"<li><b>{html.escape(str(metric))}:</b> "
            f"{html.escape(str(value))}</li>"
        )

    findings_html = ""

    if review_results:
        for issue in review_results:
            findings_html += (
                f"<li>Line {html.escape(str(issue.get('line')))}: "
                f"{html.escape(str(issue.get('description')))} "
                f"(Severity: {html.escape(str(issue.get('severity')))})</li>"
            )
    else:
        findings_html = "<li>No review findings available.</li>"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Code Review Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f4f4f4;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
            }}
            h1, h2 {{
                color: #243b55;
            }}
            .score {{
                font-size: 28px;
                font-weight: bold;
                color: green;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI Code Review Report</h1>
            <p><b>File:</b> {html.escape(filename)}</p>
            <p><b>Language:</b> {html.escape(language)}</p>
            <p><b>Date:</b> {html.escape(report_data['date'])}</p>

            <h2>Static Analysis Results</h2>
            <ul>{metrics_html}</ul>

            <h2>Code Quality Score</h2>
            <p class="score">{quality_score}/100</p>

            <h2>AI Review Findings</h2>
            <ul>{findings_html}</ul>
        </div>
    </body>
    </html>
    """

    with open(html_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    return (
        str(json_path),
        str(markdown_path),
        str(html_path)
    )