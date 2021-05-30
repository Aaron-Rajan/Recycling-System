import time
import random
import sys
sys.path.append('../')

from Common_Libraries.p3b_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim():
    try:
        my_table.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

### Constants
speed = 0.1 #Qbot's speed

### Initialize the QuanserSim Environment
my_table = servo_table()
arm = qarm()
arm.home()
bot = qbot(speed)

##---------------------------------------------------------------------------------------
## STUDENT CODE BEGINS
##---------------------------------------------------------------------------------------
import random
import time

def load():
    global bottles_dispensed   #Defined as global variable to ensure it can be called later in code

    if bottles_dispensed == 1:  #Determines where the container should be loaded in the hopper postion 1
        if material == "metal":  #Different set of q-arm inputs if metal can is being loaded
            arm.rotate_shoulder(50)
            arm.rotate_elbow(-35)
            arm.control_gripper(40)
            arm.rotate_wrist(90)    #Q-arm rotates wrist to avoid hitting tube when moving container to hopper
            arm.rotate_base(30)
            arm.rotate_wrist(-90)
            arm.move_arm(0.4064,0,0.4826)
            arm.rotate_base(-91)
            arm.rotate_shoulder(3)
            arm.rotate_elbow(13)
            arm.control_gripper(-40)
            arm.rotate_elbow(-30)
            arm.home()
        else:
            arm.rotate_shoulder(50)
            arm.rotate_elbow(-38)
            arm.control_gripper(40)
            arm.rotate_wrist(90)    
            arm.rotate_base(30)
            arm.rotate_wrist(-90)
            arm.move_arm(0.4064,0,0.4826)
            arm.rotate_base(-90)
            arm.rotate_elbow(10)
            arm.control_gripper(-16)
            arm.rotate_shoulder(-30)
            arm.home()
           
    elif bottles_dispensed == 2:  #load postion 2
        if material == "metal":
            arm.rotate_shoulder(50)
            arm.rotate_elbow(-35)
            arm.control_gripper(40)
            arm.rotate_wrist(90)    
            arm.rotate_base(30)
            arm.rotate_wrist(-90)
            arm.move_arm(0.4064,0,0.4826)
            arm.rotate_base(-76)
            arm.rotate_shoulder(2)
            arm.rotate_elbow(15)
            arm.control_gripper(-14)
            arm.rotate_elbow(-30)
            arm.home()
        else:
            arm.rotate_shoulder(50)
            arm.rotate_elbow(-35)
            arm.control_gripper(40)
            arm.rotate_wrist(90)    
            arm.rotate_base(30)
            arm.rotate_wrist(-90)
            arm.move_arm(0.4064,0,0.4826)
            arm.rotate_base(-76)
            arm.rotate_elbow(10)
            arm.control_gripper(-16)
            arm.rotate_elbow(-30)
            arm.home()
   
    else:  #load postion 3
        if material == "metal":
            arm.rotate_shoulder(50)
            arm.rotate_elbow(-35)
            arm.control_gripper(40)
            arm.rotate_wrist(90)    
            arm.rotate_base(30)
            arm.rotate_wrist(-90)
            arm.move_arm(0.4064,0,0.4826)
            arm.rotate_shoulder(-30)
            arm.rotate_base(-105)
            arm.rotate_shoulder(32)
            arm.rotate_elbow(15)
            arm.control_gripper(-14)
            arm.rotate_elbow(-30)
            arm.home()
        else:
            arm.rotate_shoulder(50)
            arm.rotate_elbow(-35)
            arm.control_gripper(40)
            arm.rotate_wrist(90)    
            arm.rotate_base(30)
            arm.rotate_wrist(-90)
            arm.move_arm(0.4064,0,0.4826)
            arm.rotate_shoulder(-30)
            arm.rotate_base(-105)
            arm.rotate_shoulder(30)
            arm.rotate_elbow(10)
            arm.control_gripper(-16)
            arm.rotate_elbow(-30)
            arm.home()
            
def dispense_and_load():
    global bottles_dispensed
    global material
    global Head_ID
    global ID
    global iteration
    global Properties
    
    if iteration==0: #runs simulation style as if it has never run a full sequence
        
        start = random.randint(1,6)     #randomizing container to dispense 
        Head_ID = my_table.container_properties(start)[2]   #defines comparative ID
        material = my_table.container_properties(start)[0]  #defines material of container
        my_table.container_properties(start)
        my_table.dispense_container()
        print('*',Head_ID)

        bottles_dispensed=1
        Mass=my_table.container_properties(start)[1]
        
        for i in range(3):     #used to iterate bottle dispensing
        
            load()
            
            dispense_rand=random.randint(1,6)     #randomizes bottle that is dispensed
            Properties=my_table.container_properties(dispense_rand)     #collects properties of dispensed bottle
            my_table.dispense_container()   #dispenses a random container with defined properties

            ID=Properties[2]     #defines ID of current container
            print(ID)
            
            Mass+=Properties[1]     #updates Mass
            print(Mass)

            if ID!=Head_ID:     #checks ID against Head_ID
                break

            if Mass>90:     #checks if total mass is over 90 grams
                break

            if bottles_dispensed==3:    #checks if there are three bottles in the hopper
                break

            bottles_dispensed+=1     #updates hopper count
            
    else: #runs simulation style as if it has run a full sequence or more
        
        Mass=Properties[1] #new inital mass
        print(Mass)
        bottles_dispensed=1 #resets bottles to amount not despostied
        
        for i in range(3):     
    
            load()
        
            dispense_rand=random.randint(1,6)     
            Properties=my_table.container_properties(dispense_rand)     
            my_table.dispense_container()

            ID=Properties[2]     
            print(ID)
    
            Mass+=Properties[1]     
            print(Mass)

            if ID!=Head_ID:     
                break

            if Mass>90:     
                break

            if bottles_dispensed==3:    
                break

            bottles_dispensed+=1
            

def avg(data):  
    total = 0
    for reading in data:
        total += reading
    return total/len(data)

def transfer(): 
    output_v=0 #initalized variable for scanner output
    
    off_dis=0.4 #distance at which bot will begin bin id searching
    bot.rotate(45) #this line and the following allow for the bot to face down the main line
    time.sleep(.3)
    bot.rotate(46)
    time.sleep(.3)
    bot.rotate(45)
    time.sleep(.3)
    bot.rotate(46)
    time.sleep(.3)
    
    while bot.position()[0]>=off_dis: #corrects for angle skew
        full_info = bot.follow_line(0.05)
        lines_lost=full_info[1]
        left_wheel_speed=lines_lost[0]
        right_wheel_speed=lines_lost[1]
        bot.forward_velocity([left_wheel_speed,right_wheel_speed])
        distance=bot.depth() #distance update

    if bot.position()[0]==off_dis: #stops bot once in postion to search for bin
        bot.forward_velocity([0,0])
        bot.stop()
  
    while bot.position()[0]<=off_dis and output_v<=4.55: #this structure allows bot to seek and identify its correct bin
        
        if Head_ID=='Bin02': #used to select the correct scanner to find its bin location
            bot.activate_color_sensor('Blue')
            output_v_list=bot.read_blue_color_sensor('Bin02',0.6) #output of sensor readings 
            
        if Head_ID=='Bin01': 
            bot.activate_color_sensor('Red')
            output_v_list=bot.read_red_color_sensor('Bin01',0.6)
            
        if Head_ID=='Bin03': 
            bot.activate_color_sensor('Green')
            output_v_list=bot.read_green_color_sensor('Bin03',0.6) 
            
        if Head_ID=='Bin04': #switch to hull sensor as only a max of three colours can be used
            bot.activate_hall_sensor()
            output_v_list=bot.read_hall_sensor('Bin04',0.6) 
        
        bot.forward_time(5.72) #moves qbot between bins
        
        output_v=avg(output_v_list) #collects bin list readings and averages it for assessment
        print(output_v)
            

    if output_v>4.55: #structure turns qbot to face the bin
        bot.stop()
        bot.rotate(45)
        time.sleep(.3)
        bot.rotate(46)
        time.sleep(.3)
        
        while bot.depth()>0.07: #makes qbot near and stop next to the bin
            bot.forward_time(0.1)
            print(bot.depth())
            
    if bot.depth()<=0.14: #turns qbot to dump postion
        bot.rotate(-45)
        time.sleep(.3)
        bot.rotate(-46)
        time.sleep(.3)

def deposit(): 
    bot.activate_actuator()
    bot.rotate_actuator(15)
    time.sleep(0.1)
    bot.rotate_actuator(30)
    time.sleep(0.1)
    bot.rotate_actuator(45)
    time.sleep(0.1)
    bot.rotate_actuator(60)
    time.sleep(0.1)
    bot.rotate_actuator(75)
    time.sleep(0.1)
    bot.rotate_actuator(90) #slight jiggle forces stuck containers to fall out(cans get stuck otherwise on rare occasions)
    bot.rotate_actuator(87)
    bot.rotate_actuator(90)
    time.sleep(1)
    
    bot.deactivate_actuator()
    time.sleep(0.5)
    
def return_home():
    speed_increase=0.1 #this variable accounts for the early stop of the qbot
    distance=2 #variable defined as larger than condition in below structure
    i=1 
    
    while i!=0:     #infinite loop follows line up until qbot reaches initial placement
        full_info = bot.follow_line(0.3)
        lines_lost=full_info[1] 
        left_wheel_speed=lines_lost[0]+speed_increase
        right_wheel_speed=lines_lost[1]+speed_increase
        bot.forward_velocity([left_wheel_speed,right_wheel_speed])
        distance=bot.depth()    #distance update
        
        if distance <= 0.1: #statement stops the qbot if it is at the home postion
            bot.forward_velocity([0,0])
            bot.stop()
            time.sleep(2)
            break

def main():
    global ID
    global Head_ID
    global Properties
    global iteration
    
    Properties=[] #initalizes Properties as a list
    time.sleep(2) #forces the simulation to pause (makes errors less prevalent)
    iteration = 0 #used for run iteration
    i=1
    while i != 0: #structure runs the module of recycling conatiners
        print(iteration)
        dispense_and_load()
        transfer()
        deposit()
        return_home()
        Head_ID=ID #resets last dispensed container to the searched for container on the next loop
        iteration+=1 #increments iteration effecting simulation loops after the initial run

main() #module runs

##---------------------------------------------------------------------------------------
## STUDENT CODE ENDS
##---------------------------------------------------------------------------------------
update_thread = repeating_timer(2,update_sim)

