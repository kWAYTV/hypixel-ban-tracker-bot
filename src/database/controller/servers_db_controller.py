import aiosqlite

from src.database.schema.server_schema import ServerSchema
from src.helper.config import Config


class ServersDbController:
    """
    Controller class for managing the repository database.
    """

    def __init__(self) -> None:
        self.config = Config()
        self.db_path = "src/database/storage/broadcast_channels.sqlite"

    async def create_table(self) -> None:
        """
        Creates the 'repos' table in the database if it doesn't exist.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS repos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    server_id INTEGER NOT NULL UNIQUE,
                    channel_id INTEGER NOT NULL,
                    message_id INTEGER DEFAULT NULL
                );
            """
            )
            await db.commit()

    async def insert(self, server_schema: ServerSchema) -> None:
        """
        Inserts a new server into the database and updates the server if it already exists.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO repos (server_id, channel_id, message_id)
                VALUES (?, ?, ?)
                ON CONFLICT(server_id) DO UPDATE SET
                channel_id = excluded.channel_id,
                message_id = excluded.message_id;
            """,
                (
                    server_schema.server_id,
                    server_schema.channel_id,
                    server_schema.message_id,
                ),
            )
            await db.commit()

    async def delete(self, server_id: int) -> None:
        """
        Deletes a server from the database.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM repos WHERE server_id=?", (server_id,))
            await db.commit()

    async def update_message_id(self, server_id: int, message_id: int) -> None:
        """
        Updates the message ID of a server in the database.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE repos SET message_id=? WHERE server_id=?",
                (message_id, server_id),
            )
            await db.commit()

    async def get(self, server_id: int) -> ServerSchema:
        """
        Retrieves a server from the database.
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT server_id, channel_id, message_id FROM repos WHERE server_id=?",
                (server_id,),
            ) as cursor:
                row = await cursor.fetchone()
                return ServerSchema(*row) if row else None

    async def get_all(self) -> list[ServerSchema]:
        """
        Retrieves all servers from the database.
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT server_id, channel_id, message_id FROM repos"
            ) as cursor:
                return [ServerSchema(*row) for row in await cursor.fetchall()]

    async def count(self) -> int:
        """
        Counts the number of servers in the database.
        """
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM repos") as cursor:
                return (await cursor.fetchone())[0]

    async def clear(self) -> None:
        """
        Clears all servers from the database.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM repos")
            await db.commit()
