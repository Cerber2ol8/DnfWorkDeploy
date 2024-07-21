import time
from control import ScrcpyControl

# direct_dic = {"UP": "W", "DOWN": "S", "LEFT": "A", "RIGHT": "D"}
direct_dic = {"UP": 270, "DOWN": 90, "LEFT": 180, "RIGHT": 0}
direct_tick = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
key_status = {"UP": 0, "DOWN": 0, "LEFT": 0, "RIGHT": 0}
release_tick = 1



def move(direct:str, action_cache:list, control:ScrcpyControl, 
              verbose=False, to_release=release_tick):

    is_key_down = False
    is_key_up = False
    key_down = []
    key_up = []


    directions = direct.strip().split("_")
    if len(directions) == 0 or "STOP" in directions:
        for d in direct_tick:
            direct_tick[d] = 0

    for d in directions:
        if len(d) == 0:
            directions.remove(d)

    # action_to_complete = []
    if "UP" in directions:
        direct_tick["DOWN"] = 0
        # control.key_up(direct_dic["DOWN"])
        # key_status["DOWN"] = 0
    elif "DOWN" in directions:
        direct_tick["UP"] = 0
        # control.key_up(direct_dic["UP"])
        # key_status["UP"] = 0

    if "LEFT" in directions:
        direct_tick["RIGHT"] = 0
        # control.key_up(direct_dic["RIGHT"])
        # key_status["RIGHT"] = 0
    elif "RIGHT" in directions:
        direct_tick["LEFT"] = 0
        # control.key_up(direct_dic["LEFT"])
        # key_status["LEFT"] = 0

    action_cache = []


    # 刷新状态
    for action in direct_dic.keys():
        direct_tick[action] -= 1

        if direct_tick[action] < 0:
            if action in action_cache:
                action_cache.remove(action)
            if key_status[action] == 1:
                control.move_stop(direct_dic[action])
                is_key_up = True
                key_up.append(action)
                key_status[action] = 0
                direct_tick[action] = 0

    # 添加新的状态
    for action in directions:
        if action == "STOP":
            continue
        # control.key_press(direct_dic[action])
        if action not in action_cache:
            action_cache.append(action)
            is_key_down = True
            key_down.append(action)
            control.move_start(direct_dic[action])
            # key_status[action] = 1

        # control.key_up(direct_dic[action])
        # control.key_down(direct_dic[action])
        # control.key_press("L")



        # control.key_up(direct_dic[action])
        # control.key_down(direct_dic[action])
        # control.key_press(direct_dic[action])

        direct_tick[action] = to_release
        key_status[action] = 1

        # is_key_down = True
        # key_down.append(action)



    if verbose:

        if is_key_down:
            print(f"key down {key_down}")
        if is_key_up:
            print(f"key up {key_up}")
        print(key_status, directions, action_cache)




    return action_cache,[key_status, directions, action_cache]




def clear_action(action_cache, control):
    while len(action_cache) > 0 :
        action = action_cache.pop()
        control.key_up(direct_dic[action])
        direct_tick[action] = release_tick

def turn(direction:str, control):
    if direction in direct_dic:
        control.key_press(direct_dic[direction])
        key_status[direction] = 0
        direct_tick[direction] = 0



if __name__ == "__main__":
    action_cache = []
    # t1 = time.time()
    # while True:
        # if  int(time.time() - t1) % 2 == 0:
        #     action_cache = move("LEFT_DOWN", material=False, action_cache=action_cache, press_delay=0.1, release_delay=0.1)
        # else:
    # action_cache = move("RIGHT_UP", material=True, action_cache=action_cache, press_delay=0.1, release_delay=0.1)
    control = None
    action_cache = move("LEFT",action_cache,control)
    time.sleep(1)
    action_cache = move("LEFT_UP",action_cache,control)
    time.sleep(1)
    action_cache = move("RIGHT",action_cache,control)
    time.sleep(1)
    action_cache = move("RIGHT_UP",action_cache,control)
    time.sleep(1)
    action_cache = move("LEFT",action_cache,control)
    time.sleep(1)
    action_cache = move("LEFT_DOWN",action_cache,control)
    time.sleep(1)
    action_cache = move("RIGHT",action_cache,control)
    time.sleep(1)
    action_cache = move("RIGHT_DOWN",action_cache,control)
    time.sleep(1)
    clear_action(action_cache, control)