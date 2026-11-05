
import json
import re
from typing import Callable
from datetime import datetime, timezone

STOP_WORDS = {"the","an","a","and","with"}

def clean_the_words(text):
    # Just an NLP pre-processing step, where I get set of important words,
    # First I will find all sequences containing lowercase chars and nos
    # from the text, so that punctuations are eliminated.
    # Then subtract the stop words which hold no real meaning.
    # Output will be a set, e.g : Sentence = Python is a powerful language, with Python-like speed!
    # Output = {'python', 'powerful', 'language', 'like', 'speed'}
    return set(re.findall(r'[a-z0-9]+',text.lower())) - STOP_WORDS


def search_book(query: str) -> dict:
    from main import KNOWLEDGE_PATH
    books = json.load(open(KNOWLEDGE_PATH))
    ranked_outputs = []
    query_terms = clean_the_words(query)

    for book in books:
        title_terms = clean_the_words(book["title"])
        category_terms = clean_the_words(book["category"])
        author_terms = clean_the_words(book["author"])

        score = (
            3 * len(query_terms & title_terms ) +
            2 * len(query_terms & category_terms ) +
            len(query_terms & author_terms)
        )
        if score > 0:
            ranked_outputs.append((score,book))

    # Suppose scores are 5,10,20. We need the output with the highest score, so we sort using -scores
    # So the results will be (-20,..) , (-10,..) , (-5,..); by doing this we get the best top 2
    # results in the
    ranked_outputs.sort(key=lambda pair:(-pair[0],pair[1]["id"]))
    results = []
    for score,book in ranked_outputs[:2]:
        results.append({
            "id":book["id"],
            "title":book["title"],
            "author":book["author"],
            "category":book["category"],
            "available_copies":book["available_copies"],
        })

    return {
        "query":query,
        "results": results,
        "message": (
            "These are the top 2 keyword matches. Show these matches"
            if results else "No matching book found. Do not invent any troubleshooting steps."
        )
    }

def reserve_book(book_title : str,
                 user_name : str,
                 confirm : Callable[[str],bool] = input
                 ) -> dict :
    """Add a reservation in reservations.json, but only after explicit local confirmation."""
    from main import KNOWLEDGE_PATH,RESERVATIONS_PATH

    # 1. First search whether the book is available or not

    final_selected_books = {"books_selected" : []}
    books = json.loads(KNOWLEDGE_PATH.read_text(encoding="utf-8"))
    for book in books:
        if book["title"] == book_title:
            if book["available_copies"] > 0:
                final_selected_books["books_selected"].append(book)
    if not final_selected_books["books_selected"]:
        return {"created" : False , "reason" : "Book not found or Book is not available"}

    # 2. Get Approval

    print("\n --- RESERVATION APPROVAL REQUIRED ---")
    print("\n Book Title : ",book_title)
    print("\n User Name : ",user_name)
    approval = confirm("Create reservation for this book? (y/n): ").strip().lower()
    if approval not in {"y","yes"}:
        print("Reservation wasn't approved")
        return {"created" : False , "reason" : "User declined approval" }

    # 3 .Now it is approved, first task is to update the inventory
    for book in final_selected_books["books_selected"]:
        book["available_copies"] -= 1
    # In Python, when you do final_selected_books["books_sel"].append(book)
    # where book was in books.json, then the book inside final_selected_books
    # and the book at books.json, point to the same object in memory.
    # Hence updating one automatically changes the other.

    KNOWLEDGE_PATH.write_text(
        json.dumps(books, indent=4),
        encoding="utf-8"
    )

    # 4. Load the reservations dict and store the new reservation
    reservations = json.loads(RESERVATIONS_PATH.read_text(encoding="utf-8"))
    next_id = max(
        [int(reservation["id"].split("-")[-1]) for reservation in reservations] or [0]
    ) + 1
    reservation = {
        "id" : f"B-{next_id}",
        "book_title" : book_title,
        "user_name" : user_name,
        "created_at" : datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    reservations.append(reservation)
    RESERVATIONS_PATH.write_text(json.dumps(reservations), encoding="utf-8")
    return {"created" : True , "reservation" : reservation}

# if __name__ == "__main__":
#     query = input("Enter search query: ")
#     search_book(query)