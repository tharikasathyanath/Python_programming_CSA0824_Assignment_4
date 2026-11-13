
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
