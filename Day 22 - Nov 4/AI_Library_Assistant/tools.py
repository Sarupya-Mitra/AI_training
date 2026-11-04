
import json
import re

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


# if __name__ == "__main__":
#     query = input("Enter search query: ")
#     search_book(query)