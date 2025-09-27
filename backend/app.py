# This is the main file for our bookstore backend with JWT authentication
# Clean version that should fix the NameError

# Import all the tools we need
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, Book, User, Sale, SaleItem, bcrypt
from database import init_database
from auth import token_required, admin_required
from datetime import datetime, date
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create our Flask application - THIS MUST COME BEFORE @app.route decorators
app = Flask(__name__)

# Configure CORS
CORS(app)

# Configure our database and security
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "bookstore.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set secret keys from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key-for-development')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'fallback-jwt-key-for-development')

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Create the instance directory if it doesn't exist
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

# Initialize database with sample data
init_database(app)

# Serve frontend static files from the project Frontend/ directory.
# This lets you open the app at http://localhost:5000/ and have Flask
# serve the static HTML/CSS/JS files. It is placed after API routes so
# `/api/*` endpoints continue to work as defined above.
FRONTEND_DIR = os.path.abspath(os.path.join(basedir, '..', 'Frontend'))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    # Do not interfere with API routes (they are defined earlier and take precedence).
    # If the requested path exists in the Frontend folder, serve it; otherwise serve index.html.
    if path and os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')

# ===============================
# AUTHENTICATION ENDPOINTS
# ===============================

@app.route('/api/register', methods=['POST'])
def register():
    """POST /api/register - Create new user account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({
                'success': False,
                'error': 'Username already exists'
            }), 400
        
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'error': 'Email already exists'
            }), 400
        
        # Create new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            role=data.get('role', 'user')
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token for the new user
        token = new_user.generate_token()
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'token': token
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    """POST /api/login - User authentication with debug logging"""
    try:
        print("=== LOGIN ATTEMPT DEBUG ===")
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Validate required fields
        if not data.get('username') or not data.get('password'):
            print("ERROR: Missing username or password")
            return jsonify({
                'success': False,
                'error': 'Username and password are required'
            }), 400
        
        print(f"Looking for user: {data['username']}")
        
        # Find the user by username
        user = User.query.filter_by(username=data['username']).first()
        print(f"User found: {user}")
        
        if user:
            print("User exists, checking password...")
            password_valid = user.check_password(data['password'])
            print(f"Password valid: {password_valid}")
            
            if password_valid:
                print("Password correct, generating token...")
                # Generate a token for the user
                token = user.generate_token()
                print(f"Token generated: {token is not None}")
                
                if token:
                    print("SUCCESS: Login completed")
                    return jsonify({
                        'success': True,
                        'message': 'Login successful',
                        'user': user.to_dict(),
                        'token': token
                    }), 200
                else:
                    print("ERROR: Could not generate token")
                    return jsonify({
                        'success': False,
                        'error': 'Could not generate token'
                    }), 500
            else:
                print("ERROR: Invalid password")
        else:
            print("ERROR: User not found")
            
        return jsonify({
            'success': False,
            'error': 'Invalid username or password'
        }), 401
            
    except Exception as e:
        print(f"EXCEPTION in login: {str(e)}")
        print(f"Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    """GET /api/profile - Get current user's profile (requires token)"""
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200

# ===============================
# BOOK ENDPOINTS
# ===============================

@app.route('/api/books', methods=['GET'])
def get_all_books():
    """GET /api/books - Get all books (public endpoint)"""
    try:
        books = Book.query.all()
        return jsonify({
            'success': True,
            'data': [book.to_dict() for book in books],
            'count': len(books)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """GET /api/books/1 - Get specific book (public endpoint)"""
    try:
        book = Book.query.get(book_id)
        if book is None:
            return jsonify({
                'success': False,
                'error': 'Book not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': book.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/books', methods=['POST'])
@token_required
@admin_required
def create_book(current_user):
    """POST /api/books - Create new book (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'author', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create new book
        new_book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            price=float(data['price']),
            description=data.get('description'),
            genre=data.get('genre'),
            publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date() 
                            if data.get('publication_date') else None,
            stock_quantity=data.get('stock_quantity', 0)
        )
        
        db.session.add(new_book)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': new_book.to_dict(),
            'message': 'Book created successfully',
            'created_by': current_user.username
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/books/<int:book_id>', methods=['PUT'])
@token_required
@admin_required
def update_book(current_user, book_id):
    """PUT /api/books/1 - Update book (admin only)"""
    try:
        book = Book.query.get(book_id)
        if book is None:
            return jsonify({
                'success': False,
                'error': 'Book not found'
            }), 404
        
        data = request.get_json()
        
        # Update book fields
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'isbn' in data:
            book.isbn = data['isbn']
        if 'price' in data:
            book.price = float(data['price'])
        if 'description' in data:
            book.description = data['description']
        if 'genre' in data:
            book.genre = data['genre']
        if 'publication_date' in data:
            book.publication_date = datetime.strptime(data['publication_date'], '%Y-%m-%d').date()
        if 'stock_quantity' in data:
            book.stock_quantity = data['stock_quantity']
        
        book.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': book.to_dict(),
            'message': 'Book updated successfully',
            'updated_by': current_user.username
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@token_required
@admin_required
def delete_book(current_user, book_id):
    """DELETE /api/books/1 - Delete book (admin only)"""
    try:
        book = Book.query.get(book_id)
        if book is None:
            return jsonify({
                'success': False,
                'error': 'Book not found'
            }), 404
        
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Book deleted successfully',
            'deleted_by': current_user.username
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===============================
# SHOPPING CART
# ===============================

@app.route('/api/cart/<int:user_id>', methods=['GET'])
@token_required
def get_cart(current_user, user_id):
    """Get all items in the user's shopping cart"""
    if current_user.id != user_id:
        return jsonify({'success': False, 'error': 'You are not allowed to see this cart'}), 403

    cart = Sale.query.filter_by(user_id=user_id, status='cart').first()
    if not cart:
        return jsonify({'success': True, 'items': []})  # Empty cart

    items = [item.to_dict() for item in cart.items]
    return jsonify({'success': True, 'items': items})

@app.route('/api/cart/<int:user_id>/add', methods=['POST'])
@token_required
def add_to_cart(current_user, user_id):
    """Add a book to the shopping cart"""
    if current_user.id != user_id:
        return jsonify({'success': False, 'error': 'Cannot add to someone else\'s cart'}), 403

    data = request.get_json()
    book_id = data.get('book_id')
    quantity = int(data.get('quantity', 1))

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'success': False, 'error': 'Book not found'}), 404
    if book.stock_quantity < quantity:
        return jsonify({'success': False, 'error': f'Not enough stock for {book.title}'}), 400

    cart = Sale.query.filter_by(user_id=user_id, status='cart').first()
    if not cart:
        cart = Sale(user_id=user_id, total_amount=0, status='cart')
        db.session.add(cart)
        db.session.commit()

    sale_item = SaleItem(sale_id=cart.id, book_id=book.id, quantity=quantity, price_at_time=book.price)
    db.session.add(sale_item)
    db.session.commit()

    return jsonify({'success': True, 'message': f'{book.title} added to cart'})


# ===============================
# CHECKOUT AND LOW-STOCK ALERTS
# ===============================

@app.route('/api/checkout/<int:user_id>', methods=['POST'])
@token_required
def checkout(current_user, user_id):
    """Check out the cart and place the order"""
    if current_user.id != user_id:
        return jsonify({'success': False, 'error': 'Cannot checkout for someone else'}), 403

    cart = Sale.query.filter_by(user_id=user_id, status='cart').first()
    if not cart or not cart.items:
        return jsonify({'success': False, 'error': 'Your cart is empty'}), 400

    low_stock_alerts = []
    total_amount = 0

    for item in cart.items:
        book = Book.query.get(item.book_id)
        if book.stock_quantity < item.quantity:
            return jsonify({'success': False, 'error': f'Not enough stock for {book.title}'}), 400
        book.stock_quantity -= item.quantity
        total_amount += item.price_at_time * item.quantity

        if book.stock_quantity < 5:
            low_stock_alerts.append(f"Low stock for {book.title}! (stock={book.stock_quantity})")
            db.session.add(Notification(
                type='LOW_STOCK',
                message=f"Low stock for '{book.title}' (stock={book.stock_quantity}).",
                book_id=book.id
            ))
        if book.stock_quantity == 0:
            db.session.add(Notification(
                type='OUT_OF_STOCK',
                message=f"'{book.title}' is now OUT OF STOCK.",
                book_id=book.id
            ))

    cart.total_amount = total_amount
    cart.status = 'completed'
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Order placed successfully!',
        'order': cart.to_dict(),
        'alerts': low_stock_alerts
    })

# ===============================
# SALES ENDPOINTS
# ===============================

@app.route('/api/sales', methods=['POST'])
def create_sale():
    """POST /api/sales - Create a new sale (public endpoint for guest checkout)"""
    try:
        print("=== SALES ENDPOINT CALLED ===")
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Validate required fields
        if not data.get('items') or not isinstance(data['items'], list) or len(data['items']) == 0:
            print("ERROR: Missing or empty items")
            return jsonify({
                'success': False,
                'error': 'Items are required and must be a non-empty list'
            }), 400
        
        # Get user if token is provided (for logged-in users)
        current_user = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            current_user = User.verify_token(token)
        
        # Calculate total and validate items
        total_amount = 0
        validated_items = []
        
        print(f"Processing {len(data['items'])} items...")
        
        for item in data['items']:
            print(f"Processing item: {item}")
            if not item.get('id') or not item.get('quantity'):
                print(f"ERROR: Item missing id or quantity: {item}")
                return jsonify({
                    'success': False,
                    'error': 'Each item must have id and quantity'
                }), 400
            
            # Get book from database
            book = Book.query.get(item['id'])
            print(f"Found book: {book}")
            if not book:
                print(f"ERROR: Book with id {item['id']} not found")
                return jsonify({
                    'success': False,
                    'error': f'Book with id {item["id"]} not found'
                }), 404
            
            # Check stock
            quantity = int(item['quantity'])
            if book.stock_quantity < quantity:
                return jsonify({
                    'success': False,
                    'error': f'Insufficient stock for "{book.title}". Available: {book.stock_quantity}, Requested: {quantity}'
                }), 400
            
            # Calculate item total
            item_total = book.price * quantity
            total_amount += item_total
            
            validated_items.append({
                'book': book,
                'quantity': quantity,
                'price': book.price,
                'total': item_total
            })
        
        print(f"Total amount calculated: ${total_amount}")
        print(f"Validated items: {len(validated_items)}")
        
        # Create the sale
        new_sale = Sale(
            user_id=current_user.id if current_user else None,
            customer_email=data.get('customer_email'),
            total_amount=total_amount,
            status='completed'
        )
        
        print(f"Created sale object: {new_sale}")
        db.session.add(new_sale)
        db.session.flush()  # Get the sale ID
        print(f"Sale ID after flush: {new_sale.id}")
        
        # Create sale items and update stock
        for item in validated_items:
            sale_item = SaleItem(
                sale_id=new_sale.id,
                book_id=item['book'].id,
                quantity=item['quantity'],
                price_at_time=item['price']
            )
            print(f"Created sale item: {sale_item}")
            db.session.add(sale_item)
            
            # Update book stock
            item['book'].stock_quantity -= item['quantity']
            print(f"Updated stock for {item['book'].title}: {item['book'].stock_quantity}")
        
        db.session.commit()
        print("Sale committed to database successfully!")
        
        # Return sale details with items
        sale_dict = new_sale.to_dict()
        sale_dict['items'] = [item.to_dict() for item in new_sale.items]
        
        print(f"Returning sale data: {sale_dict}")
        
        return jsonify({
            'success': True,
            'data': sale_dict,
            'message': 'Sale completed successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sales', methods=['GET'])
@token_required
@admin_required
def get_all_sales(current_user):
    """GET /api/sales - Get all sales (admin only)"""
    try:
        sales = Sale.query.order_by(Sale.sale_date.desc()).all()
        
        sales_data = []
        for sale in sales:
            sale_dict = sale.to_dict()
            sale_dict['items'] = [item.to_dict() for item in sale.items]
            sales_data.append(sale_dict)
        
        return jsonify({
            'success': True,
            'data': sales_data,
            'count': len(sales_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sales/user', methods=['GET'])
@token_required
def get_user_sales(current_user):
    """GET /api/sales/user - Get sales for current user"""
    try:
        sales = Sale.query.filter_by(user_id=current_user.id).order_by(Sale.sale_date.desc()).all()
        
        sales_data = []
        for sale in sales:
            sale_dict = sale.to_dict()
            sale_dict['items'] = [item.to_dict() for item in sale.items]
            sales_data.append(sale_dict)
        
        return jsonify({
            'success': True,
            'data': sales_data,
            'count': len(sales_data)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sales/count', methods=['GET'])
def get_sales_count():
    """GET /api/sales/count - Get total number of sales (public endpoint for debugging)"""
    try:
        print("=== SALES COUNT ENDPOINT CALLED ===")
        total_sales = Sale.query.count()
        print(f"Total sales in database: {total_sales}")
        
        recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(5).all()
        print(f"Recent sales found: {len(recent_sales)}")
        
        recent_sales_data = []
        for sale in recent_sales:
            print(f"Processing sale: {sale}")
            sale_dict = sale.to_dict()
            sale_dict['items'] = [item.to_dict() for item in sale.items]
            recent_sales_data.append(sale_dict)
            print(f"Sale dict: {sale_dict}")
        
        result = {
            'success': True,
            'total_count': total_sales,
            'recent_sales': recent_sales_data
        }
        print(f"Returning: {result}")
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===============================
# UTILITY ENDPOINTS
# ===============================

@app.route('/api/health', methods=['GET'])
def health_check():
    """GET /api/health - Check if API is running"""
    return jsonify({
        'success': True,
        'message': 'Bookstore API with JWT Authentication is running!',
        'version': '2.0.0'
    }), 200

# ===============================
# ERROR HANDLERS
# ===============================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ===============================
# RUN THE APPLICATION
# ===============================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
# ===============================
# NOTIFICATIONS
# ===============================
from datetime import datetime

@app.route('/api/notifications', methods=['GET'])
@token_required
@admin_required
def list_notifications(current_user):
    q = Notification.query.order_by(Notification.created_at.desc())
    unseen = (request.args.get('unseen') or "").lower()
    ntype = request.args.get('type')
    if unseen in ('1','true','yes'):
        q = q.filter(Notification.seen_at.is_(None))
    if ntype:
        q = q.filter(Notification.type == ntype)
    rows = q.limit(200).all()
    return jsonify({'success': True, 'data': [n.to_dict() for n in rows]})

@app.route('/api/notifications/<int:nid>/ack', methods=['POST'])
@token_required
@admin_required
def ack_notification(current_user, nid):
    n = Notification.query.get(nid)
    if not n:
        return jsonify({'success': False, 'error': 'Not found'}), 404
    if n.seen_at is None:
        n.seen_at = datetime.utcnow()
        db.session.commit()
    return jsonify({'success': True, 'data': n.to_dict()})

# ===============================
# ORDER TRACKING (Single Sale by ID)
# ===============================
@app.route('/api/sales/<int:sale_id>', methods=['GET'])
@token_required
def get_sale_by_id(current_user, sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return jsonify({'success': False, 'error': 'Sale not found'}), 404
    if current_user.role != 'admin' and sale.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Not allowed'}), 403
    data = sale.to_dict()
    data['items'] = [i.to_dict() for i in sale.items]
    return jsonify({'success': True, 'data': data})

# ===============================
# PASSWORD RESET (Demo-friendly token flow)
# ===============================
import secrets
from datetime import timedelta

@app.route('/api/password-reset/request', methods=['POST'])
def password_reset_request():
    data = request.get_json(force=True) or {}
    email = (data.get('email') or "").strip().lower()
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400
    user = User.query.filter_by(email=email).first()
    token = None
    if user:
        token = secrets.token_hex(16)
        pr = PasswordReset(email=email, token=token, expires_at=datetime.utcnow() + timedelta(minutes=30))
        db.session.add(pr)
        db.session.commit()
    return jsonify({'success': True, 'message': 'If the email exists, a reset token has been created.', 'token': token})

@app.route('/api/password-reset/confirm', methods=['POST'])
def password_reset_confirm():
    data = request.get_json(force=True) or {}
    token = (data.get('token') or "").strip()
    new_password = (data.get('new_password') or "").strip()
    if not token or not new_password:
        return jsonify({'success': False, 'error': 'Token and new_password are required'}), 400
    pr = PasswordReset.query.filter_by(token=token).first()
    if not pr or not pr.is_valid():
        return jsonify({'success': False, 'error': 'Invalid or expired token'}), 400
    user = User.query.filter_by(email=pr.email).first()
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    user.set_password(new_password)
    pr.used_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Password has been reset.'})
