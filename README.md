# 📚 Student Performance Tracker

A comprehensive web-based application for tracking student performance across multiple subjects. Built with Flask, SQLite, and modern web technologies featuring a beautiful dark/light theme switcher.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![Flask](https://img.shields.io/badge/flask-3.0.0-red)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 🌟 Features

### Core Functionality
- **Student Management**: Add, view, and manage student records with unique roll numbers
- **Grade Tracking**: Record and update grades for multiple subjects
- **Performance Analytics**: 
  - Automatic student average calculation
  - Subject-wise topper identification
  - Class average calculation per subject
- **Data Export**: Export student data to text files for backup
- **Database Persistence**: SQLite database for reliable data storage

### UI/UX Features
- **🌓 Dark/Light Theme Switcher**: Toggle between themes with localStorage persistence
- **Modern Responsive Design**: Beautiful gradients, smooth animations, and glassmorphism effects
- **Color-Coded Performance**: Visual badges for quick performance assessment
- **Dynamic Forms**: Add multiple subjects at once with dynamic input fields
- **Flash Messages**: User-friendly notifications with auto-dismiss

---

## 📋 Requirements

- Python 3.11 or higher
- Flask 3.0.0
- Werkzeug 3.0.1

---

## 🚀 Quick Start

### Local Installation

1. **Clone or download the project**
   ```bash
   cd "Student Performance Tracker"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

---

## 🌐 Deployment to Vercel

### Prerequisites
- A [Vercel account](https://vercel.com/signup) (free tier available)
- Git repository with your code (GitHub, GitLab, or Bitbucket)

### Quick Deploy Steps

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New Project"
   - Import your GitHub repository
   - Vercel will automatically detect it's a Python project

3. **Configure Project**
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: (leave empty)
   - Install Command: `pip install -r requirements.txt`

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at `https://your-project-name.vercel.app`

### Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

### ⚠️ Important: Database Persistence

SQLite databases are **ephemeral** on Vercel (serverless environment). Data will be reset on each deployment. For production, consider using:
- **Vercel Postgres** (recommended)
- **PlanetScale** (MySQL)
- **Supabase** (PostgreSQL)
- **MongoDB Atlas**

### Alternative Deployment Platforms
- **Railway** (free tier with limitations)
- **PythonAnywhere** (free tier available)
- **Render** (free tier available)

---

## 📖 User Guide

### Adding a Student

1. Click **"Add Student"** in the navigation
2. Enter student name and unique roll number
3. Click **"Add Student"** button
4. Success message will confirm the addition

### Adding Grades

1. Navigate to **"Students"** page
2. Click **"Add Grades"** button next to a student
3. Enter subject name and grade (0-100)
4. Click **"Add Another Subject"** to add more subjects
5. Submit the form

### Viewing Student Details

1. Go to **"Students"** page
2. Click **"View Details"** for any student
3. See all grades, average, and performance summary

### Finding Subject Toppers

1. Click **"Toppers"** in navigation
2. Select a subject from dropdown
3. View the top-performing student with their grade

### Calculating Class Average

1. Click **"Averages"** in navigation
2. Select a subject from dropdown
3. View the class average for that subject

### Exporting Data

1. Click **"Export"** in navigation
2. Data will be exported to `exports/` folder
3. Download confirmation will be shown

### Using Theme Switcher

1. Locate the **🌙/☀️ icon** in the top-right corner
2. Click to toggle between light and dark modes
3. Your preference is automatically saved

---

## 🏗️ Project Structure

```
Student Performance Tracker/
├── app.py                  # Main Flask application
├── models.py               # Student and StudentTracker classes
├── database.py             # Database operations (SQLite)
├── templates/              # HTML templates (Jinja2)
│   ├── base.html          # Base template with theme switcher
│   ├── index.html         # Dashboard
│   ├── add_student.html   # Add student form
│   ├── add_grades.html    # Add grades form
│   ├── view_student.html  # Student details
│   ├── students_list.html # All students list
│   ├── subject_topper.html# Subject topper page
│   ├── class_average.html # Class average page
│   ├── 404.html           # Not found error
│   └── 500.html           # Server error
├── static/
│   └── style.css          # Modern CSS with dark mode
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## 🛠️ Technologies Used

### Backend
- **Flask 3.0.0** - Python web framework
- **SQLite** - Lightweight, serverless database
- **Python 3.11+** - Programming language

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **JavaScript** - Theme switcher and dynamic forms
- **Google Fonts (Inter)** - Typography

### Deployment
- **Vercel** - Serverless deployment platform
- **Git** - Version control

---

## 🎨 Theme Switcher

### Features
- **Toggle Button**: Located in header navigation with dynamic icon (🌙/☀️)
- **Dark Mode**: Deep navy backgrounds with light text for reduced eye strain
- **Light Mode**: Clean white backgrounds with dark text
- **Persistence**: Theme preference saved in browser localStorage
- **Smooth Transitions**: All colors transition smoothly (0.3s ease)

### Color Palette

**Light Mode:**
- Background: White (#ffffff), Light Gray (#f9fafb)
- Text: Dark Gray (#111827), Medium Gray (#6b7280)
- Gradient: Purple to Violet (#667eea → #764ba2)

**Dark Mode:**
- Background: Dark Slate (#1f2937), Darker Slate (#111827)
- Text: Off-White (#f9fafb), Light Gray (#d1d5db)
- Gradient: Dark Blue (#1e293b → #0f172a)

---

## 📊 Database Schema

### Students Table
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Grades Table
```sql
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    grade REAL NOT NULL CHECK(grade >= 0 AND grade <= 100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    UNIQUE(student_id, subject)
);
```

---

## 🔧 Configuration

### Vercel Configuration (vercel.json)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

---

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.11+ is installed
- Verify virtual environment is activated
- Check all dependencies are installed: `pip install -r requirements.txt`

### Database errors
- Delete `student_tracker.db` and restart the app
- Database will be recreated automatically

### Theme not persisting
- Check if browser allows localStorage
- Clear browser cache and try again

### Static files not loading on Vercel
- Ensure paths use `url_for('static', filename='...')`
- Check Vercel build logs for errors

---

## 📝 Best Practices

### For Teachers
- Use consistent roll number format (e.g., STU001, STU002)
- Enter grades as soon as assessments are completed
- Regularly export data for backup
- Use subject-wise toppers to identify high performers
- Monitor class averages to track overall performance

### For Developers
- Keep dependencies updated
- Use environment variables for sensitive data
- Implement proper error handling
- Add input validation on both client and server side
- Consider migrating to persistent database for production

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License for educational purposes.

---

## 🙏 Acknowledgments

- Flask documentation and community
- Vercel for serverless deployment
- Google Fonts for Inter typeface
- All contributors and users

---

## 📧 Support

For issues, questions, or suggestions:
- Create an issue in the repository
- Check existing documentation
- Review troubleshooting section

---

## 🚀 Future Enhancements

Potential features for future versions:
- User authentication and authorization
- Multi-class support
- Advanced analytics and charts
- Email notifications for grade updates
- PDF report generation
- Mobile app version
- Real-time collaboration features

---

**Made with ❤️ for educators and students**

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Status**: Production Ready ✅
