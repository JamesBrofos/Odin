import os
from .params import IOFiles


def odin_init(sname):
    """This function creates a directory with the necessary substructure for
    Odin to run a trading algorithm within it. Specifically, it creates a folder
    with the desired strategy name within the current directory. It then creates
    a subdirectory 'history' that contains relevant data on the portfolio; it
    also creates a file 'main.py' that is executed in order to perform trading.

    Usage
    -----
    This code can be used from the command line as follows:
        python3 -c "from odin.utilities import odin_init ; odin_init('strat')"

    Parameters
    ----------
    sname: String.
        A string giving an identifier to the directory that will house the
        implementation of the strategy and dependency files.
    """
    path = "./" + sname + "/"
    main = path + IOFiles.main_file.value
    handlers = path + IOFiles.handlers_file.value
    settings = path + IOFiles.settings_file.value
    strategy = path + IOFiles.strategy_file.value
    fund = path + IOFiles.fund_file.value
    # Create files and directories.
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.path.isfile(main):
        open(main, "a").close()
    if not os.path.isfile(handlers):
        open(handlers, "a").close()
    if not os.path.isfile(settings):
        open(settings, "a").close()
    if not os.path.isfile(strategy):
        open(strategy, "a").close()
    if not os.path.isfile(fund):
        open(fund, "a").close()



