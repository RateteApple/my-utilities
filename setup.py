from setuptools import setup, find_packages

setup(
    name="my_utilies",  # パッケージ名
    version="0.1.0",  # バージョン
    description="小規模な処理をまとめたモジュール",  # パッケージの説明
    author="Ratete",  # 作者名
    packages=find_packages(),  # 使うモジュール一覧を指定する
    license="MIT",  # ライセンス
)
