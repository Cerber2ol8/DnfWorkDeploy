import time
import scrcpy
from typing import Tuple
import math
import threading



direct_dic = {"UP": 90, "DOWN": 270, "LEFT": 0, "RIGHT": 180}
direct_tick = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
key_status = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
release_tick = 1



class ScrcpyControl:
    def __init__(self, parent) -> None:
        self.client = parent.client
        self.touch_map = parent.touch_map

        self.move_touch_id = -1
        self.attack_touch_id = -2
        self.skill_touch_id = -3
        self.tap_touch_id = -4



    def touch_start(self, x: float, y: float, touch_id=-1):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_DOWN, touch_id=touch_id)

    def touch_move(self, x: float, y: float, touch_id=-1):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_MOVE, touch_id=touch_id)

    def touch_end(self, x: float, y: float, touch_id=-1):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_UP, touch_id=touch_id)

    def tap(self, x: float, y: float, touch_id=-1):
        self.touch_start(x, y, touch_id=touch_id)
        time.sleep(0.01)
        self.touch_end(x, y, touch_id=touch_id)

    def calc_mov_point(self, angle: float) -> Tuple[int, int]:
        rx, ry = self.touch_map["pad_center"]
        r = 100

        x = rx + r * math.cos(angle * math.pi / 180)
        y = ry - r * math.sin(angle * math.pi / 180)
        return int(x), int(y)

    def move(self, angle: float, t: float):
        move_t = threading.Thread(
                target=self.move_thread,args=(angle,t)
            )
        move_t.start()


    def move_start(self, angle: float):
        x, y = self.calc_mov_point(angle)
        cx, xy = self.touch_map["pad_center"]
        self.touch_start(cx, xy, self.move_touch_id)
        self.touch_move(x, y, self.move_touch_id)

    def move_stop(self):
        x, y = self.touch_map["pad_center"]
        self.touch_end(x, y, self.move_touch_id)
        
    def move_thread(self, angle: float, t: float):
        self.move_start(angle)
        time.sleep(t)
        self.move_stop(angle)

    def attack(self, t: float = 0.01):
        x, y = self.touch_map["attack"]
        self.touch_start(x, y, self.attack_touch_id)
        time.sleep(t)
        self.touch_end(x, y, self.attack_touch_id)







    def direction_move(self, direct:str, to_release=release_tick):
        
        directions = direct.strip().split("_")
        if len(directions) == 0 or "STOP" in directions:
            for d in direct_tick:
                direct_tick[d] = 0
        for d in directions:
            if len(d) == 0:
                directions.remove(d)
        if "UP" in directions:
            direct_tick["DOWN"] = 0

        elif "DOWN" in directions:
            direct_tick["UP"] = 0

        if "LEFT" in directions:
            direct_tick["RIGHT"] = 0

        elif "RIGHT" in directions:
            direct_tick["LEFT"] = 0

        # 刷新状态
        for action in direct_dic.keys():
            direct_tick[action] -= 1

            if direct_tick[action] < 0:
                if key_status[action] == 1:
                    self.move_stop(direct_dic[action])
                    key_status[action] = 0
                    direct_tick[action] = 0

        # 添加新的状态
        for action in directions:
            if action == "STOP":
                continue
            self.move_start(direct_dic[action])
            direct_tick[action] = to_release
            key_status[action] = 1
        return key_status, directions




    def clear_action(self, action_cache, control):
        while len(action_cache) > 0 :
            action = action_cache.pop()
            control.key_up(direct_dic[action])
            direct_tick[action] = release_tick

    def turn(self, direction:str):
        if direction in direct_dic:
            self.move(direct_dic[direction], 0.1)
            key_status[direction] = 0
            direct_tick[direction] = 0


