from functools import wraps
import inspect
import logging
import time

# FIXME: inspectモジュールを使わない方が処理が軽いかも


# 実行時間を計測するデコレータ
def execute_time(exclude: tuple = ()):
    def decorate(target):
        # クラスに対してはメソッドをデコレートする
        if inspect.isclass(target):
            return decorate_class(target)
        # 関数に対してはそのままデコレートする
        elif inspect.isfunction(target):
            return decorate_method(target)

    # クラスデコレータ
    def decorate_class(cls):
        for name, func in inspect.getmembers(cls):
            # メソッドに絞り込む
            if not inspect.isfunction(func):
                continue
            # マジックメソッドやプライベートメソッドは除外
            if name[:2] == "__":
                continue
            # excludeに指定されたメソッドは除外
            if name in exclude:
                continue

            # メソッドをデコレート
            setattr(cls, name, decorate_method(func))
        return cls

    # 関数デコレータ
    def decorate_method(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # ロガーの取得
            logger = logging.getLogger(func.__module__)
            # 前処理
            logger.debug(f"START:{func.__name__}")  # 開始を通知
            start_time = time.time()
            # 対象の関数を実行
            result = func(*args, **kwargs)
            # 後処理
            end_time = time.time()
            logger.debug(f"END:  {func.__name__}   {end_time - start_time:.3f} sec")  # 終了を通知
            return result

        return wrapper

    return decorate
