from hub import motion_sensor, port, light_matrix
import runloop,  motor, motor_pair, asyncio, math, color_sensor, color, time, math

# A - color sensor
# B - right motor
# C - spinny motor
# D - back motor
# E - lifting motor
# F - left motor

speed = 500
speed_E = 100
speed_C = 200
speed_D = 200
speed_turn = 200
speed_turn_sensitive = 100



async def color_correct():
    global R1, R2, L1, L2
    possiblecolors = [0, 3, 6, 7, 9]
    possiblecolors.remove(R1)
    possiblecolors.remove(R2)
    possiblecolors.remove(L1)
    possiblecolors.remove(L2)
    if R1 == 0:
        R1 = possiblecolors[0]
    if L1 == 0:
        L1 = possiblecolors[0]
    if R2 == 0:
        R2 = possiblecolors[0]
    if L2 == 0:
        L2 = possiblecolors[0]

async def go_straight(length, speed_left, speed_right):
    #length = int(length)
    speed_left = int(speed_left)
    speed_right = int(speed_right)
    length = round(length/17.6*360)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, length, speed_left, speed_right)

async def right_turn(yaw, speed_turn):
    while abs(motion_sensor.tilt_angles()[0]-yaw) > 2:
        motor_pair.move_tank(motor_pair.PAIR_1, speed_turn, -speed_turn)
    motor_pair.stop(motor_pair.PAIR_1)

async def left_turn(yaw, speed_turn):
    while abs(motion_sensor.tilt_angles()[0]-yaw) > 2:
        motor_pair.move_tank(motor_pair.PAIR_1, -speed_turn, speed_turn)
    motor_pair.stop(motor_pair.PAIR_1)

async def color_reader():
    screw = 0
    if color_sensor.color(port.A) is color.RED:
        screw = color.RED
        print (screw)
    if color_sensor.color(port.A) is color.YELLOW:
        screw = color.YELLOW
        print (screw)
    if color_sensor.color(port.A) is color.GREEN:
        screw = color.GREEN
        print (screw)
    if color_sensor.color(port.A) is color.BLUE:
        screw = color.BLUE
        print (screw)
    return screw

async def shake():
    await motor.run_for_degrees(port.C, 20, 500)
    await motor.run_to_relative_position(port.C, 0, 500)

async def backmix():
    motor.reset_relative_position(port.C, 0)
    await motor.run_for_degrees(port.E, 155, speed_E)
    await go_straight(-7, speed, speed)
    await motor.run_for_degrees(port.E, -155, speed_E)
    await motor.run_for_degrees(port.C, -190, speed_C)
    await motor.run_for_degrees(port.E, 155, speed_E)
    await go_straight(12, speed, speed)
    await go_straight(-5, speed, speed)
    await motor.run_to_relative_position(port.C, 0, speed_C)
    #await motor.run_for_degrees(port.C, 190, speed_C)
    await motor. run_for_degrees(port.E, -170, speed_E)
    await shake()

async def frontmix():
    await motor.run_for_degrees(port.C, 180, speed_C)
    await backmix()
    await motor.run_for_degrees(port.C, -180, speed_C)

async def rightmix():
    await motor.run_for_degrees(port.C, 90, speed_C)
    await backmix()
    await motor.run_for_degrees(port.C, -90, speed_C)

async def leftmix():
    await motor.run_for_degrees(port.C, -90, speed_C)
    await backmix()
    await motor.run_for_degrees(port.C, -90, speed_C)

async def right_left_mix():
    await leftmix()
    await backmix()
    await leftmix()

async def left_right_mix():
    await rightmix()
    await motor.run_for_degrees(port.C, -100, speed_C)
    await backmix()
    await motor.run_for_degrees(port.C, 80, speed_C)
    await rightmix()




async def spinny_thing():
    speed = 500
    await motor.run_for_degrees(port.E, 0, 0, stop = motor.HOLD)
    await motor.run_for_degrees(port.C, 0, 0, stop = motor.HOLD)
    await go_straight(-25, speed, speed)
    motion_sensor.reset_yaw(0)
    await go_straight(25, speed, speed)
    await motor.run_for_degrees(port.E, 155, -speed_E, stop = motor.HOLD) #felvenni a payload-ot
    await go_straight(32, speed, speed)
    await right_turn(-900, speed_turn)
    await go_straight(59, speed, speed)
    speed = 100
    await go_straight(4, speed, speed)
    speed = 500
    if color_sensor.color(port.A) is color.YELLOW:
        await go_straight(-2, speed, speed)
        await motor.run_for_degrees(port.C, -185, speed_C, stop = motor.HOLD)
        await go_straight(2, speed, speed)
    if color_sensor.color(port.A) is color.RED:
        await go_straight(-2, speed, speed)
        await motor.run_for_degrees(port.C, -95, speed_C, stop = motor.HOLD)
        await go_straight(2, speed, speed)
    if color_sensor.color(port.A) is color.GREEN:
        await go_straight(-2, speed, speed)
        await motor.run_for_degrees(port.C, 95, speed_C, stop = motor.HOLD)
        await go_straight(2, speed, speed)
    await motor.run_for_degrees(port.E, 155, speed_E)

async def yellow_door():
    await go_straight(-10, speed, speed)
    await right_turn(-1790, speed_turn)
    await go_straight(30, speed, speed)
    await left_turn(-930, speed_turn) #kanyar a tolás előtt
    await go_straight(43, speed, speed)
    await left_turn(-600, speed_turn)
    await go_straight(8, speed, speed)
    await go_straight(-8, speed, speed)
    await right_turn(-900, speed_turn)

async def randomization():
    global R1, R2, L1, L2
    R1 = color.WHITE
    R2 = color.WHITE
    L1 = color.WHITE
    L2 = color.WHITE
    await go_straight(25, speed, speed)
    motor.run_to_relative_position(port.C, 0, speed_C)
    await left_turn(30, speed_turn) #amikor bemegyünk
    await motor.run_for_degrees(port.E, -155, speed_E)
    motor.run_for_degrees(port.C, -50, speed_C)
    await go_straight(52, speed, speed)
    await right_turn(0, speed_turn)
    await right_turn(-350, speed_turn) #első
    R1 = await color_reader()
    await left_turn(330, speed_turn)
    await motor.run_for_degrees(port.C, 100, speed_C)
    L1 = await color_reader()
    await right_turn(10, speed_turn)
    await go_straight(9, speed, speed)
    await left_turn(360, speed_turn)
    L2 = await color_reader()
    await right_turn(-370, speed_turn)
    await motor.run_for_degrees(port.C, -95, speed_C)
    R2 = await color_reader()
    motor.run_to_relative_position(port.C, 0, speed_C)
    motor.run_for_degrees(port.E, 155, speed_E)
    await left_turn(0, speed_turn)

async def pull_out():
    await go_straight(-37, speed, speed)
    await left_turn(900, speed_turn)
    await go_straight(-24, speed, speed)
    await left_turn(1790, speed_turn)
    #await go_straight(-1, speed, speed)
    await motor.run_for_degrees(port.D, 65, speed_D, stop = motor.HOLD)
    await go_straight(15, speed, speed)
    await motor.run_for_degrees(port.D, -75, speed_D)

async def computer():
    await go_straight(20, 750, 750)
    await right_turn(900, speed_turn)
    await go_straight(110, 750, 750)
    await right_turn(10, speed_turn)
    await go_straight(-23, speed, speed)
    motion_sensor.reset_yaw(0)
    await go_straight(66, speed, speed)
    await motor.run_for_degrees(port.E,-155, 200)
    await motor.run_for_degrees(port.E, 155, speed_E)
    await right_turn(-750, speed_turn)
    await go_straight(13, speed, speed)
    await left_turn(0, speed_turn)
    await go_straight(8, speed, speed)
    await motor.run_for_degrees(port.E, -155, speed_E)
    await go_straight(-8, speed, speed)
    await go_straight(4, speed, speed)
    await motor.run_for_degrees(port.E, 155, speed_E)

async def pickup():
    await right_turn(-900, speed_turn)
    await go_straight(-70, speed, speed)
    motion_sensor.reset_yaw(-900)
    motor.run_to_relative_position(port.C, 0, 100)
    await go_straight(10, speed, speed)
    await left_turn(10, speed_turn)
    await go_straight(10, speed, speed)
    await motor.run_for_degrees(port.E, -165, speed_E)
    await runloop.sleep_ms(500)
    await shake()

#async def arrangeing():

async def first_delivery(): #not FIRST Lego League - new slogan for WRO :)
    await go_straight(-10, speed, speed)
    await right_turn(-900, speed_turn)
    await go_straight(58, speed, speed)
    await left_turn(-450, speed_turn)
    if L2 == 7: #sárga
        motor.run_for_degrees(port.C, 135, speed_C)
    if L2 == 3: #kék
        motor.run_for_degrees(port.C, -135, speed_C)
    if L2 == 6: #zöld
        motor.run_for_degrees(port.C, -45, speed_C)
    if L2 == 9: #piros
        motor.run_for_degrees(port.C, 45, speed_C)
    await go_straight(20, speed, speed)

async def first_recapture():
    await motor.run_for_degrees(port.E, 155, speed_E)
    await go_straight(-1, speed, speed)
    await left_turn(-300, speed_turn)
    await motor.run_for_degrees(port.C, -10, speed_C)
    await motor.run_for_degrees(port.E, -155, speed_E)

async def rocketnose():
    #await go_straight(-50, speed, speed)
    #await right_turn(-900, speed_turn)
    #await go_straight(-30, speed, speed)
    motion_sensor.reset_yaw(-900)
    await go_straight(180, speed, speed)
    await left_turn(0, speed_turn)
    await go_straight(-20, speed, speed)
    motion_sensor.reset_yaw(0)
    await go_straight(14, speed, speed)
    await left_turn(900, speed_turn)
    await go_straight(-20, speed, speed)
    await go_straight(1.7, speed, speed)
    await motor.run_for_degrees(port.D, 105, 500, stop=motor.HOLD)
    motor.run(port.D, 300)
    await go_straight(-20, speed, speed)
    motion_sensor.reset_yaw(900)
    await go_straight(17, speed, speed)

async def yellow_part():
    await right_turn(0, speed_turn)
    await go_straight(49, speed, speed)
    await left_turn(450, speed_turn)
    await go_straight(8, speed, speed)
    await motor.run_for_degrees(port.D, -100, speed_E)

async def red_part():
    await go_straight(6, speed, speed)
    await motor.run_for_degrees(port.D, 100,speed_D)
    await go_straight(6, speed, speed)
    await left_turn(1350, speed_turn)
    await go_straight(-8, speed, speed)
    await motor.run_for_degrees(port.D, -100, speed_D)




async def test():
    global R1, R2, L1, L2
    R1 = 9
    R2 = 3
    L1 = 6
    L2 = 9
    #await color_correct()
    print(R1,R2,L1,L2)
    motor_pair.pair(motor_pair.PAIR_1, port.F, port.B)
    await go_straight(-5, speed, speed)
    await rocketnose()
    await yellow_part()
    await red_part()
    #await first_delivery()
    #motor.reset_relative_position(port.C, 0)
    #await go_straight(-3, speed, speed)
    #await pickup()
    #await backmix()

async def main():
    global R1, R2, L1, L2
    R1 = 0
    R2 = 0
    L1 = 0
    L2 = 0
    motor_pair.pair(motor_pair.PAIR_1, port.F, port.B)
    motor.reset_relative_position(port.C, 0)
    await spinny_thing()
    await yellow_door()
    await randomization()
    print(R1, L1, L2, R2)
    await color_correct()
    print(R1, L1, L2, R2)
    await pull_out()
    await computer()
    await pickup()
    await first_delivery()
    await first_recapture()

runloop.run(test()) 