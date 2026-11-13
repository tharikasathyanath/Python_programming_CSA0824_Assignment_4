
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
            file.write(f"{reg}: {percent:.2f}%\\n")


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
