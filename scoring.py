def calculate_quality_score(analysis_results, review_results=None):

    # Start with a perfect score
    score = 100

    # Check maintainability index
    maintainability = analysis_results["maintainability_index"]

    if maintainability < 20:
        score -= 30
    elif maintainability < 40:
        score -= 20
    elif maintainability < 60:
        score -= 10

    # Check cyclomatic complexity
    complexity = analysis_results["average_complexity"]

    if complexity > 20:
        score -= 25
    elif complexity > 10:
        score -= 15
    elif complexity > 5:
        score -= 5

    # Reduce score based on AI review findings
    if review_results:
        for issue in review_results:
            severity = issue.get("severity", "").lower()

            if severity == "critical":
                score -= 15
            elif severity == "high":
                score -= 10
            elif severity == "medium":
                score -= 5
            elif severity == "low":
                score -= 2

    # Keep score between 0 and 100
    score = max(0, min(100, score))

    return score