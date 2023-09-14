# coding: utf-8

from functools import wraps
import inspect
import logging
import time

logger = logging.getLogger(__name__)


# メソッドの開始、終了、プロセス時間を表示するデコレータ
def debug_log(func):
    @wraps(func)
    def inner_func(*args, **kwargs):
        # 前処理
        logger.debug(f"START: {func.__name__}")
        start_time = time.time()
        # メソッドの実行
        result = func(*args, **kwargs)
        # 後処理
        end_time = time.time()
        logger.debug(f"END: {func.__name__}")
        logger.debug(f"PROCESS TIME: {end_time - start_time:.3f} sec")
        # Return the return value
        return result

    return inner_func


# クラス内のメソッドに対してデコレータを適用するデコレータ
def apply_dubug_log(exclude=[]):
    # デコレータを適用する処理
    def decorate(cls):
        for name, fn in inspect.getmembers(cls):
            if name.startswith("__"):
                continue
            if callable(getattr(cls, name)) and not name in exclude:
                setattr(cls, name, debug_log(fn))
        return cls

    return decorate
