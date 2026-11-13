# TASK 1 - File Processing Design Review

from decimal import Decimal, InvalidOperation
from pathlib import Path


def calculate_mess_bill(filename):

    total = Decimal("0.00")
    report = []
    rejected = []

    try:
        with open(filename, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    parts = line.strip().split(",")

                    if len(parts) != 3:
                        raise ValueError("Expected 3 fields")

                    reg_no = parts[0].strip()
                    name = parts[1].strip()
                    amount = Decimal(parts[2].strip())

                    if not reg_no or not name:
                        raise ValueError("Missing register number or name")

                    if amount < 0:
                        raise ValueError("Negative amount")

                    total += amount
                    report.append(f"{name} {amount:.2f}")

                except (ValueError, InvalidOperation) as error:
                    rejected.append(
                        (line_number, line.strip(), str(error))
                    )

        print("MESS BILL REPORT")

        for item in report:
            print(item)

        print("\nTotal Mess Bill:", total)

        print("\nRejected Lines:")

        for item in rejected:
            print(item)

    except FileNotFoundError:
        print("Error: File not found:", filename)

    except PermissionError:
        print("Error: Permission denied")


# Create sample input file
sample_data = """192311001,Ravi,1250.50
192311002,Priya,1500.00
192311003,Arun,1200
192311004,Divya,invalid
192311005,Kumar,1300.75
192311006,InvalidLine
"""

with open("mess_oct.txt", "w", encoding="utf-8") as file:
    file.write(sample_data)

# Execute
calculate_mess_bill("mess_oct.txt")