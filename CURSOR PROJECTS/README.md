# Gmail Self-Mail Tool

A secure and efficient Flask application that allows users to access and manage their Gmail inbox through a web interface. Built with performance and security in mind.

## Features

- 🔐 Secure Gmail OAuth2.0 Authentication
- 📧 View and manage Gmail inbox
- ⚡ Optimized performance with caching
- 🔒 Production-ready security features
- 📱 Responsive web interface
- 🚀 Easy deployment configuration

## Tech Stack

- **Backend**: Flask 2.3.3
- **Authentication**: Google OAuth2.0
- **Server**: Waitress (Windows) / Gunicorn (Unix)
- **Caching**: Flask-Caching, Cachetools
- **Security**: Werkzeug, Python-dotenv
- **Frontend**: HTML, CSS, JavaScript

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- Gmail API credentials

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd gmail-self-mail-tool
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Google OAuth2.0:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project
   - Enable Gmail API
   - Create OAuth 2.0 credentials
   - Download credentials and save as `client_secrets.json`

5. Create environment file:
```bash
cp .env.example .env
```
Edit `.env` with your configuration:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
PORT=3000
```

## Running the Application

### Development
```bash
python run.py
```

### Production
```bash
python run_prod.py
```

The application will be available at `http://localhost:3000`

## Project Structure

```
gmail-self-mail-tool/
├── app.py              # Main application file
├── config.py           # Configuration settings
├── run.py             # Development server
├── run_prod.py        # Production server
├── wsgi.py            # WSGI entry point
├── requirements.txt   # Python dependencies
├── client_secrets.json # Google OAuth credentials
├── .env               # Environment variables
└── templates/         # HTML templates
    ├── index.html
    ├── emails.html
    ├── 404.html
    └── 500.html
```

## Security Features

- Secure session management
- HTTP-only cookies
- SameSite cookie policy
- CSRF protection
- Rate limiting
- Secure headers
- Environment-based configuration

## Performance Optimizations

- Response caching
- Memory-efficient credential storage
- Batch API requests
- Static file caching
- Garbage collection management

## Deployment

### Windows (Production)
```bash
python run_prod.py
```

### Unix/Linux (Production)
```bash
gunicorn wsgi:app
```

### Docker
```bash
docker build -t gmail-self-mail .
docker run -p 3000:3000 gmail-self-mail
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| FLASK_ENV | Application environment | development |
| SECRET_KEY | Flask secret key | dev |
| PORT | Server port | 3000 |

## Error Handling

The application includes comprehensive error handling for:
- Authentication failures
- API errors
- Network issues
- Invalid requests
- Server errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the repository or contact the maintainers.

## Acknowledgments

- Google Gmail API
- Flask framework
- Waitress/Gunicorn
- All contributors and maintainers 