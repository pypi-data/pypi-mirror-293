import asyncio
from loguru import logger

import sys, os

sys.path.append(os.path.abspath(os.curdir))
from ablelabs.neon.utils.network.messenger import run_server_func
from ablelabs.neon.utils.network.tcp_client import TcpClient
from ablelabs.neon.controllers.notable.api.robot_api import RobotAPI as BaseRobotAPI
from ablelabs.neon.controllers.notable.kribb.api.robot_router import RobotRouter
from ablelabs.neon.controllers.notable.kribb.api.optic_api import OpticAPI
from ablelabs.neon.common.notable.structs import Location


class RobotAPI(BaseRobotAPI):
    def __init__(self) -> None:
        tcp_client = TcpClient(name="tcp_client", log_func=logger.trace)
        super().__init__(tcp_client)
        self._optic_api = OpticAPI(tcp_client=tcp_client)

    @property
    def optic(self):
        return self._optic_api

    @run_server_func(RobotRouter.robot_scan_displacement_sensor)
    async def scan_displacement_sensor(
        self,
        pipette_number: int,
        location: Location,
        padding: tuple[float, float],
        scan_count: tuple[float, float],
    ) -> list[list[tuple[float, float, float]]]:
        pass
