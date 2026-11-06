import json
from pathlib import Path
from langchain.tools import tool

RESTAURANTS_FILE = Path(__file__).parent/'restaurants.json'

def get_restaurants():
    return json.loads(RESTAURANTS_FILE.read_text(encoding='utf-8'))

@tool
def search_particular_restaurant(keyword : str) -> str:
    """Search restaurant by its name or its cuisine type"""
    restaurants = get_restaurants()
    matches = [ r for r in restaurants
                if (keyword.lower() in r['cuisine'].lower()) or(
                keyword.lower() in r['name'].lower()
                )]
    return json.dumps(matches)

@tool
def calculate_dining_cost(
        restaurant_id : str,
        participants : int
) -> str:
    """Calculate the total dining cost for a restaurant based on its participant count"""
    if participants < 1 or participants > 30:
        return "Participant count must be between 1 and 30."

    for res in get_restaurants():
        if res["id"] == restaurant_id:
            if res["available_seats"] >= participants:
                total = res["price_per_person"]*participants
                return json.dumps({
                    "restaurant" : res["name"],
                    "participants" : participants,
                    "total_fee" : total

                })
            else:
                return "Restaurant don't have enough available seats."
    return "Restaurant not found."

if __name__ == '__main__':
    print(search_particular_restaurant.invoke({"keyword" : "Ivy"}))
    print(calculate_dining_cost.invoke({"restaurant_id" : "R330" ,
                                        "participants" : 3 }))
