import aiosqlite
import json
from enum import StrEnum
from asyncio import Lock
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType
from typing import Any


class SQLiteStorage(BaseStorage):
    """
    Async SQLite storage for aiogram bots.
    Based on https://gist.github.com/KurimuzonAkuma/683eec4d62e111578a42608d4485fc27
    """


    class __Tables(StrEnum):
        data = 'data'
        states = 'states'


    def __init__(self, path: str = 'user-states.db'):
        self.__path = path
        self.__connection = None
        self.__cursor = None
        
        self.__lock = Lock()


    async def set_state(self, key: StorageKey, state: StateType):
        raw_state = self.__get_raw_state(state)
        
        if not raw_state:
            await self.__delete_from_table(self.__Tables.states, key.user_id, key.chat_id)
            return 
        
        await self.__execute(f"""
                              INSERT INTO {self.__Tables.states}
                              (chatID, userID, state)
                              VALUES (?, ?, ?)
                              ON CONFLICT(chatID, userID) DO UPDATE SET 'state' = ?;
                              """,
                              values = (key.chat_id, key.user_id, raw_state, raw_state),
                              commit = True)


    async def get_state(self, key: StorageKey) -> str | None:
        await self.__execute(f"""
                            SELECT state FROM {self.__Tables.states} 
                            WHERE chatID = ? AND userID = ?;
                            """,
                            values = (key.chat_id, key.user_id))
        
        user = await self.__cursor.fetchone() # tuple that contains only 'state' column
        return user[0] if user else None


    async def set_data(self, key: StorageKey, data: dict[str, Any]):
        if not data:
            await self.__delete_from_table(self.__Tables.data, key.user_id, key.chat_id)
            return 
        
        serialized = json.dumps(data)
        await self.__execute(f"""
                            INSERT INTO {self.__Tables.data} 
                            (chatID, userID, data) 
                            VALUES (?, ?, ?) 
                            ON CONFLICT(chatID, userID) DO UPDATE SET 'data' = ?;
                            """,
                            values = (key.chat_id, key.user_id, serialized, serialized),
                            commit = True)
    

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        await self.__execute(f"""
                            SELECT data FROM {self.__Tables.data} 
                            WHERE chatID = ? AND userID = ?;
                            """,
                            values = (key.chat_id, key.user_id))
        
        user = await self.__cursor.fetchone() # tuple that contains only 'data' column
        return json.loads(user[0]) if user else {}


    async def close(self):
        if self.__connected_to_database:
            await self.__cursor.close()
            await self.__connection.close()


    async def __execute(self, query: str, values: tuple = None, commit: bool = False):
        async with self.__lock:
            await self.__connect_to_database_if_need()
            await self.__cursor.execute(query, values)

            if commit:
                await self.__connection.commit()


    async def __delete_from_table(self, table: str, user_id: int, chat_id: int):
        await self.__execute(f'DELETE FROM {table} WHERE chatID = ? AND userID = ?;',
                              values = (chat_id, user_id), 
                              commit = True)


    def __get_raw_state(self, state: StateType) -> str | None:
        """
        Return state.state, if state is instance of State.

        Return state, if state is just a string
        """
        
        if isinstance(state, State):
            return state.state
        
        return state


    @property
    def __connected_to_database(self) -> bool:
        return self.__connection is not None


    async def __connect_to_database(self):
        self.__connection = await aiosqlite.connect(self.__path)
        self.__cursor = await self.__connection.cursor()

        await self.__create_tables()


    async def __connect_to_database_if_need(self):
        if not self.__connected_to_database:
            await self.__connect_to_database()


    async def __create_tables(self):
        create_query = """
        CREATE TABLE IF NOT EXISTS {}(
        chatID BIGINT NOT NULL,
        userID BIGINT NOT NULL,
        {},
        PRIMARY KEY (chatID, userID)
        );"""

        create_data_table_query = create_query.format(self.__Tables.data, 'data TEXT')
        create_states_table_query = create_query.format(self.__Tables.states, 'state TEXT')

        await self.__cursor.execute(create_data_table_query)
        await self.__cursor.execute(create_states_table_query)