from .odin_enum import OdinEnum


class IOFiles(OdinEnum):
    """Odin Input/Output Parameters

    This module contains constants for specifying universal file names and
    directories that Odin uses to store pertinent information about funds and
    portfolios on the local disk. This allows for persistence across multiple
    sessions.
    """
    # Resource files when setting up a fund for trading.
    handlers_file = "handlers.py"
    settings_file = "settings.py"
    strategy_file = "strategy.py"
    fund_file = "fund.py"
    main_file = "main.py"
    # Date formatting string.
    date_format = "%Y-%m-%d %H:%M:%S"
