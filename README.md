# Digital Catalyst: AI-Driven Platform for Indian Economic Growth & Heritage Preservation

![Digital Catalyst](https://img.shields.io/badge/Version-1.0.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 🌟 Overview

**Digital Catalyst** is a comprehensive full-stack AI-powered platform designed to support and accelerate India's economic growth through heritage preservation and artisan empowerment. The platform combines modern web technologies with machine learning to provide intelligent recommendations and analytics for cultural heritage sites and traditional craftspeople.

### 🎯 Key Features

- **Heritage Management Module**: Comprehensive CRUD operations for heritage sites across India
- **Artisan & MSME Module**: Track and support traditional artisans and their crafts
- **AI Recommendation System**: Content-based filtering for heritage sites and artisans
- **Economic Analytics Dashboard**: Real-time insights with interactive Chart.js visualizations
- **User Authentication**: Secure login/registration system with Flask-Login
- **Search & Filter**: Advanced filtering by state, category, craft type
- **CSV Export**: Export heritage sites and artisans data
- **RESTful APIs**: Well-documented API endpoints for integration
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5

## 🏗️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **SQLite** - Lightweight database

### Frontend
- **HTML5/CSS3**
- **Bootstrap 5.3.0** - Responsive framework
- **JavaScript (ES6+)**
- **Chart.js** - Data visualization
- **Bootstrap Icons** - Icon library
- **Google Fonts** (Playfair Display, Work Sans)

### AI/ML
- **scikit-learn** - Machine learning algorithms
- **pandas** - Data manipulation
- **numpy** - Numerical computing

## 📁 Project Structure

```
digital_catalyst/
│
├── app.py                          # Main Flask application
├── models.py                       # Database models (User, HeritageSite, Artisan)
├── requirements.txt                # Python dependencies
├── database.db                     # SQLite database (auto-generated)
│
├── ml/
│   └── recommendation_engine.py    # AI recommendation algorithms
│
├── templates/
│   ├── base.html                   # Base template with navigation
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── dashboard.html              # Main analytics dashboard
│   ├── heritage.html               # Heritage sites listing
│   ├── add_heritage.html           # Add heritage site form
│   ├── edit_heritage.html          # Edit heritage site form
│   ├── artisans.html               # Artisans listing
│   ├── add_artisan.html            # Add artisan form
│   └── edit_artisan.html           # Edit artisan form
│
└── static/
    ├── css/
    │   └── style.css               # Custom styles (Indian-inspired design)
    └── js/
        └── main.js                 # Custom JavaScript
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step-by-Step Installation

1. **Navigate to the project directory:**
   ```bash
   cd digital_catalyst
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   If you get an SSL certificate error, use:
   ```bash
   pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```
   Or use the run script (installs dependencies if needed):
   ```bash
   chmod +x run.sh && ./run.sh
   ```

6. **Access the application:**
   Open your web browser and navigate to:
   ```
   http://localhost:5001
   ```

### Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📊 Sample Data

The application comes pre-loaded with sample data including:

### Heritage Sites (8 sites)
- Taj Mahal (Uttar Pradesh)
- Red Fort (Delhi)
- Ajanta Caves (Maharashtra)
- Hampi (Karnataka)
- Golden Temple (Punjab)
- Konark Sun Temple (Odisha)
- Khajuraho Temples (Madhya Pradesh)
- Mysore Palace (Karnataka)

### Artisans (8 artisans)
- Pottery experts from Rajasthan
- Weaving specialists from West Bengal
- Metalwork craftsmen from Uttar Pradesh
- Embroidery artists from Gujarat
- Wood carvers from Kerala
- Painters from Madhya Pradesh
- Jewelry makers from Rajasthan
- Basket weavers from Assam

## 🔌 REST API Endpoints

### Heritage Sites API

**GET /api/heritage**
- Returns all heritage sites in JSON format
- No authentication required

Example response:
```json
[
  {
    "id": 1,
    "name": "Taj Mahal",
    "state": "Uttar Pradesh",
    "category": "Monument",
    "description": "Iconic white marble mausoleum",
    "annual_visitors": 7000000,
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  }
]
```

### Artisans API

**GET /api/artisans**
- Returns all artisans in JSON format
- No authentication required

Example response:
```json
[
  {
    "id": 1,
    "name": "Ramesh Kumar",
    "craft": "Pottery",
    "state": "Rajasthan",
    "product_price": 1500,
    "contact": "9876543210",
    "description": "Traditional blue pottery artisan",
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  }
]
```

### Recommendations API

**GET /api/recommendations?type=heritage&top_n=5**
- Returns AI-recommended heritage sites
- Parameters:
  - `type`: 'heritage' or 'artisans'
  - `top_n`: Number of recommendations (default: 5)
  - `state`: State filter for artisans (optional)

**GET /api/analytics**
- Returns comprehensive analytics data including:
  - Economic impact metrics
  - Visitor trends
  - State-wise distribution

## 🎨 Design Philosophy

The platform features a distinctive **Indian-inspired modern design** with:

- **Color Palette**: Navy, teal, saffron, gold, and coral
- **Typography**: Playfair Display (headings) + Work Sans (body)
- **Animations**: Smooth transitions and micro-interactions
- **Responsive**: Mobile-first design approach
- **Accessibility**: WCAG 2.1 compliant color contrasts

## 🧠 AI/ML Features

### Recommendation Engine

The platform uses content-based filtering to provide intelligent recommendations:

1. **Heritage Site Recommendations**
   - Ranks sites by annual visitor count
   - Considers category similarity
   - Returns top N most popular sites

2. **Artisan Recommendations**
   - Filters by state (optional)
   - Sorts by product price (affordable first)
   - Supports craft-based categorization

3. **Economic Impact Analysis**
   - Calculates tourism revenue estimates
   - Computes artisan revenue projections
   - Provides total economic impact metrics

## 📈 Features Breakdown

### 1. Heritage Management Module
- ✅ Add new heritage sites
- ✅ Edit existing sites
- ✅ Delete sites
- ✅ Search and filter by name, state, category
- ✅ View visitor statistics
- ✅ Export to CSV

### 2. Artisan & MSME Module
- ✅ Add new artisans
- ✅ Edit artisan profiles
- ✅ Delete artisans
- ✅ Search and filter by name, state, craft
- ✅ Track product pricing
- ✅ Export to CSV

### 3. Analytics Dashboard
- ✅ Real-time statistics (sites, artisans, states, visitors)
- ✅ AI-powered recommendations
- ✅ Economic impact visualization
- ✅ Interactive charts (Bar chart, Doughnut chart)
- ✅ State-wise distribution analysis

### 4. Authentication System
- ✅ User registration
- ✅ Secure login
- ✅ Password hashing
- ✅ Session management
- ✅ Protected routes

## 🔒 Security Features

- Password hashing using Werkzeug security
- CSRF protection
- SQL injection prevention through SQLAlchemy ORM
- Session-based authentication
- Login required decorators for protected routes

## 🌐 Browser Support

- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🐛 Troubleshooting

### Common Issues

1. **Import Error: No module named 'flask'**
   - Solution: Run `pip install -r requirements.txt`
   - If you get an SSL certificate error, run:
     ```bash
     pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
     ```

2. **Database locked error**
   - Solution: Close any other instances of the app and restart

3. **Port 5001 already in use**
   - Solution: Change the port in `app.py` (last line), e.g. to `port=5002`

4. **Charts not displaying**
   - Solution: Ensure internet connection (Chart.js loaded from CDN)

## 🚀 Future Enhancements

- [ ] Multi-language support (Hindi, regional languages)
- [ ] Image upload for heritage sites and artisans
- [ ] Advanced analytics with ML predictions
- [ ] Payment gateway integration for artisans
- [ ] Mobile app version
- [ ] Social media integration
- [ ] Email notifications
- [ ] Admin dashboard with role-based access

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for India's Heritage & Economic Growth

## 📞 Support

For issues and questions, please create an issue in the repository.

---

**Made with passion to empower India's cultural heritage and artisan economy! 🇮🇳**
