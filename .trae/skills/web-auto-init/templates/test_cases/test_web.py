import os

from pytest_bdd import scenarios

from test_cases.steps import *  # noqa

scenarios(os.getcwd())
