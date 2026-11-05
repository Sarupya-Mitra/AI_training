import json
from pathlib import Path
from langchain.tools import tool


FILE = Path(__file__).parent/"workshops.json"
COUPON_FILE = Path(__file__).parent/"couponcodes.json"

def get_workshops():
    return json.loads(FILE.read_text(encoding="utf-8"))
def get_coupon_codes():
    return json.loads(COUPON_FILE.read_text(encoding="utf-8"))

# It is mandatory to have a docstring """<Description>""" for all the tools.
@tool
def search_workshops(keyword : str) -> str:
    """Search available workshops by title."""

    matches = [
        w for w in get_workshops()
        if keyword.lower() in w["title"].lower()
    ]

    return json.dumps(matches)

@tool
def calculate_workshop_fee(
    workshop_id: str,
    participants: int
) -> str:
    """Calculate the total fee for a workshop and participant count."""
    if participants < 1 or participants > 30:
        return "Participant count must be between 1 and 30."

    for workshop in get_workshops():

        if workshop["id"] == workshop_id:
            total = workshop["fee"] * participants

            return json.dumps({
                "workshop": workshop["title"],
                "participants": participants,
                "total_fee": total
            })

    return "Workshop not found."

@tool
def list_all_workshops() -> str:
    """Shows all the workshops."""
    workshops = get_workshops()
    return json.dumps(workshops)

@tool
def find_cheapest_workshop() -> str:
    """Finds the cheapest Workshop"""
    workshops = get_workshops()
    cheapest_workshop = min(workshops, key=lambda x:x["fee"])
    return json.dumps(cheapest_workshop)

@tool
def match_coupon_codes(user_code : str) -> str:
    """Match the user's coupon codes with the codes present in the file"""
    coupon_codes = get_coupon_codes()

    for code in coupon_codes:
        if str(user_code).strip().lower() == str(code.get('code')).strip().lower():
            return json.dumps(code)
    return "Coupon code not found."

if __name__ == "__main__":
    # In Langchain, you cannot call these tools directly like a function call in python
    # You need to use .invoke({}) and pass any arguments within {} to make it work.
    print(search_workshops.invoke({"keyword": "Python"}))

    print(calculate_workshop_fee.invoke({
        "workshop_id": "W101",
        "participants": 4
    }))

    print(list_all_workshops.invoke({}))

    print("\n Cheapest Workshop ", find_cheapest_workshop.invoke({}))
    print("\n Coupon Code : ", match_coupon_codes.invoke({"user_code" : "newuser10"}))