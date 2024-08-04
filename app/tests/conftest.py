import pytest

class VerboseOnFailurePlugin:
    def __init__(self, config):
        self.config = config
        self.verbose = False

    def pytest_runtest_logreport(self, report):
        if report.failed and not self.verbose:
            self.config.option.verbose = 1
            self.verbose = True

def pytest_configure(config):
    config.pluginmanager.register(VerboseOnFailurePlugin(config), "verbose_on_failure")

def pytest_unconfigure(config):
    verbose_plugin = config.pluginmanager.get_plugin("verbose_on_failure")
    if verbose_plugin and verbose_plugin.verbose:
        print("\nDetailed output due to test failures:")