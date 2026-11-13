# TASK 6 - College Fest Registration Desk

import os
import re
import time


# Create input and output folders
os.makedirs("fest_input", exist_ok=True)
os.makedirs("fest_output", exist_ok=True)


# Sample department registration files
department_data = {

    "CSE.txt": [
        "192311001,Ravi,CSE,ravi@gmail.com,Music;Dance",
        "192311002,Priya,CSE,priya@gmail.com,Drama;Singing",
        "192311003,Arun,CSE,arun@gmail.com,Music;Coding"
    ],

    "IT.txt": [
        "192311004,Divya,IT,divya@gmail.com,Dance;Drama",
        "192311001,Ravi,CSE,ravi@gmail.com,Music;Dance"
    ],

    "ECE.txt": [
        "192311005,Kumar,ECE,kumar@gmail.com,Singing;Coding",
        "192311006,Meena,ECE,invalid-email,Music"
    ],

    "EEE.txt": [
        "192311007,Anu,EEE,anu@gmail.com,Dance;Singing",
        "Invalid Registration Line"
    ]

    # MECH.txt is intentionally missing for testing
}


# Create sample input files
for filename, records in department_data.items():

    with open(
        os.path.join("fest_input", filename),
        "w",
        encoding="utf-8"
    ) as file:

        for record in records:
            file.write(record + "\n")


# Validate email
def validate_email(email):

    email = email.strip()

    if " " in email:
        return False

    if email.count("@") != 1:
        return False

    name, domain = email.split("@")

    if not name or "." not in domain:
        return False

    if domain.startswith(".") or domain.endswith("."):
        return False

    return True


# Process registrations
def process_registrations():

    master = {}
    seen = set()
    events = {}
    errors = []

    departments = [
        "CSE.txt",
        "IT.txt",
        "ECE.txt",
        "EEE.txt",
        "MECH.txt"
    ]

    for filename in departments:

        filepath = os.path.join("fest_input", filename)

        try:

            with open(filepath, "r", encoding="utf-8") as file:

                for line_number, line in enumerate(file, start=1):

                    try:

                        parts = line.strip().split(",")

                        if len(parts) != 5:
                            raise ValueError(
                                "Invalid number of fields"
                            )

                        reg, name, dept, email, event_text = parts

                        if not reg or not name or not dept:
                            raise ValueError(
                                "Missing student details"
                            )

                        if not validate_email(email):
                            raise ValueError(
                                "Invalid email address"
                            )

                        if reg in seen:

                            errors.append(
                                f"{filename}, Line {line_number}: "
                                f"Duplicate registration {reg}"
                            )

                            continue

                        seen.add(reg)

                        chosen_events = [
                            event.strip()
                            for event in event_text.split(";")
                            if event.strip()
                        ]

                        master[reg] = {
                            "name": name,
                            "department": dept,
                            "email": email,
                            "events": chosen_events
                        }

                        for event in chosen_events:

                            events.setdefault(
                                event, []
                            ).append(reg)

                    except ValueError as error:

                        errors.append(
                            f"{filename}, Line {line_number}: {error}"
                        )

        except FileNotFoundError:

            errors.append(
                f"{filename}: Department file missing"
            )

        except PermissionError:

            errors.append(
                f"{filename}: Permission denied"
            )

        except UnicodeDecodeError:

            errors.append(
                f"{filename}: Invalid file encoding"
            )

    # Write master list
    with open(
        "fest_output/master_list.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("COLLEGE FEST MASTER LIST\n\n")

        for reg, details in master.items():

            file.write(
                f"Register Number: {reg}\n"
            )

            file.write(
                f"Name: {details['name']}\n"
            )

            file.write(
                f"Department: {details['department']}\n"
            )

            file.write(
                f"Email: {details['email']}\n"
            )

            file.write(
                f"Events: {', '.join(details['events'])}\n\n"
            )

    # Write event-wise participant files
    for event, participants in events.items():

        filename = (
            "fest_output/"
            + event.replace(" ", "_")
            + "_participants.txt"
        )

        with open(filename, "w", encoding="utf-8") as file:

            file.write(event + " PARTICIPANTS\n\n")

            for reg in participants:
                file.write(reg + "\n")

    # Write summary report
    with open(
        "fest_output/summary_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write("COLLEGE FEST SUMMARY\n\n")

        file.write(
            "Total Unique Students: "
            + str(len(master))
            + "\n\n"
        )

        file.write("Event-wise Participants:\n")

        for event, participants in events.items():

            file.write(
                event + ": " + str(len(participants)) + "\n"
            )

    # Write error log
    with open(
        "fest_output/error_log.txt",
        "w",
        encoding="utf-8"
    ) as file:

        for error in errors:
            file.write(error + "\n")

    # Display results
    print("COLLEGE FEST REGISTRATION SYSTEM")
    print("--------------------------------")

    print("\nTotal Unique Registrations:", len(master))

    print("\nMASTER LIST")

    for reg, details in master.items():

        print(
            reg,
            details["name"],
            details["department"],
            details["email"]
        )

    print("\nEVENT PARTICIPANTS")

    for event, participants in events.items():

        print(event, ":", participants)

    print("\nERROR LOG")

    for error in errors:
        print(error)

    print("\nAll output files created successfully!")


# Execute program
start = time.perf_counter()

process_registrations()

end = time.perf_counter()

print("\nExecution Time:", end - start, "seconds")