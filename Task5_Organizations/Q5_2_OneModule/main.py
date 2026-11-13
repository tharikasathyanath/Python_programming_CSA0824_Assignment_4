
from attendance_module import *

if __name__ == "__main__":
    records = read_attendance("attendance.txt")
    data = percentage(records)
    write_report(data)
    print(data)
