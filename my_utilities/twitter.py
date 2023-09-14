import os
import urllib
from datetime import datetime
from pprint import pprint, pformat
import logging

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement

logger = logging.getLogger(__name__)

# TODO: 全部改修


class TwitterManager:
    """Twitterに投稿するクラス"""

    def __init__(self, profile_path: str, is_headless: bool = True) -> None:
        """コンストラクタ"""
        # ブラウザのオプション
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        if is_headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f"--user-data-dir={profile_path}")

        # ブラウザを開く
        self.driver = webdriver.Chrome(options)

        return None

    def login(self, id: str, password: str) -> None:
        """Twitterにログインする"""
        driver: WebElement = webdriver.Chrome(options)

        # ログインページを開く
        driver.get("https://twitter.com/login/")

        # IDの入力
        element_account = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))
        element_account.send_keys(id)

        # 次へボタンクリック
        element_login_next = driver.find_element(By.XPATH, '//div/span/span[text()="次へ"]')
        element_login_next.click()

        # パスワード入力
        element_pass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        element_pass.send_keys(password)

        # ログインボタンクリック
        element_login = driver.find_element(By.XPATH, '//div/span/span[text()="ログイン"]')
        element_login.click()

        return None

    @staticmethod
    def tweet(tweet_text: str, schedule_iso: str = None) -> None:
        """時刻指定でTweetを予約する"""
        driver = TwitterManager.driver

        # URLエンコード
        tweet_text = urllib.parse.quote(tweet_text, safe="")

        # ページを開く
        driver.get(f"https://twitter.com/compose/tweet?text={tweet_text}")

        # 投稿予約
        if schedule_iso != None:
            # 予約時刻をdatetime型に変換
            schedule = datetime.fromisoformat(schedule_iso)

            # 予約画面に遷移する
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-label="ツイートを予約"]')))
            driver.find_element(By.XPATH, '//div[@aria-label="ツイートを予約"]').click()

            # 日時を設定
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-label="日付"]')))
            select = Select(driver.find_element(By.XPATH, '//select[@aria-labelledby="SELECTOR_1_LABEL"]'))
            select.select_by_value(str(schedule.month))
            select = Select(driver.find_element(By.XPATH, '//select[@aria-labelledby="SELECTOR_2_LABEL"]'))
            select.select_by_value(str(schedule.day))
            select = Select(driver.find_element(By.XPATH, '//select[@aria-labelledby="SELECTOR_3_LABEL"]'))
            select.select_by_value(str(schedule.year))

            # 時刻を設定
            select = Select(driver.find_element(By.XPATH, '//select[@aria-labelledby="SELECTOR_4_LABEL"]'))
            select.select_by_value(str(schedule.hour))
            select = Select(driver.find_element(By.XPATH, '//select[@aria-labelledby="SELECTOR_5_LABEL"]'))
            select.select_by_value(str(schedule.minute))

            # ツイート画面に戻る
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="scheduledConfirmationPrimaryAction"]')))
            driver.find_element(By.XPATH, '//div[@data-testid="scheduledConfirmationPrimaryAction"]').click()

        # 投稿する
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="tweetButton"]')))
        driver.find_element(By.XPATH, '//div[@data-testid="tweetButton"]').click()
        print("ツイートしました")

        return None

    @staticmethod
    def tweets(tweets: list[tuple]) -> None:
        """複数のツイートを投稿する"""
        for tweet in tweets:
            TwitterManager.tweet(tweet[0], tweet[1])

        return None
