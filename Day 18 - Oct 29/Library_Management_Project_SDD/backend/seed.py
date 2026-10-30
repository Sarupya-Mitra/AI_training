import getpass
import sys

from sqlalchemy import select

from app.database import SessionLocal
from app.models import Book, InventoryEvent, User
from app.security import hash_password

LIBRARIAN_EMAIL = "admin@lib.sample.com"

# isbn, title, author, publisher, category, year, copies
BOOKS = [
    ("9780134494166", "Clean Architecture", "Robert C. Martin", "Pearson", "Software", 2017, 3),
    ("9780132350884", "Clean Code", "Robert C. Martin", "Prentice Hall", "Software", 2008, 2),
    ("9780201633610", "Design Patterns", "Erich Gamma et al.", "Addison-Wesley", "Software", 1994, 1),
    ("9780141439518", "Pride and Prejudice", "Jane Austen", "Penguin", "Fiction", 1813, 2),
    ("9780061120084", "To Kill a Mockingbird", "Harper Lee", "Harper", "Fiction", 1960, 4),
    ("9780451524935", "Nineteen Eighty-Four", "George Orwell", "Signet", "Fiction", 1949, 1),
]


def main():
    password = getpass.getpass(f"Password for {LIBRARIAN_EMAIL} (12-128 chars): ")
    if not 12 <= len(password) <= 128:
        sys.exit("Password must be 12-128 characters.")

    with SessionLocal() as db:
        librarian = db.scalar(select(User).where(User.email == LIBRARIAN_EMAIL))
        if librarian is None:
            librarian = User(
                full_name="Head Librarian",
                email=LIBRARIAN_EMAIL,
                role="Librarian",
                password_hash=hash_password(password),
                must_change_password=False,
            )
            db.add(librarian)
            db.flush()
            print("Created librarian", LIBRARIAN_EMAIL)

        for isbn, title, author, publisher, category, year, copies in BOOKS:
            if db.scalar(select(Book).where(Book.isbn == isbn)):
                continue
            book = Book(
                isbn=isbn, title=title, author=author, publisher=publisher,
                category=category, publication_year=year,
                total_copies=copies, available_copies=copies,
                created_by=librarian.id,
            )
            db.add(book)
            db.flush()
            db.add(InventoryEvent(
                book_id=book.id, event_type="Added", quantity_delta=copies,
                available_after=copies, actor_id=librarian.id,
            ))
            print("Added book", title)
        db.commit()


if __name__ == "__main__":
    main()