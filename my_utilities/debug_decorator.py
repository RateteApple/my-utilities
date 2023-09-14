# coding: utf-8

from functools import wraps
import inspect
import logging
import time


# 引数付きデコレータを作成するデコレータ
def paramdeco(func):
    # from:https://qiita.com/nshinya/items/b6746a0c07e9e20389e8
    @wraps(func)
    def param(*args, **kwargs):
        def wrapper(f):
            return func(f, *args, **kwargs)

        return wrapper

    return param


# デバッグログを出力する関数デコレータ
@paramdeco
def output_debug(func, logger: logging.Logger):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 前処理
        logger.debug(f"START: {func.__name__}")  # 開始を通知
        start_time = time.time()

        # 対象の関数を実行
        result = func(*args, **kwargs)

        # 後処理
        end_time = time.time()
        logger.debug(f"END:   {func.__name__}")  # 終了を通知
        logger.debug(f"PROCESS TIME: {end_time - start_time:.3f} sec")  # プロセス時間を表示

        # 結果を返す
        return result

    return wrapper


# デバッグデコレータをメソッドに適用するクラスデコレータ
def apply_output_debug(logger: logging.Logger, exclude: list = []):
    # デコレータを適用する処理
    def decorate(cls):
        for name, fn in inspect.getmembers(cls):
            if name.startswith("__"):  # マジックメソッドは除外
                continue
            if callable(getattr(cls, name)) and not name in exclude:  # excludeに指定されたメソッド以外に適用
                setattr(cls, name, _output_debug(fn))
        return cls

    # デバッグログを出力する関数デコレータ
    def _output_debug(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 前処理
            logger.debug(f"START: {func.__name__}")  # 開始を通知
            start_time = time.time()

            # 対象の関数を実行
            result = func(*args, **kwargs)

            # 後処理
            end_time = time.time()
            logger.debug(f"END:   {func.__name__}")  # 終了を通知
            logger.debug(f"PROCESS TIME: {end_time - start_time:.3f} sec")  # プロセス時間を表示

            # 結果を返す
            return result

        return wrapper

    return decorate
