"""
Database Models for Digital Catalyst Platform
Contains models for Heritage Sites, Artisans, and Users
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)  # 'user' or 'manufacturer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def is_manufacturer(self):
        return (self.role or 'user').lower() == 'manufacturer'
    
    def __repr__(self):
        return f'<User {self.username}>'


class HeritageSite(db.Model):
    """Heritage Site model for cultural preservation tracking"""
    __tablename__ = 'heritage_sites'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # Temple, Fort, Monument, etc.
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # optional image URL
    annual_visitors = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def image_or_placeholder(self):
        """Return image_url or a placeholder URL based on category."""
        if self.image_url:
            return self.image_url
        from urllib.parse import quote
        text = quote(self.category or 'Heritage')
        return f"https://placehold.co/400x300/2C6E7C/FFFFFF?text={text}"
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'category': self.category,
            'description': self.description,
            'image_url': self.image_url,
            'annual_visitors': self.annual_visitors,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<HeritageSite {self.name}>'


class Artisan(db.Model):
    """Artisan model for MSME and craftsperson tracking"""
    __tablename__ = 'artisans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    craft = db.Column(db.String(100), nullable=False)  # Pottery, Weaving, Metalwork, etc.
    state = db.Column(db.String(100), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    contact = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)  # optional product/image URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def image_or_placeholder(self):
        """Return image_url or a placeholder URL based on craft."""
        if self.image_url:
            return self.image_url
        from urllib.parse import quote
        text = quote(self.craft or 'Craft')
        return f"https://placehold.co/400x300/FF6B35/FFFFFF?text={text}"
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'craft': self.craft,
            'state': self.state,
            'product_price': self.product_price,
            'contact': self.contact,
            'description': self.description,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Artisan {self.name}>'
