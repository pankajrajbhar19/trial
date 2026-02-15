# ============================================================================
# PRODUCTION DATABASE INITIALIZATION (Gunicorn Compatible)
# ============================================================================

def init_database():
    """
    Initialize database with tables and sample data.
    Safe for production and Gunicorn.
    """
    db.create_all()

    # Apply schema migrations safely
    try:
        _ensure_schema_columns()
    except Exception:
        pass

    # Insert default data only if DB is empty
    if User.query.first() is None:
        from models import HeritageSite, Artisan

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
        ]

        for site in heritage_sites:
            db.session.add(site)

        # Sample Artisans
        artisans = [
            Artisan(name='Ramesh Kumar', craft='Pottery', state='Rajasthan',
                    product_price=1500, contact='9876543210',
                    description='Traditional blue pottery artisan'),
        ]

        for artisan in artisans:
            db.session.add(artisan)

        db.session.commit()
        print("✓ Database initialized with sample data")
