from __future__ import annotations
import logging, coloredlogs
from decorate_decorator import apply_logger

logger = logging.getLogger(__name__)
apply_names = ["__main__", "decorate_decorator"]
for logger_name in apply_names:
    coloredlogs.install(level="DEBUG", logger=logging.getLogger(logger_name))


@apply_logger()
class A:
    def a(self):
        pass

    def b(self):
        pass


if __name__ == "__main__":
    a = A()
    a.a()
    a.b()
