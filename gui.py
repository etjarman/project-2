import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from determine_grade import calculate_grades, determine_grade, record_scores, get_csv_path
import os
import subprocess
from typing import Optional


class GradeCalculatorApp:
    """
    A graphical user interface (GUI) for calculating grades.
    Allows users to input a student's name, number of test scores, and the test scores themselves.
    """
    ADMIN_PASSWORD: str = "admin123"  # Replace with a more secure password in production

    def __init__(self, root: tk.Tk):
        """
        Initialize the Grade Calculator application.
        """
        self.root: tk.Tk = root

        # GUI Components
        self.student_name_entry: tk.Entry
        self.num_scores_var: tk.StringVar
        self.num_scores_dropdown: ttk.Combobox
        self.scores_frame: tk.Frame
        self.score_entries: list[tk.Entry] = []
        self.message_label: tk.Label

        # Set up the GUI
        self.root.title("Grade Calculator")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        # Student Name Entry
        tk.Label(root, text="Student Name:").pack(pady=5)
        self.student_name_entry = tk.Entry(root, width=30)
        self.student_name_entry.pack(pady=5)

        # Number of Test Scores Dropdown
        tk.Label(root, text="Number of Test Scores:").pack(pady=5)
        self.num_scores_var = tk.StringVar()
        self.num_scores_dropdown = ttk.Combobox(
            root, textvariable=self.num_scores_var, state="readonly", width=10
        )
        self.num_scores_dropdown['values'] = ['1', '2', '3', '4']
        self.num_scores_dropdown.pack(pady=5)
        self.num_scores_dropdown.bind("<<ComboboxSelected>>", self.create_score_fields)

        # Frame for dynamically generated score fields
        self.scores_frame = tk.Frame(root)
        self.scores_frame.pack(pady=10)

        # Buttons
        self.submit_button = tk.Button(root, text="Calculate Grades", command=self.calculate_grades)
        self.submit_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Data", command=self.view_csv)
        self.view_button.pack(pady=5)

        self.clear_button = tk.Button(root, text="Clear Data", command=self.clear_csv)
        self.clear_button.pack(pady=5)

        # Message Label
        self.message_label = tk.Label(root, text="", font=("Arial", 10))
        self.message_label.pack(pady=5)

    def create_score_fields(self, event: Optional[tk.Event] = None) -> None:
        """
        Create input fields for the number of test scores selected in the dropdown.
        """
        # Clear any existing score fields
        for widget in self.scores_frame.winfo_children():
            widget.destroy()

        # Add new score fields with validation
        try:
            num_scores = int(self.num_scores_var.get())
        except ValueError:
            self.message_label.config(text="Invalid number of test scores selected.", fg="red")
            return

        tk.Label(self.scores_frame, text="Test Scores:").pack(side=tk.LEFT, padx=5)

        # Validation for positive integers
        validate_cmd = (self.root.register(self.validate_positive_integer), '%P')

        self.score_entries = []
        for _ in range(num_scores):
            entry = tk.Entry(self.scores_frame, validate="key", validatecommand=validate_cmd, width=5)
            entry.pack(side=tk.LEFT, padx=5)
            self.score_entries.append(entry)

    def validate_positive_integer(self, value: str) -> bool:
        """
        Validate that the input is a positive integer.
        """
        return value.isdigit() or value == ""

    def calculate_grades(self) -> None:
        """
        Calculate grades based on the entered scores and display the results.
        """
        student_name: str = self.student_name_entry.get().strip()
        if not student_name:
            self.message_label.config(text="Student name cannot be empty.", fg="red")
            return

        try:
            scores: list[int] = [int(entry.get()) for entry in self.score_entries if entry.get().strip()]
            if len(scores) != len(self.score_entries):
                self.message_label.config(text="Please fill in all score fields.", fg="red")
                return

            # Calculate grades
            grades: list[str] = calculate_grades(scores)

            # Calculate the average and best grade
            average_score: float = sum(scores) / len(scores)
            best_score: int = max(scores)
            best_grade: str = determine_grade(best_score)

            # Record scores and grades in CSV
            record_scores(student_name, scores, grades)

            # Display the average and best grade
            self.message_label.config(
                text=f"Average Score: {average_score:.2f}, Best Grade: {best_grade}",
                fg="green"
            )

        except ValueError:
            self.message_label.config(text="All test scores must be valid integers.", fg="red")

    def prompt_password(self) -> bool:
        """
        Prompt the user for the admin password.
        Password is set above the app init.
        """
        password: Optional[str] = simpledialog.askstring("Admin Access", "Enter Admin Password:", show='*')
        if password == self.ADMIN_PASSWORD:
            return True
        else:
            messagebox.showerror("Access Denied", "Incorrect password. Access denied.")
            return False

    def view_csv(self) -> None:
        """
        Open the CSV file in a default text editor (admin-protected).
        """
        if self.prompt_password():
            filepath: str = get_csv_path()
            if os.path.exists(filepath):
                subprocess.run(["notepad", filepath])  # Adjust for platform
            else:
                self.message_label.config(text="No data to display.", fg="red")

    def clear_csv(self) -> None:
        """
        Clear the contents of the CSV file (admin-protected).
        """
        if self.prompt_password():
            filepath: str = get_csv_path()
            if os.path.exists(filepath):
                os.remove(filepath)
                self.message_label.config(text="Data cleared successfully.", fg="green")
            else:
                self.message_label.config(text="No data to clear.", fg="red")


# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = GradeCalculatorApp(root)
    root.mainloop()
