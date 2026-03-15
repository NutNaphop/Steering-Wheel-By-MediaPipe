import pyvjoy
import config as cfg
from ..core.utils import to_vjoy

class VirtualJoystick:
    def __init__(self, device_id=1):
        self.j = pyvjoy.VJoyDevice(device_id)

    def update(self, steering, throttle, brake):
        self.j.data.wAxisY = 0
        self.j.data.wAxisZ = 0
        
        self.j.data.wAxisX = to_vjoy(steering, cfg.VJOY_CENTER, cfg.VJOY_MAX)
        # self.j.data.wAxisX = to_vjoy(steering)
        self.j.data.wAxisY = int(throttle * cfg.VJOY_MAX)
        self.j.data.wAxisZ = int(brake * cfg.VJOY_MAX)
        self.j.update()
        # print(f"X:{self.j.data.wAxisX} Y:{self.j.data.wAxisY} Z:{self.j.data.wAxisZ}")

    
    def reset(self):
        self.j.data.wAxisX = cfg.VJOY_CENTER
        self.j.update()