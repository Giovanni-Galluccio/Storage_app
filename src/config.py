
from support_functions import configure_sqlite, configure_postgres, setup_config, load_config


def get_config():
    config = load_config()
    if config == None:
        config = setup_config()
    
