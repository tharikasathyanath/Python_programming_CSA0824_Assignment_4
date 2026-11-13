
from reader import read_attendance
from stats import percentage
from report import write_report

if __name__ == "__main__":
    records = read_attendance("attendance.txt")
    data = percentage(records)
    write_report(data)
    print(data)
