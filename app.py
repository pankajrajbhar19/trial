"""
Digital Catalyst: AI-Driven Platform for Indian Economic Growth & Heritage Preservation
========================================================================================

Main Flask Application with Blueprint-based Modular Architecture

Academic Note:
This application demonstrates professional Flask architecture using Blueprints for
modular organization. The application is structured into four main components:

1. Authentication (blueprints/auth.py): User login, registration, logout
2. Main Application (blueprints/main.py): Core CRUD operations for heritage sites, artisans, products
3. REST API (blueprints/api.py): JSON endpoints for programmatic access
4. Analytics Dashboard (blueprints/dashboard.py): Admin analytics and reporting

Architecture Benefits:
- Separation of Concerns: Each blueprint handles specific functionality
- Maintainability: Easier to locate and modify code
- Scalability: New features can be added as new blueprints
- Testability: Each blueprint can be tested independently
- Reusability: Blueprints can be reused across projects

Database Design:
- SQLite for development (easy setup, no server required)
- SQLAlchemy ORM for database abstraction
- Proper relationships with foreign keys and cascade rules
- Indexes on frequently queried columns

Security Features:
- Password hashing using werkzeug.security
- Session-based authentication using Flask-Login
- CSRF protection (to be added)
- Input validation and sanitization
- Role-based access control
"""

from flask import Flask
from flask_login import LoginManager
from models import db, User
from werkzeug.security import generate_password_hash
from sqlalchemy import text

# Initialize Flask app
app = Flask(__name__)

# ============================================================================
# APPLICATION CONFIGURATION
# ============================================================================

# Academic Note: Configuration should be externalized in production
# Use environment variables or config files for sensitive data
import os

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'digital-catalyst-secret-key-2026')

# Fix for Render PostgreSQL URL (postgres:// -> postgresql://)
database_url = os.environ.get('DATABASE_URL', f'sqlite:///{os.path.join(basedir, "instance", "database.db")}')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database connection pooling for better performance
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,           # Maximum number of connections
    'pool_recycle': 3600,      # Recycle connections after 1 hour
    'pool_pre_ping': True      # Verify connections before use
}

# Disable template auto-reload for better performance
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = False

# ============================================================================
# SECURITY CONFIGURATION
# ============================================================================

# Academic Note - Session Security:
# ---------------------------------
# These settings protect against common session-based attacks:
#
# SESSION_COOKIE_SECURE:
# - Ensures cookies only sent over HTTPS
# - Prevents man-in-the-middle attacks
# - Set to False for development (HTTP), True for production (HTTPS)
#
# SESSION_COOKIE_HTTPONLY:
# - Prevents JavaScript access to session cookies
# - Mitigates XSS (Cross-Site Scripting) attacks
# - Even if attacker injects JS, they can't steal session
#
# SESSION_COOKIE_SAMESITE:
# - Prevents CSRF (Cross-Site Request Forgery) attacks
# - 'Lax': Cookies sent with top-level navigation (GET requests)
# - 'Strict': Cookies never sent from external sites (more secure but less usable)
# - 'None': No protection (requires SECURE flag)
#
# PERMANENT_SESSION_LIFETIME:
# - Auto-logout after inactivity period
# - Reduces risk of session hijacking
# - Balance security vs user convenience

from datetime import timedelta

# Session cookie security settings
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)  # 24-hour session timeout

# File upload security settings
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size

# ============================================================================
# INITIALIZE EXTENSIONS
# ============================================================================

# Initialize database
db.init_app(app)

# Initialize Flask-Login for session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated

@login_manager.user_loader
def load_user(user_id):
    """
    User Loader Callback
    
    Flask-Login uses this to reload user object from user ID stored in session.
    
    Academic Note:
    This callback is called on every request to load the current user.
    It should be efficient (use caching in production).
    """
    return User.query.get(int(user_id))

# ============================================================================
# REGISTER BLUEPRINTS
# ============================================================================

# Academic Note: Blueprints are registered with URL prefixes
# This creates a clear URL structure:
# - /auth/login, /auth/register, /auth/logout
# - /heritage, /artisans, /products (no prefix for main routes)
# - /api/heritage, /api/artisans, /api/recommendations
# - /dashboard/analytics

from blueprints.auth import auth_bp
from blueprints.main import main_bp
from blueprints.api import api_bp
from blueprints.dashboard import dashboard_bp

app.register_blueprint(auth_bp)      # URL prefix: /auth
app.register_blueprint(main_bp)      # URL prefix: / (none)
app.register_blueprint(api_bp)       # URL prefix: /api
app.register_blueprint(dashboard_bp) # URL prefix: /dashboard

# ============================================================================
# DATABASE INITIALIZATION ON STARTUP
# ============================================================================

# Initialize database when app starts (works with Gunicorn)
with app.app_context():
    try:
        db.create_all()
        print("✓ Database tables created/verified")
        
        # Check if admin user exists, if not create it
        if User.query.first() is None:
            print("Initializing database with default users...")
            from models import HeritageSite, Artisan
            
            # Create default users
            admin_user = User(
                username='admin',
                email='admin@digitalcatalyst.in',
                password=generate_password_hash('admin123'),
                role='user'
            )
            manufacturer_user = User(
                username='manufacturer',
                email='manufacturer@digitalcatalyst.in',
                password=generate_password_hash('manufacturer123'),
                role='manufacturer'
            )
            
            db.session.add(admin_user)
            db.session.add(manufacturer_user)
            
            # Sample Heritage Sites
            heritage_sites = [
                HeritageSite(name='Taj Mahal', state='Uttar Pradesh', category='Monument', 
                           description='Iconic white marble mausoleum', annual_visitors=7000000),
                HeritageSite(name='Red Fort', state='Delhi', category='Fort', 
                           description='Historic fortified palace', annual_visitors=2500000),
                HeritageSite(name='Ajanta Caves', state='Maharashtra', category='Cave Temple', 
                           description='Ancient Buddhist rock-cut caves', annual_visitors=600000),
                HeritageSite(name='Hampi', state='Karnataka', category='Archaeological Site', 
                           description='Ruins of Vijayanagara Empire', annual_visitors=500000),
                HeritageSite(name='Golden Temple', state='Punjab', category='Temple', 
                           description='Holiest Gurdwara of Sikhism', annual_visitors=100000),
                HeritageSite(name='Konark Sun Temple', state='Odisha', category='Temple', 
                           description='13th-century Sun Temple', annual_visitors=400000),
                HeritageSite(name='Khajuraho Temples', state='Madhya Pradesh', category='Temple', 
                           description='Medieval Hindu and Jain temples', annual_visitors=300000),
                HeritageSite(name='Mysore Palace', state='Karnataka', category='Palace', 
                           description='Historical palace in Mysore', annual_visitors=2800000),
            ]
            
            for site in heritage_sites:
                db.session.add(site)
            
            # Sample Artisans
            artisans = [
                Artisan(name='Ramesh Kumar', craft='Pottery', state='Rajasthan', 
                       product_price=1500, contact='9876543210', 
                       description='Traditional blue pottery artisan'),
                Artisan(name='Lakshmi Devi', craft='Weaving', state='West Bengal', 
                       product_price=3500, contact='9876543211', 
                       description='Handloom saree weaver'),
                Artisan(name='Mohammed Ali', craft='Metalwork', state='Uttar Pradesh', 
                       product_price=2500, contact='9876543212', 
                       description='Brass and copper craftsman'),
                Artisan(name='Priya Sharma', craft='Embroidery', state='Gujarat', 
                       product_price=2000, contact='9876543213', 
                       description='Kutch embroidery specialist'),
                Artisan(name='Suresh Babu', craft='Wood Carving', state='Kerala', 
                       product_price=4000, contact='9876543214', 
                       description='Traditional temple wood carver'),
                Artisan(name='Anjali Patel', craft='Painting', state='Madhya Pradesh', 
                       product_price=1200, contact='9876543215', 
                       description='Gond art painter'),
                Artisan(name='Vijay Singh', craft='Jewelry Making', state='Rajasthan', 
                       product_price=5000, contact='9876543216', 
                       description='Kundan jewelry craftsman'),
                Artisan(name='Geeta Rani', craft='Basket Weaving', state='Assam', 
                       product_price=800, contact='9876543217', 
                       description='Bamboo basket weaver'),
            ]
            
            for artisan in artisans:
                db.session.add(artisan)
            
            db.session.commit()
            print("✓ Database initialized with sample data!")
            print("✓ Default users: admin/admin123, manufacturer/manufacturer123")
        else:
            print("✓ Database already initialized")
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        # Don't fail app startup, just log the error

# ============================================================================
# DATABASE SCHEMA MIGRATION
# ============================================================================

def _ensure_schema_columns():
    """
    Add missing columns for existing databases.
    
    Academic Note:
    This function handles schema evolution without losing data.
    In production, use proper migration tools like Alembic.
    
    Migrations Applied:
    - Add 'role' column to users table (for role-based access control)
    - Add 'image_url' column to heritage_sites table
    - Add 'image_url' column to artisans table
    """
    migrations = [
        ("users", "role", "VARCHAR(20) DEFAULT 'user'"),
        ("heritage_sites", "image_url", "VARCHAR(500)"),
        ("artisans", "image_url", "VARCHAR(500)"),
    ]
    
    for table, column, col_type in migrations:
        try:
            db.session.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}"))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # Ignore "duplicate column" errors (column already exists)
            if "duplicate column name" not in str(e).lower():
                raise

# Global flag to ensure migration runs only once per process
_role_migration_done = False

@app.before_request
def run_schema_migration_once():
    """
    Run schema migration before first request.
    
    Academic Note:
    This ensures database schema is up-to-date before handling requests.
    The global flag prevents running migration on every request.
    """
    global _role_migration_done
    if _role_migration_done:
        return
    try:
        _ensure_schema_columns()
    except Exception:
        pass  # Ignore errors (columns may already exist)
    _role_migration_done = True

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database():
    """
    Initialize database with tables and sample data.
    
    Academic Note:
    This function demonstrates database initialization with:
    1. Table creation using SQLAlchemy models
    2. Schema migration for existing databases
    3. Sample data insertion for development/testing
    
    In production:
    - Use proper migration tools (Alembic)
    - Don't insert sample data
    - Use database backups
    """
    with app.app_context():
        # Create all tables defined in models.py
        db.create_all()
        
        # Apply schema migrations
        try:
            _ensure_schema_columns()
        except Exception:
            pass
        
        # Check if data already exists
        if User.query.first() is None:
            # Import models here to avoid circular imports
            from models import HeritageSite, Artisan
            
            # Create default users with different roles
            users = [
                User(
                    username='admin',
                    email='admin@digitalcatalyst.in',
                    password=generate_password_hash('admin123'),
                    role='user'
                ),
                User(
                    username='manufacturer',
                    email='manufacturer@digitalcatalyst.in',
                    password=generate_password_hash('manufacturer123'),
                    role='manufacturer'
                )
            ]
            
            for user in users:
                db.session.add(user)
            
            # Sample Heritage Sites
            heritage_sites = [
                HeritageSite(name='Taj Mahal', state='Uttar Pradesh', category='Monument', 
                           description='Iconic white marble mausoleum', annual_visitors=7000000),
                HeritageSite(name='Red Fort', state='Delhi', category='Fort', 
                           description='Historic fortified palace', annual_visitors=2500000),
                HeritageSite(name='Ajanta Caves', state='Maharashtra', category='Cave Temple', 
                           description='Ancient Buddhist rock-cut caves', annual_visitors=600000),
                HeritageSite(name='Hampi', state='Karnataka', category='Archaeological Site', 
                           description='Ruins of Vijayanagara Empire', annual_visitors=500000),
                HeritageSite(name='Golden Temple', state='Punjab', category='Temple', 
                           description='Holiest Gurdwara of Sikhism', annual_visitors=100000),
                HeritageSite(name='Konark Sun Temple', state='Odisha', category='Temple', 
                           description='13th-century Sun Temple', annual_visitors=400000),
                HeritageSite(name='Khajuraho Temples', state='Madhya Pradesh', category='Temple', 
                           description='Medieval Hindu and Jain temples', annual_visitors=300000),
                HeritageSite(name='Mysore Palace', state='Karnataka', category='Palace', 
                           description='Historical palace in Mysore', annual_visitors=2800000),
            ]
            
            for site in heritage_sites:
                db.session.add(site)
            
            # Sample Artisans
            artisans = [
                Artisan(name='Ramesh Kumar', craft='Pottery', state='Rajasthan', 
                       product_price=1500, contact='9876543210', 
                       description='Traditional blue pottery artisan'),
                Artisan(name='Lakshmi Devi', craft='Weaving', state='West Bengal', 
                       product_price=3500, contact='9876543211', 
                       description='Handloom saree weaver'),
                Artisan(name='Mohammed Ali', craft='Metalwork', state='Uttar Pradesh', 
                       product_price=2500, contact='9876543212', 
                       description='Brass and copper craftsman'),
                Artisan(name='Priya Sharma', craft='Embroidery', state='Gujarat', 
                       product_price=2000, contact='9876543213', 
                       description='Kutch embroidery specialist'),
                Artisan(name='Suresh Babu', craft='Wood Carving', state='Kerala', 
                       product_price=4000, contact='9876543214', 
                       description='Traditional temple wood carver'),
                Artisan(name='Anjali Patel', craft='Painting', state='Madhya Pradesh', 
                       product_price=1200, contact='9876543215', 
                       description='Gond art painter'),
                Artisan(name='Vijay Singh', craft='Jewelry Making', state='Rajasthan', 
                       product_price=5000, contact='9876543216', 
                       description='Kundan jewelry craftsman'),
                Artisan(name='Geeta Rani', craft='Basket Weaving', state='Assam', 
                       product_price=800, contact='9876543217', 
                       description='Bamboo basket weaver'),
            ]
            
            for artisan in artisans:
                db.session.add(artisan)
            
            # Commit all changes
            db.session.commit()
            print("✓ Database initialized with sample data!")
            print("✓ Default users created:")
            print("  - Username: admin, Password: admin123 (role: user)")
            print("  - Username: manufacturer, Password: manufacturer123 (role: manufacturer)")

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Initialize database on startup
    init_database()
    
    # Run Flask development server
    # Academic Note: This is for development only
    # In production, use a WSGI server like Gunicorn or uWSGI
    port = int(os.environ.get('PORT', 5002))
    app.run(
        debug=False,              # Disable debug mode for better performance
        host='0.0.0.0',          # Listen on all interfaces for production
        port=port,               # Port from environment or default 5002
        threaded=True,           # Enable threading for concurrent requests
        use_reloader=False       # Disable auto-reloader for faster startup
    )

# ============================================================================
# ACADEMIC NOTES ON FLASK APPLICATION STRUCTURE
# ============================================================================

"""
Flask Application Lifecycle:
1. Application Initialization: Create Flask app instance
2. Configuration: Set app.config values
3. Extension Initialization: Initialize Flask extensions (SQLAlchemy, Flask-Login)
4. Blueprint Registration: Register modular components
5. Request Handling: Process incoming HTTP requests
6. Response Generation: Return HTTP responses

Request-Response Cycle:
1. Client sends HTTP request
2. Flask routes request to appropriate blueprint/route
3. Route function executes business logic
4. Database queries performed if needed
5. Template rendered with data
6. HTTP response sent to client

Database ORM (Object-Relational Mapping):
- SQLAlchemy provides Python classes for database tables
- Automatic SQL generation from Python code
- Type safety and validation
- Relationship management
- Query optimization

Security Considerations:
- Password hashing (never store plaintext)
- Session management (secure cookies)
- CSRF protection (prevent cross-site attacks)
- Input validation (prevent injection attacks)
- Role-based access control (authorization)

Performance Optimization:
- Database connection pooling
- Query optimization (select only needed columns)
- Caching (Redis for production)
- Lazy loading (load data only when needed)
- Pagination (limit query results)

Scalability Considerations:
- Horizontal scaling (multiple app instances)
- Load balancing (distribute requests)
- Database replication (read replicas)
- Caching layer (Redis, Memcached)
- CDN for static files

Production Deployment:
- Use PostgreSQL instead of SQLite
- Use Gunicorn/uWSGI as WSGI server
- Use Nginx as reverse proxy
- Enable HTTPS with SSL certificates
- Set up monitoring and logging
- Implement backup strategy
- Use environment variables for configuration
"""
