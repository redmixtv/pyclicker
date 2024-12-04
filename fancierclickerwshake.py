import random
import time
import win32api
import win32con


SHAKE_ENABLED = True


x = 0

until_x_reset = 10

#values in ms
hold_avg = random.uniform(32, 38)
hold_stddev = random.uniform(4, 6)
#40-57ms
#outliers 37-60

interval_avg = random.uniform(42, 48)
interval_stddev = random.uniform(4, 6)
#70-80ms
#60-90ms range


def generate_times():
    global hold_time, interval_time, y
    
    y = min(max(0.005 * x + 1 + random.uniform(-0.02, 0.02), 1), 2)
    
    if random.random() < 0.15:  # 15% chance of bigger variance
        y *= random.uniform(0.85, 1.15)
    
    random_value = random.random()
     
    if 0.7 > random_value:
        hold_time = max(min(random.gauss(hold_avg, hold_stddev), hold_avg + 3*hold_stddev), hold_avg - 3*hold_stddev)*y
        interval_time = max(min(random.gauss(interval_avg, interval_stddev), interval_avg + 3*interval_stddev), interval_avg - 3*interval_stddev)*y
    else:
        hold_time = max(min(random.gauss(hold_avg, hold_stddev), hold_avg + 3*hold_stddev), hold_avg - 3*hold_stddev)/y
        interval_time = max(min(random.gauss(interval_avg, interval_stddev), interval_avg + 3*interval_stddev), interval_avg - 3*interval_stddev)/y
        
    if random.random() < 0.2:  # 20% chance
        hold_time += random.uniform(-2, 2)
        interval_time += random.uniform(-3, 3)

        
def print_click_debug():
    print("Clicked LMB!")
    #print("Hold Duration is " + str(hold_time) + "ms")
    #print("Interval Duration is " + str(interval_time) + "ms")
    #print("x is " + str(x) + "s")
    #print("until_x_reset is " + str(until_x_reset) + "s")   
    time.sleep(0.1)
        
        
def missed_click():
    global interval_time
    interval_time = min(interval_time * random.uniform(1.4, 1.6), 140)
    
    
def click():
    if SHAKE_ENABLED:
        start_pos = win32api.GetCursorPos()
        
        shake_amount = random.randint(3, 5)
        
        try:
            win32api.SetCursorPos((
                start_pos[0] + random.randint(-shake_amount, shake_amount),
                start_pos[1] + random.randint(-shake_amount, shake_amount)
            ))
        except:
            pass
    
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(hold_time*0.001*(1 + random.uniform(-0.05, 0.05)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
    if SHAKE_ENABLED:
        try:
            return_amount = random.randint(1, 3)
            win32api.SetCursorPos((
                start_pos[0] + random.randint(-return_amount, return_amount),
                start_pos[1] + random.randint(-return_amount, return_amount)
            ))
        except:
            pass
        
    time.sleep(interval_time*0.001*(1 + random.uniform(-0.05, 0.05)))
    

while True:
    if win32api.GetKeyState(0x05) < 0: #if pressed
        if x < 15:                     #max exhaust 15s
            x += 0.1 * random.uniform(0.95, 1.05)
        until_x_reset = 10
        generate_times()
        
        random_value = random.uniform(0, 1)
        
        if random_value < min(0.99 / y, 0.99):
            click()
        else:
            missed_click()
            time.sleep(interval_time*0.001)
    else:                              #else
        if x > 0 and until_x_reset > 0:
            x -= 0.1 * random.uniform(0.95, 1.05)
            until_x_reset -= 0.1
            time.sleep(0.1)
        else:
            x = 0
            until_x_reset = 10
        #debug print("x is " + str(x) + "s")
        #debug print("until_x_reset is " + str(until_x_reset) + "s")