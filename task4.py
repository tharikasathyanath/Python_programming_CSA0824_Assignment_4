# TASK 4 - File and Exception Forensics

import os


# Repaired save_returns function
def save_returns(books):

    try:
        with open("returns.log", "a", encoding="utf-8") as log:

            for book in books:
                log.write(book + "\n")

    except OSError as error:

        with open("error.log", "a", encoding="utf-8") as error_file:
            error_file.write(str(error) + "\n")


# Process daily file
def process(day_file):

    try:
        with open(day_file, "r", encoding="utf-8") as file:
            books = [
                line.strip()
                for line in file
                if line.strip()
            ]

        save_returns(books)

        print(day_file, "processed successfully")

    except FileNotFoundError as error:

        print("Missing file:", day_file)

        with open("error.log", "a", encoding="utf-8") as error_file:
            error_file.write(str(error) + "\n")

    except PermissionError as error:

        with open("error.log", "a", encoding="utf-8") as error_file:
            error_file.write(str(error) + "\n")


# Create three daily files
daily_files = {
    "day1.txt": ["Python Book", "Java Book"],
    "day2.txt": ["C Book", "Data Science Book"],
    "day3.txt": ["AI Book", "Networking Book"]
}

for filename, books in daily_files.items():

    with open(filename, "w", encoding="utf-8") as file:

        for book in books:
            file.write(book + "\n")


# Clear old logs for testing
for filename in ["returns.log", "error.log"]:

    if os.path.exists(filename):
        os.remove(filename)


# Process all three days
process("day1.txt")
process("day2.txt")
process("day3.txt")

# Display final log
print("\nFINAL BOOK RETURN LOG")

with open("returns.log", "r", encoding="utf-8") as file:
    print(file.read())


# Missing file demonstration
print("MISSING FILE TEST")

process("day4.txt")

# Display error log
print("\nERROR LOG")

if os.path.exists("error.log"):

    with open("error.log", "r", encoding="utf-8") as file:
        print(file.read())