"""Module for database abstractions

This module implements some functions to deal with both the kiskadee db
and cached data with package versions.
"""
import sqlalchemy

# This should be somewhere else and use a config file
# redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)


def get_db_data():
    """retrieves all packages and versions from kiskadee database"""
    return {}


# def update_cache(plugin, package, version):
    # """adds or updates an entry to the cached data"""
    # redis_db.set(':'.join([plugin, package]), version)
