
from attendance import read_attendance, percentage, write_report

if __name__ == "__main__":
    records = read_attendance("attendance.txt")
    data = percentage(records)
    write_report(data)
    print(data)
