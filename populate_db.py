from library_management_app import create_app
from library_management_app.extensions import db
from library_management_app.models import Book

app = create_app()

with app.app_context():
    db.create_all()

    books = [
        {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling"},
        {"title": "The Alchemist", "author": "Paulo Coelho"},
        {"title": "The Catcher in the Rye", "author": "J.D. Salinger"},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee"},
        {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
        {"title": "The Fault in Our Stars", "author": "John Green"},
        {"title": "1984", "author": "George Orwell"},
        {"title": "The Hunger Games", "author": "Suzanne Collins"},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
        {"title": "Five Point Someone", "author": "Chetan Bhagat"},
        {"title": "Midnight's Children", "author": "Salman Rushdie"},
        {"title": "The Immortals of Meluha", "author": "Amish Tripathi"},
        {"title": "2 States", "author": "Chetan Bhagat"},
        {"title": "The Guide", "author": "R.K. Narayan"},
        {"title": "My Family and Other Animals", "author": "Gerald Durrell"},
        {"title": "The Perks of Being a Wallflower", "author": "Stephen Chbosky"},
        {"title": "One Indian Girl", "author": "Chetan Bhagat"},
    ]

    for book_data in books:
        book = Book(title=book_data["title"], author=book_data["author"])
        db.session.add(book)

    db.session.commit()

    print("Database populated successfully!")
