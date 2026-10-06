import json
import os
import shutil

DATABASE_FILE = "users.json"
DOCUMENT_FOLDER = "documents"

REQUIRED_DOCUMENTS = [
    "Valid ID",
    "Police Clearance",
    "Medical Clearance",
    "Tax Form"
]

def load_database():
    if not os.path.exists(DATABASE_FILE):
        return {}

    try:
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_database():
    with open(DATABASE_FILE, "w") as file:
        json.dump(employees, file, indent=4)


employees = load_database()


if not os.path.exists(DOCUMENT_FOLDER):
    os.makedirs(DOCUMENT_FOLDER)


def add_employee():
    print("\n========== ADD EMPLOYEE ==========")

    employee_id = input("Enter Employee ID: ").strip()

    if employee_id in employees:
        print("Employee ID already exists.")
        return

    name = input("Enter employee name: ").strip()
    position = input("Enter position: ").strip()
    department = input("Enter department: ").strip()

    employees[employee_id] = {
        "name": name,
        "position": position,
        "department": department,
        "documents": {},
        "onboarding_status": "Incomplete"
    }

    for document in REQUIRED_DOCUMENTS:
        employees[employee_id]["documents"][document] = {
            "file": "",
            "status": "Missing",
            "remarks": ""
        }

    save_database()

    print("\nEmployee successfully added!")
    print("Employee ID:", employee_id)


def view_employees():
    print("\n========== EMPLOYEE LIST ==========")

    if not employees:
        print("No employees found.")
        return

    for employee_id, employee in employees.items():
        print("\nEmployee ID :", employee_id)
        print("Name        :", employee["name"])
        print("Position    :", employee["position"])
        print("Department  :", employee["department"])
        print("Status      :", employee["onboarding_status"])


def view_employee():
    print("\n========== EMPLOYEE DETAILS ==========")

    employee_id = input("Enter Employee ID: ").strip()

    if employee_id not in employees:
        print("Employee not found.")
        return

    employee = employees[employee_id]

    print("\nEmployee ID :", employee_id)
    print("Name        :", employee["name"])
    print("Position    :", employee["position"])
    print("Department  :", employee["department"])

    print("\n----- DOCUMENT CHECKLIST -----")

    for document, information in employee["documents"].items():
        print("\nDocument:", document)
        print("File    :", information["file"] or "None")
        print("Status  :", information["status"])
        print("Remarks :", information["remarks"] or "None")


def upload_document():
    print("\n========== UPLOAD DOCUMENT ==========")

    employee_id = input("Enter Employee ID: ").strip()

    if employee_id not in employees:
        print("Employee not found.")
        return

    print("\nRequired Documents:")

    for number, document in enumerate(REQUIRED_DOCUMENTS, 1):
        print(f"{number}. {document}")

    try:
        choice = int(input("\nSelect document: "))
    except ValueError:
        print("Invalid choice.")
        return

    if choice < 1 or choice > len(REQUIRED_DOCUMENTS):
        print("Invalid document.")
        return

    document_name = REQUIRED_DOCUMENTS[choice - 1]

    source_file = input(
        "\nEnter the FULL PATH of the document file: "
    ).strip()

    # Remove quotation marks if user copied the path
    source_file = source_file.strip('"')

    if not os.path.isfile(source_file):
        print("File does not exist.")
        return

    employee_folder = os.path.join(
        DOCUMENT_FOLDER,
        employee_id
    )

    if not os.path.exists(employee_folder):
        os.makedirs(employee_folder)

    original_name = os.path.basename(source_file)

    destination_file = os.path.join(
        employee_folder,
        original_name
    )

    try:
        shutil.copy2(source_file, destination_file)
    except Exception as error:
        print("Could not upload file.")
        print("Error:", error)
        return

    employees[employee_id]["documents"][document_name] = {
        "file": destination_file,
        "status": "Pending",
        "remarks": ""
    }

    update_onboarding_status(employee_id)

    save_database()

    print("\nDocument uploaded successfully!")
    print("Document:", document_name)
    print("Status: Pending")


def verify_document():
    print("\n========== DOCUMENT VERIFICATION ==========")

    employee_id = input("Enter Employee ID: ").strip()

    if employee_id not in employees:
        print("Employee not found.")
        return

    employee = employees[employee_id]

    print("\nDocuments:")

    for number, document in enumerate(REQUIRED_DOCUMENTS, 1):
        information = employee["documents"][document]

        print(
            f"{number}. {document} "
            f"[{information['status']}]"
        )

    try:
        choice = int(input("\nSelect document: "))
    except ValueError:
        print("Invalid choice.")
        return

    if choice < 1 or choice > len(REQUIRED_DOCUMENTS):
        print("Invalid document.")
        return

    document_name = REQUIRED_DOCUMENTS[choice - 1]
    document = employee["documents"][document_name]

    if not document["file"]:
        print("\nThis document has not been uploaded.")
        return

    print("\nDocument:", document_name)
    print("File:", document["file"])
    print("Current Status:", document["status"])

    print("\n1. Approve")
    print("2. Request Revision")
    print("3. Cancel")

    action = input("\nSelect action: ").strip()

    if action == "1":

        document["status"] = "Approved"
        document["remarks"] = "Document approved by HR."

        print("\nDocument approved!")

    elif action == "2":

        remarks = input(
            "Enter reason for revision: "
        ).strip()

        document["status"] = "Revision Required"
        document["remarks"] = remarks

        print("\nRevision requested.")

    elif action == "3":

        print("Cancelled.")
        return

    else:

        print("Invalid choice.")
        return

    update_onboarding_status(employee_id)
    save_database()


def update_onboarding_status(employee_id):

    documents = employees[employee_id]["documents"]

    all_approved = True

    for document in REQUIRED_DOCUMENTS:

        if documents[document]["status"] != "Approved":
            all_approved = False
            break

    if all_approved:
        employees[employee_id]["onboarding_status"] = "Completed"
    else:
        employees[employee_id]["onboarding_status"] = "Incomplete"


def onboarding_checklist():

    print("\n========== ONBOARDING CHECKLIST ==========")

    employee_id = input("Enter Employee ID: ").strip()

    if employee_id not in employees:
        print("Employee not found.")
        return

    employee = employees[employee_id]

    print("\nEmployee:", employee["name"])

    completed = 0

    for document in REQUIRED_DOCUMENTS:

        status = employee["documents"][document]["status"]

        if status == "Approved":
            mark = "[DONE]"
            completed += 1

        elif status == "Pending":
            mark = "[PENDING]"

        elif status == "Revision Required":
            mark = "[REVISION]"

        else:
            mark = "[MISSING]"

        print(f"{mark} {document}")

    print(
        f"\nProgress: {completed}/{len(REQUIRED_DOCUMENTS)}"
    )

    if completed == len(REQUIRED_DOCUMENTS):
        print("Onboarding Status: COMPLETED")
    else:
        print("Onboarding Status: INCOMPLETE")


def search_employee():

    print("\n========== SEARCH EMPLOYEE ==========")

    search = input(
        "Enter employee name or ID: "
    ).strip().lower()

    found = False

    for employee_id, employee in employees.items():

        if (
            search in employee_id.lower()
            or search in employee["name"].lower()
        ):

            print("\nEmployee ID :", employee_id)
            print("Name        :", employee["name"])
            print("Position    :", employee["position"])
            print("Department  :", employee["department"])
            print("Status      :", employee["onboarding_status"])

            found = True

    if not found:
        print("No employee found.")


def delete_employee():

    print("\n========== DELETE EMPLOYEE ==========")

    employee_id = input("Enter Employee ID: ").strip()

    if employee_id not in employees:
        print("Employee not found.")
        return

    employee_name = employees[employee_id]["name"]

    confirmation = input(
        f"Delete {employee_name}? (yes/no): "
    ).lower()

    if confirmation == "yes":

        del employees[employee_id]

        employee_folder = os.path.join(
            DOCUMENT_FOLDER,
            employee_id
        )

        if os.path.exists(employee_folder):
            shutil.rmtree(employee_folder)

        save_database()

        print("Employee deleted.")

    else:
        print("Deletion cancelled.")


def main():

    while True:

        print("\n")
        print("==========================================")
        print(" EMPLOYEE ONBOARDING & DOCUMENT SYSTEM")
        print("==========================================")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. View Employee Details")
        print("4. Upload Document")
        print("5. Verify Document")
        print("6. Onboarding Checklist")
        print("7. Search Employee")
        print("8. Delete Employee")
        print("9. Exit")
        print("==========================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_employee()

        elif choice == "2":
            view_employees()

        elif choice == "3":
            view_employee()

        elif choice == "4":
            upload_document()

        elif choice == "5":
            verify_document()

        elif choice == "6":
            onboarding_checklist()

        elif choice == "7":
            search_employee()

        elif choice == "8":
            delete_employee()

        elif choice == "9":
            print("\nThank you for using the system!")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()