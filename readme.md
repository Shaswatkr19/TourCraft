# 🌍 TourCraft

**TourCraft** is a comprehensive platform for creating interactive product tours and step-by-step guides. Built with Django and modern web technologies, TourCraft helps you build engaging, visual experiences with screen recordings, highlights, and smooth animations to transform complex workflows into intuitive guides.

🚀 **Live Demo**: https://tourcraft-c5bw.onrender.com

📝 Important Note

If you are new to the app, you must first Sign Up and then Log In to access the TourCraft dashboard and create tours.

⸻


## ✨ Features

- **Interactive Product Tours** - Create engaging step-by-step guides for software and applications
- **Screen Recording Integration** - Capture and integrate screen recordings seamlessly
- **Visual Highlights & Annotations** - Add callouts, arrows, and highlights to guide users
- **Smooth Animations** - Fluid transitions and animations for better user experience
- **Workflow Transformation** - Convert complex processes into intuitive visual guides
- **Customizable Templates** - Pre-built templates for different types of product tours
- **Analytics & Tracking** - Monitor user engagement and tour completion rates
- **Responsive Design** - Tours work perfectly on desktop, tablet, and mobile devices
- **Embedding Options** - Easily embed tours into websites, apps, or documentation
- **Team Collaboration** - Multiple team members can create and edit tours together

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Node.js 14+ (for frontend assets, optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/tourcraft.git
   cd tourcraft
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Apply database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to access TourCraft!

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework, PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Database**: PostgreSQL
- **Real-time Features**: WebSockets, Redis
- **Analytics**: Custom analytics dashboard
- **Deployment**: Render, Neon.tech
- **Storage**: AWS S3 (for media files)

## 📁 Project Structure

```
tourcraft/
├── tourcraft/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
├── static/
├── media/
├── requirements.txt
├── .env.example
├── render.yaml
└── manage.py
```

## 🔧 Configuration

Create a `.env` file in the root directory with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://localhost:6379/1
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
ALLOWED_HOSTS=localhost,127.0.0.1,tourcraft.onrender.com
```

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

For coverage report:

```bash
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Render (Current Deployment)

The application is currently deployed on Render with the following setup:

1. **Database**: PostgreSQL database on Render
2. **Static Files**: Served via WhiteNoise middleware
3. **Media Files**: Stored on AWS S3
4. **Environment**: Production settings with DEBUG=False

**Deployment Steps:**

1. Connect your GitHub repository to Render
2. Create a new Web Service on Render
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `gunicorn tourcraft.wsgi:application`
5. Add environment variables in Render dashboard
6. Deploy automatically on every push to main branch


### Docker

```bash
docker build -t tourcraft .
docker run -p 5000:5000 tourcraft
```

### Manual Deployment

For other platforms, you can use the following commands:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn tourcraft.wsgi:application
```

## 🌐 Live Application

Visit the live application at: https://tourcraft-c5bw.onrender.com

Features available in the live demo:
- Create and manage tours
- Interactive tour builder
- Real-time preview
- Analytics dashboard
- User management system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 API Documentation

API documentation is available at `/api/` when running the development server with Django REST Framework.

## 🔒 Security

- All user passwords are hashed using Django's built-in authentication
- CSRF protection enabled on all forms
- SQL injection protection via Django ORM
- Rate limiting implemented on API endpoints
- HTTPS encryption in production
- Secure headers and middleware configuration

## 📊 Roadmap

- [ ] Advanced animation effects and transitions
- [ ] AI-powered tour optimization suggestions
- [ ] Integration with popular design tools (Figma, Sketch)
- [ ] Multi-language support for tours
- [ ] Advanced analytics and A/B testing
- [ ] Mobile app for tour creation
- [ ] API for third-party integrations
- [ ] White-label solutions for enterprises

## 🚨 Production Notes

**Current Status**: ✅ Live on Render
- **URL**: https://tourcraft-c5bw.onrender.com
- **Database**: PostgreSQL on Neon.tech
- **Static Files**: WhiteNoise
- **Media Storage**: AWS S3
- **SSL**: Enabled
- **Auto-Deploy**: Enabled for main branch

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Django and deployed on Render
- Thanks to the open-source community for the amazing tools and libraries