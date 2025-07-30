# StudyBuddy - Django Study Room Platform

A Django web application inspired by Discord, designed for students to create study rooms, engage in topic-based discussions, and find study partners around the world.

## 🚀 Features

- **Study Rooms**: Create and join topic-based study rooms
- **Real-time Messaging**: Chat with other users in study rooms
- **Topic Categories**: Browse and filter rooms by study topics
- **User Profiles**: View user profiles and activity history
- **Recent Activity Feed**: Track recent messages and room activities
- **Room Management**: Create, update, and delete study rooms (host only)
- **User Authentication**: Register, login, and manage user accounts
- **Responsive Design**: Modern, Discord-inspired UI design
- **Search Functionality**: Search for rooms by name, topic, or description

## 🛠️ Technology Stack

- **Backend**: Django 5.1.1 (Python)
- **Database**: SQLite (default) / PostgreSQL compatible
- **Frontend**: HTML5, CSS3, JavaScript
- **Templates**: Django Template Engine
- **Authentication**: Django built-in authentication system
- **Static Files**: Django static files handling

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8+
- pip (Python package installer)
- Git

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jagadeesh-sagar/Django-discord.git
cd Django-discord
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django
pip install djangorestframework  # For future API features
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Create Static Files Directory

Create the following directory structure:
```
static/
├── css/
├── js/
├── images/
└── styles/
    └── style.css
```

## 🚀 Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📁 Project Structure

```
Django-discord/
├── manage.py
├── studybud/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── base/                     # Main application
│   ├── models.py            # Room, Topic, Message models
│   ├── views.py             # All view functions
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL patterns
│   ├── admin.py             # Admin configuration
│   ├── migrations/          # Database migrations
│   ├── templates/base/      # HTML templates
│   └── api/                 # REST API (future development)
├── templates/               # Global templates
│   ├── main.html           # Base template
│   └── navbar.html         # Navigation component
└── static/                 # Static files (CSS, JS, images)
```

## 🎯 Key Models

### Room Model
- **Fields**: name, description, topic, host, participants, created, updated
- **Relationships**: Many-to-Many with Users (participants), Foreign Key to Topic and User (host)

### Topic Model
- **Fields**: name
- **Purpose**: Categorize study rooms by subject/topic

### Message Model
- **Fields**: body, user, room, created, updated
- **Relationships**: Foreign Key to User and Room

## 📖 Usage

### Creating Study Rooms
1. Register/Login to your account
2. Click "Create Room" button
3. Select a topic, add room name and description
4. Submit to create your study room

### Joining Conversations
1. Browse available rooms on the homepage
2. Click on any room to enter
3. Start chatting with other participants
4. Your messages will appear in the activity feed

### Managing Content
- **Room Hosts**: Can edit and delete their rooms
- **Message Authors**: Can delete their own messages
- **All Users**: Can join any public room and participate

## 🔧 Configuration

### Database Configuration
The project uses SQLite by default. To use PostgreSQL:

1. Install psycopg2: `pip install psycopg2`
2. Update `studybud/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'studybud_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static Files
Ensure your `settings.py` includes:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## 🎨 UI Components

The application features a modern, Discord-inspired design with:
- **Dark theme** with modern color scheme
- **Responsive layout** that works on all devices
- **Component-based templates** for reusability
- **Interactive elements** with hover effects and transitions

## 👥 User Features

### Authentication
- User registration with username and email
- Secure login/logout functionality
- Profile management and editing

### Activity Tracking
- Recent activity feed showing latest messages
- User profile pages with activity history
- Room participation tracking

### Search & Discovery
- Search rooms by name, topic, or description
- Browse topics with room counts
- Filter rooms by specific topics

## 🚀 Deployment

### Basic Deployment Steps
1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Set up static file serving
4. Use a production database (PostgreSQL recommended)
5. Configure web server (nginx + gunicorn recommended)



## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

