# coding:utf-8

import asyncio
from googleapiclient.discovery import build
from google.oauth2 import service_account
from pprint import pprint, pformat
import logging

logger = logging.getLogger(__name__)


class GoogleCalendarClient:
    def __init__(self, credentials_path):
        self.credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=["https://www.googleapis.com/auth/calendar"])
        self.service = build("calendar", "v3", credentials=self.credentials)

    # カレンダーを作成する関数
    async def create_calendar(self, summary, time_zone) -> str:
        """カレンダーを作成する

        Args:
            summary (str): カレンダーのタイトル
            time_zone (str): カレンダーのタイムゾーン

        Returns:
            str: 作成したカレンダーのID
        """

        def create_calendar_sync():
            calendar = {
                "summary": summary,
                "timeZone": time_zone,
            }
            created_calendar = self.service.calendars().insert(body=calendar).execute()
            logger.info(f'created calendar   ID:{created_calendar["id"]}')
            return created_calendar["id"]

        loop = asyncio.get_running_loop()
        calendar_id = await loop.run_in_executor(None, create_calendar_sync)
        return calendar_id

    # カレンダーを削除する関数
    async def delete_calendar(self, calendar_id) -> None:
        """カレンダーを削除する

        Args:
            calendar_id (str): 削除するカレンダーのID

        Returns:
            None
        """

        def delete_calendar_sync():
            self.service.calendars().delete(calendarId=calendar_id).execute()
            logger.info(f"deleted calendar   ID:{calendar_id}")

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, delete_calendar_sync)

    # カレンダーの一覧を取得する関数
    async def get_all_calendars(self) -> list:
        """すべてのカレンダーの一覧を取得する

        Returns:
            list: カレンダーの一覧（辞書のリスト）
        """

        def get_calendars_sync():
            calendars_result = self.service.calendarList().list().execute()
            calendars = calendars_result.get("items", [])
            logger.info(f"get all calendars")
            return calendars

        loop = asyncio.get_running_loop()
        calendars = await loop.run_in_executor(None, get_calendars_sync)
        return calendars

    # カレンダーを一般公開にする関数
    async def make_calendar_public(self, calendar_id) -> dict:
        # カレンダーの一般公開設定を更新
        rules = {
            "role": "reader",
            "scope": {
                "type": "default",
            },
        }
        created_rule = self.service.acl().insert(calendarId=calendar_id, body=rules).execute()
        logger.info(f"made calendar public   ID:{calendar_id}")

        return created_rule

    # イベントを作成する関数
    async def create_event(self, calendar_id, event) -> dict:
        """イベントを作成する

        Args:
            calendar_id (str): イベントを作成するカレンダーのID
            event (dict): イベントの情報

        Returns:
            dict: 作成したイベントの情報
        """

        def create_event_sync():
            created_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
            logger.info(f'created event   ID:{created_event["id"]}')
            return created_event

        loop = asyncio.get_running_loop()
        created_event = await loop.run_in_executor(None, create_event_sync)
        return created_event

    # イベントの詳細を取得する関数
    async def get_event_details(self, calendar_id, event_id) -> dict:
        """イベントの詳細を取得する

        Args:
            calendar_id (str): イベントの詳細を取得するカレンダーのID
            event_id (str): 取得するイベントのID

        Returns:
            dict: イベントの詳細
        """

        def get_event_details_sync():
            event = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
            logger.info(f'get event details   ID:{event["id"]}')
            return event

        loop = asyncio.get_running_loop()
        event = await loop.run_in_executor(None, get_event_details_sync)
        return event

    # イベントを削除する関数
    async def delete_event(self, calendar_id, event_id) -> None:
        """イベントを削除する

        Args:
            calendar_id (str): イベントを削除するカレンダーのID
            event_id (str): 削除するイベントのID

        Returns:
            None
        """

        def delete_event_sync():
            self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            logger.info(f"deleted event   ID:{event_id}")

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, delete_event_sync)

    # イベントを更新する関数
    async def update_event(self, calendar_id, event_id, updated_event) -> dict:
        """イベントを更新する

        Args:
            calendar_id (str): イベントを更新するカレンダーのID
            event_id (str): 更新するイベントのID
            updated_event (dict): 更新するイベントの情報

        Returns:
            dict: 更新したイベントの情報
        """

        def update_event_sync():
            updated_event = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=updated_event).execute()
            logger.info(f'updated event   ID:{updated_event["id"]}')
            return updated_event

        loop = asyncio.get_running_loop()
        updated_event = await loop.run_in_executor(None, update_event_sync)
        return updated_event

    # イベントを別のカレンダーにコピーする関数
    async def copy_event_to_calendar(self, event_id, source_calendar_id, destination_calendar_id, id_retention: bool = False) -> dict:
        """イベントを別のカレンダーにコピーする

        Args:
            event_id (str): コピーするイベントのID
            source_calendar_id (str): コピー元のカレンダーのID
            destination_calendar_id (str): コピー先のカレンダーのID

        Returns:
            dict: コピーしたイベントの情報
        """

        async def copy_event_async():
            # コピー元のイベントの詳細を取得
            event = await self.get_event_details(calendar_id=source_calendar_id, event_id=event_id)
            if id_retention == False:
                # 必要な部分だけ抽出
                event = {
                    "summary": event["summary"],
                    "description": event["description"],
                    "start": event["start"],
                    "end": event["end"],
                    "reminders": event["reminders"],
                    "creator": event["creator"],
                }
            # イベントをコピー
            copied_event = await self.create_event(calendar_id=destination_calendar_id, event=event)
            logger.info(f"copied event   {source_calendar_id}→{destination_calendar_id}")
            logger.debug(
                f'copied event\n source_calendar_id:{source_calendar_id} source_event_id:{event_id}\n→destination_calendar_id:{destination_calendar_id} destination_event_id:{copied_event["id"]}'
            )
            return copied_event

        copied_event = await copy_event_async()
        return copied_event

    # 登録されているイベントの一覧を取得する関数
    async def get_all_events(self, calendar_id, limit=None, timemin=None, orderby=None) -> list:
        """カレンダーに登録されているイベントの一覧を取得する

        Args:
            calendar_id (str): イベントの一覧を取得するカレンダーのID
            limit (int): 取得するイベントの数の制限
            timemin (str): 取得するイベントの開始時刻の下限
            orderby (str): イベントの並び順

        Returns:
            list: イベントの一覧（辞書のリスト）
        """

        def get_events_sync():
            events_result = self.service.events().list(calendarId=calendar_id, singleEvents=True, orderBy="startTime").execute()
            events = events_result.get("items", [])

            if limit is not None:
                events = events[:limit]

            logger.info(f"get all events")
            logger.debug(f"get all events\n calendar_id:{calendar_id} limit:{limit} timemin:{timemin} orderby:{orderby}")
            return events

        loop = asyncio.get_running_loop()
        events = await loop.run_in_executor(None, get_events_sync)
        return events
