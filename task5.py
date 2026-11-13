# TASK 5 - Organising Python Code Four Ways

from pathlib import Path

base = Path("Task5_Organizations")
base.mkdir(exist_ok=True)

# Common functions
common_code = '''
def read_attendance(filename):
    records = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")

            if len(parts) == 2 and parts[1] in ("P", "A"):
                records.append((parts[0], parts[1]))

    return records


def percentage(records):
    result = {}
    total = {}

    for reg, status in records:
        total[reg] = total.get(reg, 0) + 1
        result[reg] = result.get(reg, 0) + (status == "P")

    return {
        reg: result[reg] / total[reg] * 100
        for reg in total
    }


def write_report(data):
    with open("attendance_report.txt", "w", encoding="utf-8") as file:
        for reg, percent in data.items():
            file.write(f"{reg}: {percent:.2f}%\\\\n")


def absent_three_days(daily_records):
    result = []

    if len(daily_records) < 3:
        return result

    students = set(reg for reg, status in daily_records[0])

    for day in daily_records:
        absent = {
            reg for reg, status in day if status == "A"
        }
        students &= absent

    return sorted(students)
'''

# Organisation 1: One script
folder1 = base / "Q5_1_OneScript"
folder1.mkdir(exist_ok=True)

(folder1 / "attendance.py").write_text(
    common_code +
    '''
if __name__ == "__main__":
    records = read_attendance("attendance.txt")
    data = percentage(records)
    write_report(data)
    print(data)
''',
    encoding="utf-8"
)

# Organisation 2: One module and main script
folder2 = base / "Q5_2_OneModule"
folder2.mkdir(exist_ok=True)

(folder2 / "attendance_module.py").write_text(
    common_code,
    encoding="utf-8"
)

(folder2 / "main.py").write_text(
    '''
from attendance_module import *

if __name__ == "__main__":
    records = read_attendance("attendance.txt")
    data = percentage(records)
    write_report(data)
    print(data)
''',
    encoding="utf-8"
)

# Organisation 3: Three modules
folder3 = base / "Q5_3_ThreeModules"
folder3.mkdir(exist_ok=True)

(folder3 / "reader.py").write_text(
    '''
def read_attendance(filename):
    records = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")

            if len(parts) == 2 and parts[1] in ("P", "A"):
                records.append((parts[0], parts[1]))

    return records
''',
    encoding="utf-8"
)

(folder3 / "stats.py").write_text(
    '''
def percentage(records):
    result = {}
    total = {}

    for reg, status in records:
        total[reg] = total.get(reg, 0) + 1
        result[reg] = result.get(reg, 0) + (status == "P")

    return {
        reg: result[reg] / total[reg] * 100
        for reg in total
    }


def absent_three_days(daily_records):
    if len(daily_records) < 3:
        return []

    students = set(reg for reg, status in daily_records[0])

    for day in daily_records:
        students &= {
            reg for reg, status in day if status == "A"
        }

    return sorted(students)
''',
    encoding="utf-8"
)

(folder3 / "report.py").write_text(
    '''
def write_report(data):
    with open("attendance_report.txt", "w", encoding="utf-8") as file:
        for reg, percent in data.items():
            file.write(f"{reg}: {percent:.2f}%\\\\n")
''',
    encoding="utf-8"
)

(folder3 / "main.py").write_text(
    '''
from reader import read_attendance
from stats import percentage
from report import write_report

if __name__ == "__main__":
    records = read_attendance("attendance.txt")
    data = percentage(records)
    write_report(data)
    print(data)
''',
    encoding="utf-8"
)

# Organisation 4: Package
folder4 = base / "Q5_4_Package"
package = folder4 / "attendance"
package.mkdir(parents=True, exist_ok=True)

(package / "__init__.py").write_text(
    'from .reader import read_attendance\\n'
    'from .stats import percentage, absent_three_days\\n'
    'from .report import write_report\\n',
    encoding="utf-8"
)

(package / "reader.py").write_text(
    (folder3 / "reader.py").read_text(encoding="utf-8"),
    encoding="utf-8"
)

(package / "stats.py").write_text(
    (folder3 / "stats.py").read_text(encoding="utf-8"),
    encoding="utf-8"
)

(package / "report.py").write_text(
    (folder3 / "report.py").read_text(encoding="utf-8"),
    encoding="utf-8"
)

(folder4 / "main.py").write_text(
    '''
from attendance import read_attendance, percentage, write_report

if __name__ == "__main__":
    records = read_attendance("attendance.txt")
    data = percentage(records)
    write_report(data)
    print(data)
''',
    encoding="utf-8"
)

# Create sample attendance data in every folder
sample = (
    "192311001,P\\n"
    "192311002,A\\n"
    "192311003,P\\n"
    "192311004,A\\n"
)

for folder in [folder1, folder2, folder3, folder4]:

    (folder / "attendance.txt").write_text(
        sample,
        encoding="utf-8"
    )

print("FOUR ORGANISATIONS CREATED SUCCESSFULLY")

print("\n1. One Script:", folder1)
print("2. One Module:", folder2)
print("3. Three Modules:", folder3)
print("4. Package:", folder4)

print("\nRun the following files separately:")

print("1.", folder1 / "attendance.py")
print("2.", folder2 / "main.py")
print("3.", folder3 / "main.py")
print("4.", folder4 / "main.py")