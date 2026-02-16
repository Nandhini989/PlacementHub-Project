# Placement Hub System

A comprehensive web application connecting Students, Companies, and Colleges for internships, placements, resume building, and AI-based interview preparation.

## 🎯 Project Overview

**Placement Hub** is a centralized platform designed to streamline the placement process for educational institutions. It provides role-based access for students, companies, and colleges, along with AI-powered tools for resume building and interview preparation.

## 🏗️ Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Authentication**: Django Authentication with Role-Based Access Control
- **AI Features**: Resume Builder & Interview Preparation
- **Media Handling**: Image uploads (logos, profile images)

## 👥 User Roles

### 🎓 Student
- Browse and apply for jobs/internships
- Track application status
- AI-powered resume builder
- Interview preparation tools
- Profile management

### 🏢 Company
- Post job opportunities
- Review applications
- Track candidate progress
- Company profile management
- Download student resumes

### 🏫 College (Admin/Placement Cell)
- Monitor student placements
- Track placement statistics
- Connect with companies
- Analytics dashboard
- Student and company management

## 🚀 Features

### 🔐 Authentication & Security
- Role-based registration and login
- Secure password validation (8+ chars, uppercase, lowercase, numbers, special characters)
- Session-based authentication
- Role-specific dashboard redirects

### 📊 Dashboards
- **Student Dashboard**: Available jobs, application tracking, AI tools
- **Company Dashboard**: Job management, applicant tracking, statistics
- **College Dashboard**: Placement analytics, student/company management

### 🤖 AI Features
- **AI Resume Builder**: Generate professional resumes based on student profiles
- **Interview Preparation**: Company-specific and role-specific interview questions

### 📱 Responsive Design
- Mobile-friendly interface
- Modern UI with Bootstrap 5
- Clean, professional design

## 📁 Project Structure

```
placement_hub/
├── accounts/          # User authentication and role management
├── students/          # Student-specific functionality
├── companies/         # Company-specific functionality
├── colleges/          # College-specific functionality
├── jobs/              # Job postings and applications
├── ai_tools/          # AI-powered features
├── templates/         # HTML templates
├── static/            # CSS, JavaScript, images
├── media/             # User uploads
├── placement_hub/     # Main Django project
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd placementhub
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📋 Default Credentials

- **Admin User**: Username: `admin`, Password: `Admin123!`
- You can create new users through the registration page

## 🎨 UI/UX Features

- **Modern Design**: Clean, professional interface with Bootstrap 5
- **Responsive Layout**: Works seamlessly on desktop and mobile devices
- **Interactive Elements**: Hover effects, smooth transitions
- **Role-Based Navigation**: Dynamic menu based on user role
- **Dashboard Analytics**: Visual representation of placement statistics

## 🔧 Configuration

### Database Settings
- Development: SQLite (default)
- Production: Update `settings.py` with PostgreSQL configuration

### Media Files
- Profile images: `media/profile_images/`
- Company logos: `media/company_logos/`
- College logos: `media/college_logos/`
- Resumes: `media/resumes/`

### Static Files
- CSS: `static/css/`
- JavaScript: `static/js/`
- Images: `static/img/`

## 🚀 Deployment

### Production Setup
1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Set up PostgreSQL database
4. Configure static files serving
5. Set up domain and SSL

### Environment Variables
- `SECRET_KEY`: Django secret key
- `DATABASE_URL`: Database connection string
- `DEBUG`: Debug mode setting

## 📊 Models Overview

### User Model (accounts)
- Custom user model with role-based access
- Roles: student, company, college

### StudentProfile (students)
- Academic information
- Skills and experience
- Resume and profile image

### CompanyProfile (companies)
- Company details
- Industry type
- HR information

### CollegeProfile (colleges)
- Institution details
- Placement officer information

### JobPost (jobs)
- Job descriptions
- Requirements
- Application tracking

### Application (jobs)
- Student applications
- Status tracking
- Cover letters

### AI Tools Models
- Resume generation
- Interview questions
- Session management

## 🔄 API Endpoints

The application uses Django REST Framework for API functionality:
- Authentication endpoints
- Profile management
- Job postings
- Application tracking
- AI tool integration

## 🧪 Testing

Run tests with:
```bash
python manage.py test
```

## 📈 Future Enhancements

- Real-time notifications
- Advanced analytics dashboard
- Video interview integration
- Machine learning for job matching
- Mobile application
- Email notifications
- Chat support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 📞 Support

For support and queries:
- Email: support@placementhub.com
- GitHub Issues: [Repository Issues]

## 🙏 Acknowledgments

- Django Framework
- Bootstrap
- Font Awesome Icons
- Django REST Framework

---

**Placement Hub** - Empowering careers through intelligent connections! 🚀
