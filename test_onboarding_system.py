from onboarding import OnboardingManager


def test_employee_can_submit_onboarding_with_documents():
    manager = OnboardingManager()
    employee_id = manager.create_employee(
        "Jane Doe",
        "jane@example.com",
        ["Identity Card", "Police Clearance"],
    )

    manager.submit_onboarding(employee_id, {"Identity Card": "id.pdf", "Police Clearance": "clearance.pdf"})

    employee = manager.get_employee(employee_id)
    assert employee["name"] == "Jane Doe"
    assert employee["status"] == "Document Review Pending"
    assert employee["documents"]["Identity Card"] == "id.pdf"
    assert employee["documents"]["Police Clearance"] == "clearance.pdf"


def test_hr_can_approve_or_request_revision():
    manager = OnboardingManager()
    employee_id = manager.create_employee("John Smith", "john@example.com", ["Passport", "NBI Clearance"])
    manager.submit_onboarding(employee_id, {"Passport": "passport.pdf", "NBI Clearance": "nbi.pdf"})

    manager.review_employee(employee_id, "approved")
    employee = manager.get_employee(employee_id)
    assert employee["status"] == "Approved"

    second_id = manager.create_employee("Mary Jones", "mary@example.com", ["ID", "Background Check"])
    manager.submit_onboarding(second_id, {"ID": "id.pdf", "Background Check": "bg.pdf"})
    manager.review_employee(second_id, "revision_requested", "Please upload a clearer ID scan.")
    employee = manager.get_employee(second_id)
    assert employee["status"] == "Revision Requested"
    assert employee["hr_note"] == "Please upload a clearer ID scan."
