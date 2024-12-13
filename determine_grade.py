import csv
import os
from typing import List


def get_csv_path(filename: str = "data.csv") -> str:
    """Get the file path to save the CSV file in the same directory."""
    return os.path.join(os.path.dirname(__file__), filename)


def determine_grade(score: int, best_score: int = 100) -> str:
    """Determine the grade based on the score and the best possible score."""
    if score >= best_score - 10:
        return 'A'
    elif score >= best_score - 20:
        return 'B'
    elif score >= best_score - 30:
        return 'C'
    elif score >= best_score - 40:
        return 'D'
    else:
        return 'F'


def record_scores(student_name: str, scores: List[int], grades: List[str]) -> None:
    """Record the scores and grades into a CSV."""
    file_path = get_csv_path()
    file_exists = os.path.exists(file_path)

    max_tests = 4
    padded_scores = scores + ["NA"] * (max_tests - len(scores))
    padded_grades = grades + ["NA"] * (max_tests - len(grades))
    valid_scores = [score for score in scores if isinstance(score, int)]
    average_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
    best_attempt = max(valid_scores) if valid_scores else 0
    best_grade = determine_grade(best_attempt, best_score=100)

    row = [student_name] + padded_scores + [f"Avg: {average_score:.2f}", best_grade]

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            headers = ['Student Name'] + [f"Test {i+1}" for i in range(max_tests)] + ['Average', 'Best Grade']
            writer.writerow(headers)
        writer.writerow(row)


def calculate_grades(scores: List[int]) -> List[str]:
    """Calculate grades for all scores using static thresholds."""
    return [determine_grade(score, best_score=100) for score in scores]
