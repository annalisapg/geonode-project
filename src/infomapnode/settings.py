# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import os
import ast

try:
    from urllib.parse import urlparse, urlunparse
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
    from urlparse import urlparse, urlunparse
# Load more settings from a file called local_settings.py if it exists
try:
    from infomapnode.local_settings import *
#    from geonode.local_settings import *
except ImportError:
    from geonode.settings import *

#
# General Django development settings
#
PROJECT_NAME = 'infomapnode'

# add trailing slash to site url. geoserver url will be relative to this
if not SITEURL.endswith('/'):
    SITEURL = '{}/'.format(SITEURL)

SITENAME = os.getenv("SITENAME", 'infomapnode')

# Defines the directory that contains the settings file as the LOCAL_ROOT
# It is used for relative settings elsewhere.
LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', "en")

LANGUAGES = (
    ('en-us', 'English'),
    ('fr-fr', 'Français'),
    ('ar-ar', 'Arabic')
)

if PROJECT_NAME not in INSTALLED_APPS:
    INSTALLED_APPS += (PROJECT_NAME,)

# Location of url mappings
ROOT_URLCONF = os.getenv('ROOT_URLCONF', '{}.urls'.format(PROJECT_NAME))

# Additional directories which hold static files
# - Give priority to local geonode-project ones
STATICFILES_DIRS = [os.path.join(LOCAL_ROOT, "static"), ] + STATICFILES_DIRS

# Location of locale files
LOCALE_PATHS = (
    os.path.join(LOCAL_ROOT, 'locale'),
    ) + LOCALE_PATHS

TEMPLATES[0]['DIRS'].insert(0, os.path.join(LOCAL_ROOT, "templates"))
loaders = TEMPLATES[0]['OPTIONS'].get('loaders') or ['django.template.loaders.filesystem.Loader','django.template.loaders.app_directories.Loader']
# loaders.insert(0, 'apptemplates.Loader')
TEMPLATES[0]['OPTIONS']['loaders'] = loaders
TEMPLATES[0].pop('APP_DIRS', None)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '%(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"], "level": "ERROR", },
        "geonode": {
            "handlers": ["console"], "level": "INFO", },
        "geoserver-restconfig.catalog": {
            "handlers": ["console"], "level": "ERROR", },
        "owslib": {
            "handlers": ["console"], "level": "ERROR", },
        "pycsw": {
            "handlers": ["console"], "level": "ERROR", },
        "celery": {
            "handlers": ["console"], "level": "DEBUG", },
        "mapstore2_adapter.plugins.serializers": {
            "handlers": ["console"], "level": "DEBUG", },
        "geonode_logstash.logstash": {
            "handlers": ["console"], "level": "DEBUG", },
    },
}

CENTRALIZED_DASHBOARD_ENABLED = ast.literal_eval(os.getenv('CENTRALIZED_DASHBOARD_ENABLED', 'False'))
if CENTRALIZED_DASHBOARD_ENABLED and USER_ANALYTICS_ENABLED and 'geonode_logstash' not in INSTALLED_APPS:
    INSTALLED_APPS += ('geonode_logstash',)

    CELERY_BEAT_SCHEDULE['dispatch_metrics'] = {
        'task': 'geonode_logstash.tasks.dispatch_metrics',
        'schedule': 3600.0,
    }

LDAP_ENABLED = ast.literal_eval(os.getenv('LDAP_ENABLED', 'False'))
if LDAP_ENABLED and 'geonode_ldap' not in INSTALLED_APPS:
    INSTALLED_APPS += ('geonode_ldap',)

# Add your specific LDAP configuration after this comment:
# https://docs.geonode.org/en/master/advanced/contrib/#configuration

DEFAULT_MS2_BACKGROUNDS = [
    #{
    #    "type": "osm",
    #    "title": "Open Street Map",
    #    "name": "mapnik",
    #    "source": "osm",
    #    "group": "background",
    #    "visibility": False,
    #},
    {
        "type": "tileprovider",
        "title": "OpenTopoMap",
        "provider": "OpenTopoMap",
        "name": "OpenTopoMap",
        "source": "OpenTopoMap",
        "group": "background",
        "visibility": False,
    },
    {
        "type": "wms",
        "title": "Sentinel-2 cloudless - https://s2maps.eu",
        "format": "image/jpeg",
        "id": "s2cloudless",
        "name": "s2cloudless:s2cloudless",
        "url": "https://maps.geosolutionsgroup.com/geoserver/wms",
        "group": "background",
        "thumbURL": f"{SITEURL}static/mapstorestyle/img/s2cloudless-s2cloudless.png",
        "visibility": False,
    },
    {
        "source": "ol",
        "group": "background",
        "id": "none",
        "name": "empty",
        "title": "Empty Background",
        "type": "empty",
        "visibility": False,
        "args": ["Empty Background", {"visibility": False}],
    },
]

if MAPBOX_ACCESS_TOKEN:
    BASEMAP = {
        "type": "tileprovider",
        "title": "MapBox streets-v11",
        "provider": "MapBoxStyle",
        "name": "MapBox streets-v11",
        "accessToken": f"{MAPBOX_ACCESS_TOKEN}",
        "source": "streets-v11",
        "thumbURL": f"https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/256/6/33/23?access_token={MAPBOX_ACCESS_TOKEN}",  # noqa
        "group": "background",
        "visibility": True,
    }
    DEFAULT_MS2_BACKGROUNDS = [
        BASEMAP,
    ] + DEFAULT_MS2_BACKGROUNDS

if BING_API_KEY:
    BASEMAP = {
        "type": "bing",
        "title": "Bing Aerial",
        "name": "AerialWithLabels",
        "source": "bing",
        "group": "background",
        "apiKey": "{{apiKey}}",
        "visibility": True,
    }
    DEFAULT_MS2_BACKGROUNDS = [
        BASEMAP,
    ] + DEFAULT_MS2_BACKGROUNDS

MAPSTORE_BASELAYERS = DEFAULT_MS2_BACKGROUNDS

# OpenLDAP settings
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType
import logging

logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

AUTHENTICATION_BACKENDS = (
    'infomapnode.backend.IMNLDAPBackend',
) + AUTHENTICATION_BACKENDS

AUTH_LDAP_SERVER_URI = os.getenv(
    'AUTH_LDAP_SERVER_URI', 'ldap://localhost:389'
)

AUTH_LDAP_BIND_DN = os.getenv(
    'AUTH_LDAP_BIND_DN', 'cn=admin,dc=example,dc=org'
)

AUTH_LDAP_BIND_PASSWORD = os.getenv(
    'AUTH_LDAP_BIND_PASSWORD', 'password'
)

AUTH_LDAP_USER_BASE_SEARCH = os.getenv(
    'AUTH_LDAP_USER_BASE_SEARCH', 'dc=example,dc=org'
)

AUTH_LDAP_USER_SEARCH_ATTR = os.getenv(
    'AUTH_LDAP_USER_SEARCH_ATTR', 'uid'
)

AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_USER_BASE_SEARCH,
    ldap.SCOPE_SUBTREE,
    "({}=%(user)s)".format(AUTH_LDAP_USER_SEARCH_ATTR),
)

DJANGO_USER_ATTR_1 = os.getenv('DJANGO_USER_ATTR_1', 'first_name')
LDAP_USER_ATTR_1 = os.getenv('LDAP_USER_ATTR_1', 'givenName')
DJANGO_USER_ATTR_2 = os.getenv('DJANGO_USER_ATTR_2', 'last_name')
LDAP_USER_ATTR_2 = os.getenv('LDAP_USER_ATTR_2', 'sn')
DJANGO_USER_ATTR_3 = os.getenv('DJANGO_USER_ATTR_3', 'email')
LDAP_USER_ATTR_3 = os.getenv('LDAP_USER_ATTR_3', 'mail')
DJANGO_USER_ATTR_4 = os.getenv('DJANGO_USER_ATTR_4', 'username')
LDAP_USER_ATTR_4 = os.getenv('LDAP_USER_ATTR_4', 'uid')

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    DJANGO_USER_ATTR_1: LDAP_USER_ATTR_1,
    DJANGO_USER_ATTR_2: LDAP_USER_ATTR_2,
    DJANGO_USER_ATTR_3: LDAP_USER_ATTR_3,
    DJANGO_USER_ATTR_4: LDAP_USER_ATTR_4,
}

AUTH_LDAP_ALWAYS_UPDATE_USER = strtobool(
    os.getenv(
        'AUTH_LDAP_ALWAYS_UPDATE_USER', 'True'
    )
)

#Set up the basic group parameters.
LDAP_GROUP_OBJECTCLASS = os.getenv(
    'LDAP_GROUP_OBJECTCLASS', '(objectClass=GroupOfUniqueNames)'
)
LDAP_GROUP_BASE_SEARCH = os.getenv(
    'LDAP_GROUP_BASE_SEARCH', 'ou=groups,dc=example,dc=org'
)

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    LDAP_GROUP_BASE_SEARCH,
    ldap.SCOPE_SUBTREE,
    LDAP_GROUP_OBJECTCLASS
)

AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType(name_attr='cn')

LDAP_GROUP_STAFF_DN = os.getenv(
    'LDAP_GROUP_STAFF_DN', 'cn=staff,ou=groups,dc=example,dc=org'
)

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_staff": LDAP_GROUP_STAFF_DN,
}

AUTH_LDAP_MIRROR_GROUPS = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = strtobool(
    os.getenv(
        'AUTH_LDAP_FIND_GROUP_PERMS', 'True'
    )
)

# Use OU attribute to assign groups membership
IMN_AUTH_LDAP_OU_SEPARATOR = '|'
IMN_AUTHORIZE_USERS_FROM_OU = True
