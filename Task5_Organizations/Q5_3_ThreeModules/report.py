
def write_report(data):
    with open("attendance_report.txt", "w", encoding="utf-8") as file:
        for reg, percent in data.items():
            file.write(f"{reg}: {percent:.2f}%\\n")
