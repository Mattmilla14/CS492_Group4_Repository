# This file sets up our database and adds sample data
# Now it creates both books and users

# Import our database models
from models import db, Book, User, Sale, SaleItem
from datetime import date

def init_database(app):
    """
    This function sets up our database and adds sample data
    Now it creates both books and users with authentication
    """
    with app.app_context():
        
        # Create all the database tables
        # This creates both 'books' and 'users' tables
        db.create_all()
        
        # Add sample users if they don't exist
        if User.query.first() is None:
            print("Creating sample users...")
            
            # Create an admin user
            admin_user = User(
                username='admin',
                email='admin@bookstore.com',
                role='admin'
            )
            admin_user.set_password('admin123')  # This gets encrypted automatically
            
            # Create a regular user
            regular_user = User(
                username='user',
                email='user@bookstore.com',
                role='user'
            )
            regular_user.set_password('user123')  # This gets encrypted automatically
            
            # Add users to database
            db.session.add(admin_user)
            db.session.add(regular_user)
            db.session.commit()
            
            print("Sample users created!")
            print("Admin login: admin / admin123")
            print("User login: user / user123")
        
        # Add sample books if they don't exist (same as before)
        if Book.query.first() is None:
            print("Creating sample books...")
            
            sample_books = [
                Book(
                    title="The Great Gatsby",
                    author="F. Scott Fitzgerald",
                    isbn="9780743273565",
                    price=12.99,
                    description="A classic American novel set in the Jazz Age",
                    genre="Fiction",
                    publication_date=date(1925, 4, 10),
                    stock_quantity=50
                ),
                Book(
                    title="To Kill a Mockingbird",
                    author="Harper Lee",
                    isbn="9780061120084",
                    price=14.99,
                    description="A gripping tale of racial injustice and childhood innocence",
                    genre="Fiction",
                    publication_date=date(1960, 7, 11),
                    stock_quantity=30
                ),
                Book(
                    title="1984",
                    author="George Orwell",
                    isbn="9780451524935",
                    price=13.99,
                    description="A dystopian social science fiction novel",
                    genre="Science Fiction",
                    publication_date=date(1949, 6, 8),
                    stock_quantity=25
                )
            ]
            
            # Add books to database
            for book in sample_books:
                db.session.add(book)
            
            db.session.commit()
            print("Sample books created!")