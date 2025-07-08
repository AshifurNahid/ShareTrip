INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.users',  # Make sure this is correct
    'apps.bookings',
    'apps.trips',  # If you have this app
]

AUTH_USER_MODEL = 'users.User'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Remove or comment out STATICFILES_DIRS if the directory doesn't exist
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]