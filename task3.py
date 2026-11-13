# TASK 3 - Exception Handling in Attendance Processor

import os
import tempfile


class InvalidRecord(Exception):
    """Raised when attendance record is invalid."""


# TODO 1 - Parse attendance line
def parse_line(line):

    parts = line.strip().split(",")

    if len(parts) != 3:
        raise InvalidRecord(
            f"expected 3 fields, found {len(parts)}"
        )

    reg_no, date, status = parts

    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")

    return reg_no, date, status


# TODO 2 - Summarise attendance file
def summarise(path):

    present = 0
    absent = 0
    errors = []

    try:
        with open(path, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):

                if not line.strip():
                    continue

                try:
                    reg_no, date, status = parse_line(line)

                    if status == "P":
                        present += 1
                    else:
                        absent += 1

                except InvalidRecord as error:
                    errors.append((line_number, str(error)))

        return present, absent, errors

    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Attendance file not found: {path}"
        ) from error

    except PermissionError as error:
        raise PermissionError(
            f"Cannot access file: {path}"
        ) from error

    except UnicodeDecodeError as error:
        raise ValueError(
            "File contains invalid encoding"
        ) from error

    finally:
        print("File processing completed")


# Create sample attendance file
data = (
    "192311001,2026-10-08,P\n"
    "192311002,2026-10-08,A\n"
    "192311003,2026-10-08\n"
    "192311004,2026-10-08,L\n"
)

with tempfile.NamedTemporaryFile(
    "w",
    suffix=".csv",
    delete=False,
    encoding="utf-8"
) as tmp:

    tmp.write(data)
    filename = tmp.name


# Execute
try:
    result = summarise(filename)
    print(result)

except (FileNotFoundError, PermissionError, ValueError) as error:
    print("Error:", error)

finally:
    if os.path.exists(filename):
        os.remove(filename)


# Test missing file
print("\nMissing File Test")

try:
    summarise("missing_attendance.csv")

except FileNotFoundError as error:
    print("Handled:", error)