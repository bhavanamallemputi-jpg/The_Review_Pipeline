from pathlib import Path

def read_source_file(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError("The selected file does not exist.")

    if path.suffix.lower() not in [".py", ".js"]:
        raise ValueError("Only Python and JavaScript files are supported.")

    source_code = path.read_text(encoding="utf-8")

    if not source_code.strip():
        raise ValueError("The selected file is empty.")

    if path.suffix.lower() == ".py":
        language = "Python"
    else:
        language = "JavaScript"

    line_count = len(source_code.splitlines())

    return {
        "filename": path.name,
        "language": language,
        "source_code": source_code,
        "line_count": line_count
    }