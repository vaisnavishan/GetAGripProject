## ----------------------------------------------------------------------------------------------------------
## Team: Thurs 23
##Team Member 1: Emilie Alain, macID: alaine1, Student Number:400298084
##Team Member 2: Vaisnavi Shanthamoorthy, macID: shanthav, Student Number: 400319038
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.
import random
import sys
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)
# (0.5055, 0.0, 0.0227)

## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------


# Global Variables (Vaisnavi)
home = [0.4066, 0.0, 0.4824] # Q-arm home location
pickup = [0.5055, 0.0, 0.0227] # Pickup location for containers
thres = 0.5 # Set threshold to 0.5

#Emilie found all the small locations & Vaisnavi found all the large bin locations
# Red: small, large 
autoclave1 = [[-0.5893, 0.2321, 0.364], [-0.3744, 0.155, 0.3303]]
# Green: small, large
autoclave2 = [[-0.0055, -0.6337, 0.3675], [0.0, -0.3994, 0.3093]]
# Blue: small, large
autoclave3 = [[-0.0022, 0.6337, 0.3675], [0.0, 0.3993, 0.3095]]



# The following function identifies the ID of the container according to its size and colour (Emilie)
def get_location(identify):
    if identify == 1:
        location = autoclave1[0] # Small red
    elif identify == 2:
        location = autoclave2[0] # Small green 
    elif identify == 3:
        location = autoclave3[0] # Small blue
    elif identify == 4:
        location = autoclave1[1] # Large red
    elif identify == 5:
        location = autoclave2[1] # Large green
    elif identify == 6:
        location = autoclave3[1] # Large blue
    return location


# This function moves the container to the pick up, dropoff and home locations (Vaisnavi)
# If left and right arm are both above the threshold then the arm will move to desired location
def move_end_effector(coordinate):
    while True:
        if arm.emg_left() > thres and arm.emg_right() > thres:
            arm.move_arm(coordinate[0], coordinate[1], coordinate[2]) #dropoff location coordinates
            break


# This function opens the drawer if the container ID corresponds to a large container (containers 4, 5 and 6) (Emilie)
# If the left arm is above the threshold, the right arm is 0 and the container is large, the corresponding drawer will open

def drawer_open(identify):
    while True:
        if identify == 4 and arm.emg_left() > thres and arm.emg_right() == 0:
            arm.open_red_autoclave(True) # Opens red drawer
            break
        elif identify == 5 and arm.emg_left() > thres and arm.emg_right() == 0:
            arm.open_green_autoclave(True) # Opens green drawer
            break
        elif identify == 6 and arm.emg_left() > thres and arm.emg_right() == 0 :
            arm.open_blue_autoclave(True) # Opens blue drawer
            break
        elif identify < 4:
            break
            

# This function controls the gripper in terms of opening and closing it to hold and release the container (Vaisnavi)
# If the right arm is greater than the threshold and the left arm is 0, the gripper will fully close
# If the right arm is between 0 and the threshold and the left arm is 0, the gripper will fully open
def gripper():
    while True:
        if arm.emg_right()  > thres and arm.emg_left() == 0:
            arm.control_gripper(45) # Close gripper fully
            break
        elif arm.emg_right() < thres and arm.emg_right() > 0 and arm.emg_left() == 0:
            arm.control_gripper(-45) # Open gripper fully
            break
                
# This function closes the drawer after the container has been placed in it (Emilie)
# If the left arm is above the threshold, the right arm is 0 and the container is large, the corresponding drawer will close
def drawer_close(identify):
   while True: 
        if identify == 4 and arm.emg_right() == 0 and arm.emg_left() > thres:
            arm.open_red_autoclave(False) # Closes red drawer
            break
        elif identify == 5 and arm.emg_right() == 0 and arm.emg_left() > thres:
            arm.open_green_autoclave(False) # Closes green drawer
            break
        elif identify == 6 and arm.emg_right() == 0 and arm.emg_left() > thres:
            arm.open_blue_autoclave(False) # Closes blue drawer
            break
        elif identify < 4: # Nothing will happen if the container is small
            break
        
#main function (Vaisnavi & Emilie)
def main():
    container_ID = [1, 2, 3, 4, 5, 6] # List of all containers
    random.shuffle(container_ID) # Randomizes spawned container
    for identify in container_ID:
        arm.spawn_cage(identify) # Correct container will spawn
        dropoff = get_location(identify) # Gets coordinates for drop off location
        move_end_effector(pickup) # Arm moves to container's pickup location
        gripper() # Closes gripper
        move_end_effector(home) # Arm moves home
        time.sleep(5)
        move_end_effector(dropoff) # Arm moves to the container's dropoff location
        drawer_open(identify) # Opens drawer if needed (containers 4, 5 and 6)
        gripper() # Opens gripper
        time.sleep(5)
        arm.home() # Q-arm returns home
        drawer_close(identify) # If any drawer is open, it will close
        time.sleep(5)

main() # Calling main function
       
