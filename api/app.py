from app import app, init_db

# Ensure DB is initialized when the app is started by the platform
init_db()

# The hosting platform (Vercel/Gunicorn/etc.) will import this module
# and look for a WSGI application object named `app`.

# Expose `app` as the callable WSGI application
# (already provided by the imported `app` variable)

application = app
