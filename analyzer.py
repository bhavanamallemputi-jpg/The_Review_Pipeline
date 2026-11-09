from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze


def analyze_code(source_code):

    # Calculate lines of code
    raw_metrics = analyze(source_code)

    # Calculate cyclomatic complexity
    complexity_results = cc_visit(source_code)

    if complexity_results:
        average_complexity = sum(
            item.complexity for item in complexity_results
        ) / len(complexity_results)
    else:
        average_complexity = 0

    # Calculate maintainability index
    maintainability = mi_visit(source_code, multi=True)

    return {
        "lines_of_code": raw_metrics.loc,
        "logical_lines": raw_metrics.lloc,
        "average_complexity": round(average_complexity, 2),
        "maintainability_index": round(maintainability, 2)
    }