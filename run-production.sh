#!/bin/bash
# Production startup script for David's 30th Birthday Party application

set -e

echo "🎉 Starting David's 30th Birthday Party - Production Deployment"
echo "=============================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9 or later."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install/upgrade production dependencies
echo "📥 Installing production dependencies..."
pip install --upgrade pip
pip install -r requirements-prod.txt

# Load environment configuration
if [ -f ".env.production" ]; then
    echo "📄 Loading production environment from .env.production..."
    set -a
    source .env.production
    set +a
else
    echo "⚠️  .env.production not found. Using default configuration."
fi

# Set production mode
export FLASK_ENV=production
export FLASK_DEBUG=False

# Generate secure SECRET_KEY if not set
if [ -z "$SECRET_KEY" ]; then
    echo "🔐 Generating secure SECRET_KEY..."
    export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    echo "   Generated: $SECRET_KEY"
    echo "   Add this to .env.production for consistency across restarts"
fi

# Number of Gunicorn workers (4x CPU cores recommended)
WORKERS=${GUNICORN_WORKERS:-4}

echo ""
echo "🚀 Launching Gunicorn with configuration:"
echo "   Workers: $WORKERS"
echo "   Host: ${FLASK_HOST:-0.0.0.0}"
echo "   Port: ${FLASK_PORT:-5000}"
echo "   Environment: production"
echo ""
echo "📌 Access the application at: http://${FLASK_HOST:-0.0.0.0}:${FLASK_PORT:-5000}"
echo "📌 Press Ctrl+C to stop the server"
echo ""

# Start Gunicorn
gunicorn \
    --workers=$WORKERS \
    --worker-class=sync \
    --bind=${FLASK_HOST:-0.0.0.0}:${FLASK_PORT:-5000} \
    --timeout=120 \
    --access-logfile=- \
    --error-logfile=- \
    --log-level=info \
    app:app
