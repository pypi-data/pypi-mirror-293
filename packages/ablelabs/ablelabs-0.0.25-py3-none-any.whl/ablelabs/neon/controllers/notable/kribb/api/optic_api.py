import sys, os

sys.path.append(os.path.abspath(os.curdir))
from ablelabs.neon.utils.network.messenger import MessengerClient, run_server_func
from ablelabs.neon.utils.network.tcp_client import TcpClient
from ablelabs.neon.controllers.notable.kribb.api.robot_router import RobotRouter


class OpticAPI(MessengerClient):
    def __init__(self, tcp_client: TcpClient) -> None:
        super().__init__(tcp_client)

    @run_server_func(RobotRouter.optic_camera_capture)
    async def camera_capture(self):
        pass

    @run_server_func(RobotRouter.optic_camera_show)
    async def camera_show(
        self,
        winname: str,
        resize_ratio=0.5,
    ):
        pass

    @run_server_func(RobotRouter.optic_set_led_brightness)
    async def set_led_brightness(self, value: int):
        pass

    @run_server_func(RobotRouter.optic_set_led_on_off)
    async def set_led_on_off(self, on: bool):
        pass

    @run_server_func(RobotRouter.optic_set_displacement_zero)
    async def set_displacement_zero(self):
        pass

    @run_server_func(RobotRouter.optic_get_displacement_value)
    async def get_displacement_value(self):
        pass
