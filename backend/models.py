# This file defines what our database tables look like
# Now we have both Books and Users for authentication

# Import the tools we need
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import jwt
import secrets
from flask import current_app

# Create database and encryption objects
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    """
    User model for authentication and authorization
    This stores information about people who can log into our system
    """
    __tablename__ = 'users'
    
    # Basic user information
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # Password hash - we NEVER store actual passwords!
    # bcrypt encrypts the password so it's secure
    password_hash = db.Column(db.String(128), nullable=False)
    
    # User role - determines what they can do
    # 'admin' can do everything, 'user' has limited access
    role = db.Column(db.String(20), default='user')
    
    # When this user account was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """
        This function takes a plain text password and encrypts it
        We use bcrypt to make it secure - even if someone steals our database,
        they can't see the actual passwords
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """
        This function checks if a password is correct
        It compares the encrypted version with what the user typed
        """
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def generate_token(self):
        """
        This creates a JWT token for the user after they log in
        The token contains the user's ID and expires after 24 hours
        Think of it like a temporary access card
        """
        try:
            print(f"Starting token generation for user: {self.username}")
            
            # Create the token payload (data inside the token)
            payload = {
                'user_id': self.id,
                'username': self.username,
                'role': self.role,
                'exp': datetime.utcnow() + timedelta(hours=24)  # Expires in 24 hours
            }
            
            print(f"Token payload created: {payload}")
            
            # Get the secret key from app config
            secret_key = current_app.config.get('JWT_SECRET_KEY')
            print(f"JWT Secret Key exists: {secret_key is not None}")
            print(f"JWT Secret Key value: {secret_key}")
            
            if not secret_key:
                print("ERROR: JWT_SECRET_KEY is missing from app config!")
                return None
            
            # Encrypt the token using our secret key
            token = jwt.encode(
                payload,
                secret_key,
                algorithm='HS256'
            )
            
            print(f"Token generated successfully: {type(token)}")
            print(f"Token value: {token}")
            
            return token
            
        except Exception as e:
            print(f"ERROR in token generation: {str(e)}")
            print(f"Exception type: {type(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def verify_token(token):
        """
        This function checks if a token is valid and returns the user
        It's like checking if an access card is real and not expired
        """
        try:
            # Decrypt the token using our secret key
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256']
            )
            
            # Get the user from the database
            user = User.query.get(payload['user_id'])
            return user
            
        except jwt.ExpiredSignatureError:
            # Token has expired
            print("Token has expired")
            return None
        except jwt.InvalidTokenError:
            # Token is invalid
            print("Token is invalid")
            return None
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None
    
    def to_dict(self):
        """Convert user object to dictionary (but don't include password!)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

class Book(db.Model):
    """
    Book model for the bookstore database
    This is the same as before - no changes needed
    """
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    publication_date = db.Column(db.Date)
    stock_quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert book object to dictionary for JSON response"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'price': self.price,
            'description': self.description,
            'genre': self.genre,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'stock_quantity': self.stock_quantity,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'

class Sale(db.Model):
    """
    Sale model for recording completed transactions
    Stores information about each sale including customer details and items purchased
    """
    __tablename__ = 'sales'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_email = db.Column(db.String(120), nullable=True)  # For guest checkout
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # For logged-in users
    total_amount = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='completed')  # completed, pending, cancelled
    
    # Relationship to user
    user = db.relationship('User', backref=db.backref('sales', lazy=True))
    
    def to_dict(self):
        """Convert sale object to dictionary for JSON response"""
        return {
            'id': self.id,
            'customer_email': self.customer_email,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'sale_date': self.sale_date.isoformat(),
            'status': self.status,
            'user': self.user.to_dict() if self.user else None
        }
    
    def __repr__(self):
        return f'<Sale {self.id} - ${self.total_amount}>'

class SaleItem(db.Model):
    """
    SaleItem model for storing individual items in each sale
    This creates a many-to-many relationship between Sales and Books
    """
    __tablename__ = 'sale_items'
    
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price_at_time = db.Column(db.Float, nullable=False)  # Store price at time of sale
    
    # Relationships
    sale = db.relationship('Sale', backref=db.backref('items', lazy=True, cascade='all, delete-orphan'))
    book = db.relationship('Book', backref=db.backref('sale_items', lazy=True))
    
    def to_dict(self):
        """Convert sale item object to dictionary for JSON response"""
        return {
            'id': self.id,
            'sale_id': self.sale_id,
            'book_id': self.book_id,
            'quantity': self.quantity,
            'price_at_time': self.price_at_time,
            'book': self.book.to_dict() if self.book else None
        }
    
    def __repr__(self):
        return f'<SaleItem {self.id} - Book {self.book_id} x{self.quantity}>'
# --- Notifications -----------------------------------------------------------
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)  # 'LOW_STOCK', 'OUT_OF_STOCK', etc.
    message = db.Column(db.Text, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    seen_at = db.Column(db.DateTime, nullable=True)

    book = db.relationship('Book', backref=db.backref('notifications', lazy=True))
    sale = db.relationship('Sale', backref=db.backref('notifications', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'message': self.message,
            'book_id': self.book_id,
            'sale_id': self.sale_id,
            'created_at': self.created_at.isoformat(),
            'seen_at': self.seen_at.isoformat() if self.seen_at else None
        }

# --- Password Reset Tokens ---------------------------------------------------
class PasswordReset(db.Model):
    __tablename__ = 'password_resets'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)

    def is_valid(self):
        return self.used_at is None and datetime.utcnow() < self.expires_at
