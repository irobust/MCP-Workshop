from fastmcp import FastMCP

from data import employees

resources_server = FastMCP(name="CorporateResources")


@resources_server.resource(
    "corporate://holidays/2025",
    description="Provides a list of official company holidays for the year 2025.",
)
def company_holidays():
    """Returns a list of company holiday dates."""
    return [
        "2025-01-01",  # New Year's Day
        "2025-07-04",  # Independence Day
        "2025-12-25",  # Christmas Day
    ]


@resources_server.resource(
    "corporate://employees/{employee_id}",
    description="Fetches employee details for a given employee ID.",
)
def get_employee_details(employee_id: str):
    """Looks up an employee by their ID and returns their details."""
    return employees.get(employee_id, {"error": "Employee not found"})

