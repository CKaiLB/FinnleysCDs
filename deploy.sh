echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting Gunicorn..."
gunicorn --config gunicorn_config.py wsgi:app