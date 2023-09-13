from __future__ import annotations
import logging, coloredlogs


logger = logging.getLogger(__name__)
coloredlogs.install(level="DEBUG", logger=logger)


def test_apply_logger():
    from my_utilies.decorate_decorator import apply_logger

    coloredlogs.install(level="DEBUG", logger=logging.getLogger("my_utilies.decorate_decorator"))

    @apply_logger()
    class A:
        def a(self):
            pass

        def b(self):
            pass

    a = A()
    a.a()
    a.b()


if __name__ == "__main__":
    test_apply_logger()
