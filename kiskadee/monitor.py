import kiskadee.database


def sync_db_cache():
    """loads db pkg-version information in redis"""
    data = kiskadee.database.get_analyzed_software()
    kiskadee.database.update_cached_data(data)


def monitor_repository():
    pass
