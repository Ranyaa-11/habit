from app import app, init_db

# Ensure DB is initialized when the app is started by the platform
# Wrap in try-except to handle any initialization errors gracefully
try:
    init_db()
except Exception as e:
    # Log the error but don't crash - the app can still run
    # The database will be created on first use if initialization fails
    print(f"Warning: Database initialization failed: {e}")

# The hosting platform (Vercel/Gunicorn/etc.) will import this module
# and look for a WSGI application object named `app`.

# Expose `app` as the callable WSGI application
# (already provided by the imported `app` variable)

application = app
