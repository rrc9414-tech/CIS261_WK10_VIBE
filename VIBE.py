#Robert Cooper
#CIS261
#WK10 Vibe Coding

"""Student Grade Calculator using Option A: a list of dictionaries."""

import os


FILE_NAME = "student_grades.txt"
ESC = "\x1b"


def calculate_average(test1, test2, test3):
	"""Return the average of three test scores."""
	return (test1 + test2 + test3) / 3


def calculate_grade(average):
	"""Return a letter grade based on an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def make_student(name, student_id, test1, test2, test3):
	"""Create a student dictionary with calculated fields."""
	average = calculate_average(test1, test2, test3)
	return {
		"name": name,
		"id": student_id,
		"test1": test1,
		"test2": test2,
		"test3": test3,
		"average": average,
		"grade": calculate_grade(average),
	}


def is_escape(value):
	"""Return True when the user entered the ESC key."""
	return value == ESC


def prompt_text(prompt):
	"""Prompt for text, returning None when ESC is pressed."""
	while True:
		value = input(prompt).strip()
		if is_escape(value):
			return None
		if value:
			return value
		print("This field cannot be blank.")


def prompt_score(prompt):
	"""Prompt for a score from 0 through 100, or return None for ESC."""
	while True:
		value = input(prompt).strip()
		if is_escape(value):
			return None
		try:
			score = float(value)
			if 0 <= score <= 100:
				return score
			print("Enter a score from 0 to 100.")
		except ValueError:
			print("Enter a numeric score, such as 87.5.")


def display_students(students):
	"""Display all student records in a formatted table."""
	if not students:
		print("No student records found.")
		return

	print("\n" + "=" * 69)
	print("ALL STUDENT RECORDS")
	print("=" * 69)
	print(
		f"{'Name':<18} {'ID':<10} {'Test 1':>7} {'Test 2':>7} "
		f"{'Test 3':>7} {'Average':>8} {'Grade':>5}"
	)
	print("-" * 69)
	for student in students:
		print(
			f"{student['name'][:18]:<18} {student['id'][:10]:<10} "
			f"{student['test1']:>7.2f} {student['test2']:>7.2f} "
			f"{student['test3']:>7.2f} {student['average']:>8.2f} "
			f"{student['grade']:>5}"
		)
	print("=" * 69)
	print(f"Total students: {len(students)}")


def display_statistics(students):
	"""Display class averages, named extremes, and grade distribution."""
	if not students:
		print("No student records available for statistics.")
		return

	averages = [student["average"] for student in students]
	highest = max(students, key=lambda student: student["average"])
	lowest = min(students, key=lambda student: student["average"])
	grade_counts = {}
	for student in students:
		grade = student["grade"]
		grade_counts[grade] = grade_counts.get(grade, 0) + 1

	print("\n" + "=" * 69)
	print("CLASS STATISTICS")
	print("=" * 69)
	print()
	print(f"Class Average: {sum(averages) / len(averages):.2f}")
	print(f"Highest Average: {highest['average']:.2f} ({highest['name']})")
	print(f"Lowest Average: {lowest['average']:.2f} ({lowest['name']})")
	print()
	print("Grade Distribution:")
	for grade, count in sorted(grade_counts.items(), key=lambda item: (-item[1], item[0])):
		print(f"    {grade}: {count} student(s)")


def add_student(students):
	"""Prompt for and append one student record."""
	print("\n" + "=" * 69)
	print("ADD NEW STUDENT")
	print("=" * 69)
	name = prompt_text("Enter student name: ")
	if name is None:
		print("Add cancelled.")
		return False
	student_id = prompt_text("Enter student ID: ")
	if student_id is None:
		print("Add cancelled.")
		return False
	test1 = prompt_score("Enter Test 1 score: ")
	if test1 is None:
		print("Add cancelled.")
		return False
	test2 = prompt_score("Enter Test 2 score: ")
	if test2 is None:
		print("Add cancelled.")
		return False
	test3 = prompt_score("Enter Test 3 score: ")
	if test3 is None:
		print("Add cancelled.")
		return False

	student = make_student(name, student_id, test1, test2, test3)
	students.append(student)
	print(f"\n✓ Added student: {name} (ID: {student_id})")
	print(f"     Average: {student['average']:.2f} | Grade: {student['grade']}")
	return True


def search_students(students):
	"""Display records whose names contain the search text."""
	search_term = prompt_text("Search name: ")
	if search_term is None:
		print("Search cancelled.")
		return

	matches = [
		student for student in students
		if search_term.casefold() in student["name"].casefold()
	]
	if matches:
		display_students(matches)
	else:
		print(f'No students found matching "{search_term}".')


def save_students(students):
	"""Save records in the required pipe-delimited format."""
	try:
		with open(FILE_NAME, "w", encoding="utf-8") as file:
			for student in students:
				file.write(
					f"{student['name']}|{student['id']}|{student['test1']:.2f}|"
					f"{student['test2']:.2f}|{student['test3']:.2f}|"
					f"{student['average']:.2f}|{student['grade']}\n"
				)
		print(f"Saved {len(students)} student record(s) to {FILE_NAME}.")
		return True
	except OSError as error:
		print(f"Could not save student records: {error}")
		return False


def load_students():
	"""Load records and skip malformed lines with a clear message."""
	students = []
	if not os.path.exists(FILE_NAME):
		return students

	try:
		with open(FILE_NAME, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				fields = line.rstrip("\n").split("|")
				if len(fields) != 7:
					print(f"Skipped invalid record on line {line_number}.")
					continue
				try:
					name, student_id = fields[0], fields[1]
					test1, test2, test3 = (
						float(fields[2]), float(fields[3]), float(fields[4])
					)
					scores = (test1, test2, test3)
					if not name or not student_id or not all(0 <= score <= 100 for score in scores):
						raise ValueError
					students.append(make_student(name, student_id, test1, test2, test3))
				except ValueError:
					print(f"Skipped invalid record on line {line_number}.")
		print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")
	except OSError as error:
		print(f"Could not load student records: {error}")
	return students


def show_menu():
	"""Display the main menu."""
	print("=" * 69)
	print("STUDENT GRADE CALCULATOR")
	print("=" * 69)
	print("1.  Add New Student")
	print("2.  Display All Students")
	print("3.  Search Student by Name")
	print("4.  View Class Statistics")
	print("5.  Save and Exit (or press ESC)")
	print("=" * 69)


def show_welcome():
	"""Display the welcome banner."""
	print("=" * 69)
	print("WELCOME TO STUDENT GRADE CALCULATOR")
	print("=" * 69)


def main():
	"""Run the Student Grade Calculator."""
	students = load_students()
	show_welcome()
	print()
	while True:
		show_menu()
		choice = input("Select an option (1-5) or press ESC to exit: ").strip()
		if is_escape(choice):
			save_students(students)
			print("Goodbye.")
			return
		if choice == "1":
			if add_student(students):
				save_students(students)
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			search_students(students)
		elif choice == "4":
			display_statistics(students)
		elif choice == "5":
			save_students(students)
		else:
			print("Please select an option from 1 to 5, or press ESC to exit.")


if __name__ == "__main__":
	main()

