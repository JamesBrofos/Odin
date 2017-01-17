import os
import shutil
import unittest
from odin.utilities import odin_init
from odin.utilities.params import IOFiles


class OdinInitTest(unittest.TestCase):
    def test_odin_init(self):
        # Create a test file.
        path = "./test_portfolio_id/"
        main = path + IOFiles.main_file.value
        handlers = path + IOFiles.handlers_file.value
        settings = path + IOFiles.settings_file.value
        strategy = path + IOFiles.strategy_file.value
        fund = path + IOFiles.fund_file.value
        odin_init(path)
        # Assert that all of the requisite files exist.
        self.assertTrue(os.path.isdir(path))
        self.assertTrue(os.path.isfile(main))
        self.assertTrue(os.path.isfile(handlers))
        self.assertTrue(os.path.isfile(settings))
        self.assertTrue(os.path.isfile(strategy))
        self.assertTrue(os.path.isfile(fund))
        shutil.rmtree(path)


if __name__ == "__main__":
    unittest.main()
