import traceback
from loguru import logger
from src.database.controller.servers_db_controller import ServersDbController

class DatabaseLoader:
    """
    Class responsible for loading the database and setting it up.
    """

    def __init__(self) -> None:
        self.servers_db_controller = ServersDbController()

    async def setup(self) -> bool:
        """
        Sets up the database by creating the necessary table.
        """
        try:
            await self.servers_db_controller.create_table()
            return True
        except Exception as e:
            logger.critical(f"Error setting up database: {e}")
            traceback.print_exc()
            return False
