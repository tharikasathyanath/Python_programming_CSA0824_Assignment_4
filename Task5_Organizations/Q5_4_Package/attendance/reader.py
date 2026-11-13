
def read_attendance(filename):
    records = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(",")

            if len(parts) == 2 and parts[1] in ("P", "A"):
                records.append((parts[0], parts[1]))

    return records
