# TASK 2 - Biometric Attendance Processing

import os
from pathlib import Path


def process_attendance(folder):

    attendance = {}
    errors = []

    files = sorted(Path(folder).glob("*.txt"))

    if not files:
        print("No attendance files found")
        return

    for filename in files:

        with open(filename, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                try:
                    parts = line.strip().split(",")

                    if len(parts) != 3:
                        raise ValueError("Invalid number of fields")

                    reg_no, date, status = parts

                    if status not in ("P", "A"):
                        raise ValueError("Invalid attendance status")

                    if not reg_no or not date:
                        raise ValueError("Missing information")

                    if reg_no not in attendance:
                        attendance[reg_no] = {
                            "present": 0,
                            "absent": 0
                        }

                    if status == "P":
                        attendance[reg_no]["present"] += 1
                    else:
                        attendance[reg_no]["absent"] += 1

                except ValueError as error:
                    errors.append(
                        f"{filename.name}, Line {line_number}: {error}"
                    )

    # Generate attendance report
    with open("attendance_report.txt", "w", encoding="utf-8") as file:

        file.write("ATTENDANCE REPORT\n\n")

        for reg_no, data in attendance.items():

            total = data["present"] + data["absent"]

            percentage = (
                data["present"] / total * 100
                if total > 0 else 0
            )

            file.write(
                f"{reg_no}: {percentage:.2f}%\n"
            )

            if percentage < 75:
                file.write("Below 75% Attendance\n")

            file.write("\n")

    # Generate error log
    with open("attendance_errors.txt", "w", encoding="utf-8") as file:

        for error in errors:
            file.write(error + "\n")

    print("Attendance Report Created Successfully")

    print("\nAttendance Summary:")

    for reg_no, data in attendance.items():

        total = data["present"] + data["absent"]

        percentage = (
            data["present"] / total * 100
            if total else 0
        )

        print(reg_no, ":", round(percentage, 2), "%")

    print("\nDamaged Lines:", errors)


# Create sample attendance folder
os.makedirs("attendance_files", exist_ok=True)

# Create sample files
with open("attendance_files/day1.txt", "w", encoding="utf-8") as file:
    file.write(
        "192311001,2026-11-01,P\n"
        "192311002,2026-11-01,A\n"
        "192311003,2026-11-01,P\n"
    )

with open("attendance_files/day2.txt", "w", encoding="utf-8") as file:
    file.write(
        "192311001,2026-11-02,P\n"
        "192311002,2026-11-02,P\n"
        "192311003,2026-11-02,A\n"
        "Invalid Line\n"
    )

# Run program
process_attendance("attendance_files")