# 🎉 David's 30th Birthday Party - Production Deployment Guide

## Overview
Your Flask application is now fully configured for production deployment. This guide covers everything needed to run the application safely and reliably on your server or local network.

## ✅ Pre-Deployment Checklist

- [ ] Python 3.9+ is installed
- [ ] Virtual environment created (`.venv/`)
- [ ] All dependencies installed from `requirements-prod.txt`
- [ ] `.env.production` configured with your settings
- [ ] Moderator password changed (currently: `123`)
- [ ] All games tested in development mode
- [ ] Firewall rules configured to allow port 5000 (or your custom port)

## 🚀 Quick Start

### Windows
```powershell
# From the project directory
.\run-production.bat
```

### Linux/macOS
```bash
# Make script executable
chmod +x run-production.sh

# Run the startup script
./run-production.sh
```

### Manual Start (Any OS)
```bash
# 1. Activate virtual environment
# Windows: .venv\Scripts\activate.bat
# Linux/macOS: source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements-prod.txt

# 3. Set environment variables (optional - defaults are used otherwise)
# Windows PowerShell:
# $env:FLASK_ENV = "production"
# $env:SECRET_KEY = "your-secure-key-here"
# $env:FLASK_HOST = "0.0.0.0"
# $env:FLASK_PORT = "5000"

# Linux/macOS:
# export FLASK_ENV=production
# export SECRET_KEY="your-secure-key-here"
# export FLASK_HOST=0.0.0.0
# export FLASK_PORT=5000

# 4. Start Gunicorn
gunicorn --workers=4 --bind=0.0.0.0:5000 app:app
```

## 🔐 Security Configuration

### Change the Moderator Password
Edit `app.py` and change the password validation in the `/moderator_login` route:

```python
# Current (line ~420):
if password == '123':

# Change to:
if password == 'your_new_secure_password':
```

### Generate a Secure SECRET_KEY
```bash
# Python
python -c "import secrets; print(secrets.token_hex(32))"

# Or use online generator (not recommended for production)
```

Then add to `.env.production`:
```
SECRET_KEY=your_generated_key_here
```

### Enable HTTPS (Required for Production)
If accessing from external networks:

1. **Option A: Self-Signed Certificate (Testing Only)**
```bash
# Generate certificate valid for 365 days
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

2. **Option B: Let's Encrypt (Free & Recommended)**
- Use certbot for automatic SSL/TLS certificates
- Configure reverse proxy (nginx/Apache)

3. **Option C: Commercial Certificate**
- Purchase from certificate authority
- Install on production server

### Session Security
The app automatically sets:
- `SESSION_COOKIE_HTTPONLY=True` (prevents JavaScript access)
- `SESSION_COOKIE_SAMESITE=Lax` (prevents CSRF attacks)
- `SESSION_TIMEOUT=8 hours` (automatic logout)

For HTTPS connections, also enable:
- `SESSION_COOKIE_SECURE=True` (only send over encrypted connection)

## 📊 Performance Tuning

### Number of Workers
The startup scripts default to 4 workers. Adjust based on:
- **CPU Cores**: Use 2-4 × number of CPU cores
- **Memory**: Each worker uses ~50-100MB RAM
- **Guests**: For <20 guests, 4 workers is usually sufficient

Example for 8-core system:
```bash
gunicorn --workers=16 --bind=0.0.0.0:5000 app:app
```

### Connection Handling
- **Timeout**: 120 seconds (suitable for party environment)
- **Worker Class**: `sync` (good for I/O-bound web apps)
- **Thread Support**: Enabled for concurrent requests

## 🌐 Network Access

### Local Network (Same Building)
1. Find your computer's IP:
   - **Windows**: `ipconfig` (look for IPv4 Address)
   - **Linux/macOS**: `ifconfig` or `ip addr`

2. Access from another device:
   - Guests: `http://YOUR_IP:5000`
   - Moderator: Same URL, click "🔓 Moderator" and enter password

### Port Forwarding (External Access)
⚠️ **WARNING**: Only do this if you understand the security implications.

```bash
# If using router:
# Forward port 5000 (or custom) to your computer's IP
# Check your router's manual for port forwarding instructions

# Then access with:
# http://YOUR_PUBLIC_IP:5000
```

## 📝 Logging & Monitoring

### View Application Logs
The startup scripts output logs in real-time. Look for:
```
INFO: Application startup complete
INFO: 127.0.0.1 GET /spieluebersicht HTTP/1.1 200
ERROR: [Your message if something goes wrong]
```

### Log Files (if configured)
- Console output during startup is the primary log
- No file logs are created by default (can be added)

### Monitor during party
- Keep terminal visible to see requests
- Watch for any ERROR messages
- Session/connection issues appear as warnings

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change port in .env.production or command line:
export FLASK_PORT=8080
gunicorn --bind=0.0.0.0:8080 app:app
```

### Permission Denied (Linux/macOS)
```bash
# Make startup script executable
chmod +x run-production.sh
```

### Import Errors / Missing Packages
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements-prod.txt
```

### Slow Performance
- Reduce number of workers (if high memory usage)
- Check if antivirus is scanning your app directory
- Monitor CPU/RAM with system tools

### Session Not Persisting
- Ensure cookies are enabled in browser
- Check that `SECRET_KEY` is consistent across restarts
- Verify `SESSION_COOKIE_HTTPONLY` is True

## 📋 Environment Variables Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `FLASK_ENV` | development | Set to `production` for deployment |
| `FLASK_DEBUG` | True | Set to `False` in production |
| `FLASK_HOST` | 0.0.0.0 | Server bind address (0.0.0.0 = all interfaces) |
| `FLASK_PORT` | 5000 | Server port number |
| `SECRET_KEY` | default key | Session encryption - change this! |
| `SESSION_COOKIE_SECURE` | False | True = only send over HTTPS |
| `SESSION_COOKIE_HTTPONLY` | True | Prevent JavaScript from accessing cookies |
| `SESSION_COOKIE_SAMESITE` | Lax | CSRF protection level |
| `PERMANENT_SESSION_LIFETIME` | 28800 | Session timeout in seconds (8 hours) |

## 🛠️ Advanced: Docker Deployment

### Dockerfile
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

COPY . .

ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000

EXPOSE 5000

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "app:app"]
```

### Build and Run
```bash
# Build image
docker build -t davids-party:latest .

# Run container
docker run -p 5000:5000 \
  -e SECRET_KEY="your-secure-key" \
  -e FLASK_ENV=production \
  davids-party:latest
```

## 📞 Support

### Common Issues
1. **Can't access from other computer**
   - Check firewall allows port 5000
   - Verify you're using correct IP address
   - Try disabling antivirus temporarily

2. **Password reset/changes**
   - Edit `app.py` password validation
   - Restart application

3. **Performance issues**
   - Reduce worker count and restart
   - Check system RAM/CPU usage
   - Clear browser cache

### Testing Before Party
1. Start server: `./run-production.bat` (or `.sh`)
2. Access locally: `http://localhost:5000`
3. Test on another device: `http://YOUR_IP:5000`
4. Run all games, test moderator functions
5. Verify points update in real-time
6. Test logout and re-login

## 🎊 You're Ready!

Your application is production-ready. The startup scripts handle:
- ✅ Virtual environment management
- ✅ Dependency installation
- ✅ Environment configuration loading
- ✅ Secure key generation if needed
- ✅ Gunicorn worker optimization
- ✅ Real-time logging

Simply run the startup script and enjoy the party! 🎉
