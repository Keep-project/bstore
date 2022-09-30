import dj_database_url
from bstore.settings import *
from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name, default_value=None):

    try:
        return os.environ.get(var_name)
    except KeyError:
        if default_value is None:
            error_msg = "Set the {0} environment variable".format(var_name)
            raise ImproperlyConfigured(error_msg)
        else:
            return default_value

# SECRET_KEY = get_env_variable('SECRET_KEY', 'e4g2)*lwyaw5w*9$)xz+9zy4poae(ui_2*lh@v59e!w9si3kn5')


DEBUG = False
TEMPLATES_DEBUG = False

ALLOWED_HOST = ['*']


DATABASES['default'] = dj_database_url.config()

MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware',]


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'