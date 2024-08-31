from dfk_commons.classes import TablesManager


def get_tables_manager(isProd):
    return TablesManager(isProd)