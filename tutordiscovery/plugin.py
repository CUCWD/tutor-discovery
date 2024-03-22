from glob import glob
import os

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

config = {
    "add": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SECRET_KEY": "{{ 20|random_string }}",
        "OAUTH2_SECRET": "{{ 8|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 8|random_string }}",
    },
    "defaults": {
        "VERSION": __version__,
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY}}overhangio/openedx-discovery:{{ DISCOVERY_VERSION }}",
        "HOST": "discovery.{{ LMS_HOST }}",
        "INDEX_OVERRIDES": {},
        "MYSQL_DATABASE": "discovery",
        "MYSQL_HOSTNETWORK_EAST_1A_PUBLIC": "172.16.16.0/255.255.240.0",  # AWS VPC subnet 'edx-prod-us-east-1a-public' versus all hosts '%' since Docker containers NAT out.
        "MYSQL_HOSTNETWORK_EAST_1B_PUBLIC": "172.16.14.0/255.255.240.0",  # AWS VPC subnet 'edx-prod-us-east-1b-public' versus all hosts '%' since Docker containers NAT out.
        "MYSQL_USERNAME": "discovery",
        "OAUTH2_KEY": "discovery",
        "OAUTH2_KEY_DEV": "discovery-dev",
        "OAUTH2_KEY_SSO": "discovery-sso",
        "OAUTH2_KEY_SSO_DEV": "discovery-sso-dev",
        "CACHE_REDIS_DB": "{{ OPENEDX_CACHE_REDIS_DB }}",
    },
}

hooks = {
    "build-image": {"discovery": "{{ DISCOVERY_DOCKER_IMAGE }}"},
    "remote-image": {"discovery": "{{ DISCOVERY_DOCKER_IMAGE }}"},
    "pre-init": ["mysql"],
    "init": ["lms", "discovery"],
}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
