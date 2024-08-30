"""Main module of ydata-profiling.

.. include:: ../../README.md
"""

# ignore numba warnings
import warnings  # isort:skip # noqa
from numba.core.errors import NumbaDeprecationWarning  # isort:skip # noqa

warnings.simplefilter("ignore", category=NumbaDeprecationWarning)

import importlib.util  # isort:skip # noqa

from data_analyser.compare_reports import compare  # isort:skip # noqa
from data_analyser.controller import pandas_decorator  # isort:skip # noqa
from data_analyser.profile_report import ProfileReport  # isort:skip # noqa
from data_analyser.version import __version__  # isort:skip # noqa

# backend
import data_analyser.model.pandas  # isort:skip  # noqa

spec = importlib.util.find_spec("pyspark")
if spec is not None:
    import data_analyser.model.spark  # isort:skip  # noqa


__all__ = [
    "pandas_decorator",
    "ProfileReport",
    "__version__",
    "compare",
]
