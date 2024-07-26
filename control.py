import time
import scrcpy
from typing import Tuple
import math
import threading



class ScrcpyControl:
    def __init__(self, parent) -> None:
        self.client = parent.client
        self.touch_map = parent.touch_map

        self.move_touch_id = -1
        self.attack_touch_id = -2
        self.skill_touch_id = -3
        self.tap_touch_id = -4

        self.directions = []
        self.current_direction = None
        
        self.direct_dic = {"UP": 270, "DOWN": 90, "LEFT": 180, "RIGHT": 0}
        self.direct_tick = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        self.last_direct_tick = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        


        self.key_status = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        self.last_status = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}

        self.posX, self.posY = self.touch_map["pad_center"]
        self.moving = False

        self.is_touching = False


        



    def touch_start(self, x: float, y: float, touch_id=-1):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_DOWN, touch_id=touch_id)

    def touch_move(self, x: float, y: float, touch_id=-1):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_MOVE, touch_id=touch_id)

    def touch_end(self, x: float, y: float, touch_id=-1):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_UP, touch_id=touch_id)

    def tap(self, x: float, y: float, touch_id=-1):
        self.touch_start(x, y, touch_id=touch_id)
        time.sleep(0.005)
        self.touch_end(x, y, touch_id=touch_id)

    def tap_pos(self, pos: list, touch_id=-1):
        x = pos[0]
        y = pos[1]
        self.touch_start(x, y, touch_id=touch_id)
        time.sleep(0.005)
        self.touch_end(x, y, touch_id=touch_id)


    def calc_mov_point(self, angle: float) -> Tuple[int, int]:
        rx, ry = self.touch_map["pad_center"]
        r = 100

        x = rx + r * math.cos(angle * math.pi / 180)
        y = ry + r * math.sin(angle * math.pi / 180)
        return int(x), int(y)

    def move_test(self, directions:list, t):
        move_t = threading.Thread(
                target=self.move_thread,args=(directions,t)
            )
        move_t.start()


    def move_start(self, directions:list):
        # print("move_start")

        angle = self.directions_to_angle(directions)
        x, y = self.calc_mov_point(angle)
        self.posX = x
        self.posY = y
        cx, cy = self.touch_map["pad_center"]

        self.touch_start(x, y, self.move_touch_id)

        self.moving = True

        self.directions = directions



    def move_to_direction(self, direction:str):
        if direction == "STOP":
            x, y = self.posX, self.posY
            self.touch_end(x, y, self.move_touch_id)
            self.is_touching = False
            return
        
        if direction:
            directions = direction.split("_")

            if not self.is_touching:
                self.move_start(directions)
                self.is_touching = True

            self.move_change(directions)

    def update_direction(self, new_direction:str):
        if new_direction != self.current_direction:
            self.current_direction = new_direction
            self.move_to_direction(new_direction)

    def stop(self):
        if self.is_touching:
            self.touch_end()
            self.is_touching = False

            
    def move_stop(self):
        # print("move_stop")
        x, y = self.posX, self.posY
        self.touch_end(x, y, self.move_touch_id)

        self.moving = False

        self.last_status = self.key_status.copy()
        self.last_direct_tick = self.direct_tick.copy()

        self.directions = ["STOP"]
        self.direct_tick = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
        self.key_status = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}


    def move_change(self, directions:list):
        # print("move_change")

        angle = self.directions_to_angle(directions)
        x, y = self.calc_mov_point(angle)

        self.touch_move(x, y, self.move_touch_id)

        self.directions = directions

        
    def move_thread(self, directions:list, t: float):
        self.moving = True
        angle = self.directions_to_angle(directions)
        x, y = self.calc_mov_point(angle)
        
        self.touch_start(x, y, self.move_touch_id)
        time.sleep(t)
        self.touch_end(x, y, self.move_touch_id)
        self.moving = False


    def attack(self, t: float=0.1):

        attack_t = threading.Thread(
                target=self.attack_thread
            )
        attack_t.start()


    def attack_thread(self):
        x, y = self.touch_map["attack"]
        self.touch_start(x, y, self.attack_touch_id)
        time.sleep(0.005)
        self.touch_end(x, y, self.attack_touch_id)

    def stop_all(self):
        pass

    def directions_to_angle(self, directions:list):
        direction_mask = [0, 0, 0, 0] # RIGHT DOWN LEFT UP
        if "RIGHT" in directions:
            direction_mask[0] = 1
        if "DOWN" in directions:
            direction_mask[1] = 1
        if "LEFT" in directions:
            direction_mask[2] = 1
        if "UP" in directions:
            direction_mask[3] = 1
        
        angle = -1

        if direction_mask == [1, 0, 0, 0]:
            angle = 0
        elif direction_mask == [1, 1, 0, 0]:
            angle = 45
        elif direction_mask == [0, 1, 0, 0]:
            angle = 90
        elif direction_mask == [0, 1, 1, 0]:
            angle = 135
        elif direction_mask == [0, 0, 1, 0]:
            angle = 180
        elif direction_mask == [0, 0, 1, 1]:
            angle = 225
        elif direction_mask == [0, 0, 0, 1]:
            angle = 270

        return angle
    
    def on_frame(self):

        last_ticks = sum(self.last_direct_tick.values())
        ticks = sum(self.direct_tick.values())

        if ticks > 0:

            # if last_ticks == 0:
            #     # start move
            #     self.move_start(self.directions)
            # elif last_ticks > 0:
            #     self.move_change(self.directions)

            # 状态发生改变
            if self.last_status != self.key_status:
                if last_ticks == 0:
                    # start move
                    self.move_start(self.directions)
                elif last_ticks > 0:
                    self.move_change(self.directions)

        else:
            if self.moving:
                self.move_stop()

        self.last_direct_tick = self.direct_tick.copy()
        self.last_status = self.key_status.copy()

        #print(self.direct_tick)

    def update_status(self):

        for action in self.direct_dic.keys():
            self.direct_tick[action] -= 1
            if self.direct_tick[action] < 0:
                self.direct_tick[action] = 0


    def parse_inputs(self, direct:str, to_release):
        input_direction = direct.strip().split("_")
        
        if len(input_direction) == 0 or "STOP" in input_direction:
            # for d in self.direct_tick:
            #     self.direct_tick[d] = 0
            if self.moving:
                self.move_stop()
            return self.key_status, self.directions
        
        for d in input_direction:
            if len(d) == 0:
                input_direction.remove(d)

        if "UP" in input_direction:
            self.direct_tick["DOWN"] = 0
            self.direct_tick["UP"] = to_release
            self.key_status["DOWN"] = 0
            self.key_status["UP"] = 1

        elif "DOWN" in input_direction:
            self.direct_tick["UP"] = 0
            self.direct_tick["DOWN"] = to_release
            self.key_status["UP"] = 0
            self.key_status["DOWN"] = 1

        if "LEFT" in input_direction:
            self.direct_tick["RIGHT"] = 0
            self.direct_tick["LEFT"] = to_release
            self.key_status["RIGHT"] = 0
            self.key_status["LEFT"] = 1

        elif "RIGHT" in input_direction:
            self.direct_tick["LEFT"] = 0
            self.direct_tick["RIGHT"] = to_release
            self.key_status["LEFT"] = 0
            self.key_status["RIGHT"] = 1


        directions = [] # 实际的方向
        for action in self.direct_dic.keys():
            if self.direct_tick[action] > 0:
                directions.append(action)
        self.directions = directions

    def direction_move(self, direct:str, to_release):

        self.update_status()
        self.parse_inputs(direct, to_release)
        
        self.on_frame()




        return self.key_status, self.directions






        # 刷新状态
        # for action in self.direct_dic.keys():
        #     self.direct_tick[action] -= 1

        #     if self.direct_tick[action] < 0:
        #         if key_status[action] == 1:
        #             # self.move_stop(self.direct_dic[action])
        #             self.move_stop()
        #             key_status[action] = 0
        #             self.direct_tick[action] = 0

        # # 添加新的状态
        # for action in directions:
        #     if action == "STOP":
        #         continue
        #     self.move_start(self.direct_dic[action])
        #     self.direct_tick[action] = to_release
        #     key_status[action] = 1

        
        # return key_status, directions




    # def clear_action(self, action_cache, control):
    #     while len(action_cache) > 0 :
    #         action = action_cache.pop()
    #         control.key_up(self.direct_dic[action])
    #         self.direct_tick[action] = release_tick

    def turn(self, direction:str):
        self.direction_move(direction, 30)
        # if direction in self.direct_dic:
        #     self.move(direction, 0.1)
        #     key_status[direction] = 0
        #     direct_tick[direction] = 0


