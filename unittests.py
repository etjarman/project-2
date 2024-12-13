import unittest
import os
import csv
from determine_grade import (
    determine_grade,
    calculate_grades,
    record_scores,
    get_csv_path
)


class TestDetermineGrade(unittest.TestCase):
    def test_determine_grade(self):
        """Test the determine_grade function with various scores."""
        self.assertEqual(determine_grade(95), 'A')
        self.assertEqual(determine_grade(85), 'B')
        self.assertEqual(determine_grade(75), 'C')
        self.assertEqual(determine_grade(65), 'D')
        self.assertEqual(determine_grade(50), 'F')


class TestCalculateGrades(unittest.TestCase):
    def test_calculate_grades(self):
        """Test the calculate_grades function with various inputs."""
        scores = [95, 85, 75, 65]
        grades = calculate_grades(scores)
        self.assertEqual(grades, ['A', 'B', 'C', 'D'])

        scores = [100, 100, 100]
        grades = calculate_grades(scores)
        self.assertEqual(grades, ['A', 'A', 'A'])


class TestRecordScores(unittest.TestCase):
    def setUp(self):
        """Set up a temporary CSV file for testing."""
        self.csv_file = get_csv_path()
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def tearDown(self):
        """Clean up the temporary CSV file."""
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)

    def test_record_scores(self):
        """Test that scores and grades are recorded correctly in the CSV file."""
        student_name = "John Doe"
        scores = [95, 85]
        grades = ['A', 'B']
        record_scores(student_name, scores, grades)

        # Check that the CSV file exists and has the correct content
        self.assertTrue(os.path.exists(self.csv_file))

        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Check headers
        expected_headers = ['Student Name', 'Test 1', 'Test 2', 'Test 3', 'Test 4', 'Average', 'Best Grade']
        self.assertEqual(rows[0], expected_headers)

        # Check student data
        expected_row = ['John Doe', '95', '85', 'NA', 'NA', 'Avg: 90.00', 'A']
        self.assertEqual(rows[1], expected_row)

    def test_record_multiple_scores(self):
        """Test recording multiple students' scores."""
        record_scores("Alice", [100, 90], ['A', 'B'])
        record_scores("Bob", [70, 80], ['C', 'B'])

        with open(self.csv_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # Check the second student's data
        expected_row = ['Bob', '70', '80', 'NA', 'NA', 'Avg: 75.00', 'B']
        self.assertEqual(rows[2], expected_row)


if __name__ == "__main__":
    unittest.main()
