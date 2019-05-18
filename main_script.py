# -*- coding: utf-8 -*-
"""
Created on Mon May 4 13:11:13 2019

@author: Soumyaa
"""
'''
My project has two main classes, USERS and BASESTATIONS.
These classes encapsulate all the attributes pertinent to each of them. Two objects of the base station class are created at the beginning of the project. Every time a user attempts to make a call, an object of the user, a new object of the user class is made. This was done to reduce the space complexity and time complexity of allocating individual arrays to a thousand users, avoid looping through various variable and to ensure the general readability and reusability of the code.
The code is divided into three main segments or functions
1)	Service an attempting user
2)	Service an active call
3)	Printing the said statistics.
Each of these main functions have several auxiliary service functions that are written in different scripts for better fragmentation.
To run the code, please run the script titled ‘main_script.py’
Most of my code reads like english, but comments have been added whereever deemed necessary

'''
####################### importing service classes ##########################
import userlocation as ul
import user_call_service as us
import rsl
import basestations as bs
import get_user_inputs as gui
#############################################################################
#                            VARIABLE ASSIGNMENT
##############################################################################
attempting_user_list=[]
active_user_list=[]
completed_call_list=[]
dropped_call_list=[]
total_completed_calls=0
currently_active_and_attempting_users=0
currently_active_users=0
num_total_attempting_users=0
ho_time=3
successful_handoff=0
hours=gui.get_time()
simulation_time=3600*hours #in seconds
distance_bw_bstn=gui.get_distance()
mobile_speed=gui.get_speed()
num_users=gui.get_users()
num_channels=30
bs1=bs.basestation(0)
bs2=bs.basestation(0)
shadow_val=rsl.compute_shadowing(distance_bw_bstn)
rsl_thresh=-102
bstn_choice=0
call_block_power=0
all_call_attempts=0
completed_calls=0
all_dropped_calls=0
attempted_handoff=0

##############################################################################
#                        CALL SERVICE FUNCTIONS
###############################################################################

def activate_call(serv_bstn,j,other_bstn,isBs1,curr_time):
    global currently_active_users
    serv_bstn.successful_connections+=1
    serv_bstn.active_calls+=1
    serv_bstn.available_channels-=1
    attempting_user_list[j].serving_bstn=serv_bstn
    attempting_user_list[j].other_bstn=other_bstn
    attempting_user_list[j].bstn1=isBs1
    attempting_user_list[j].current_duration=curr_time
    attempting_user_list[j].call_duration=us.get_call_duration()+curr_time
    active_user_list.append(attempting_user_list[j])
    attempting_user_list.pop(j)
    currently_active_users+=1

def terminate_call(k):
    global currently_active_users
    global completed_calls
    completed_call_list.append(k) #creating a list of all complete calls for logs
    active_user_list.remove(k)
    currently_active_users-=1
    k.serving_bstn.available_channels+=1
    k.serving_bstn.active_calls-=1
    k.serving_bstn.completed_calls+=1
    completed_calls+=1
    
def drop_call(k):
    global currently_active_users
    global all_dropped_calls
    dropped_call_list.append(k) #creating a dropped calls list for logs
    active_user_list.remove(k)
    currently_active_users-=1
    k.serving_bstn.active_calls-=1
    k.serving_bstn.available_channels+=1
    k.serving_bstn.dropped_calls+=1
    all_dropped_calls+=1
    
##########################################################################################
#                                USER SERVICE FUNCTIONS
##########################################################################################       
    
def service_attempting_users(curr_time,currently_active_and_attempting_users):
    global num_total_attempting_users
    global bstn_choice
    global call_block_power
    global all_call_attempts
    #get the number of users appearinf at this second
    num_current_attempting_users=us.get_users_attempting_call(currently_active_and_attempting_users,num_users)
    if num_current_attempting_users>0:
        for i in range(num_current_attempting_users):
            attempting_user_list.append(us.assign_locations(num_users))
            all_call_attempts+=1
            num_total_attempting_users+=1
            j=len(attempting_user_list)-1
            #get rsl
            rsl1=rsl.get_rsl(shadow_val,attempting_user_list[j].location)
            rsl2=rsl.get_rsl(shadow_val,distance_bw_bstn-attempting_user_list[j].location)
            #attempt call
            if rsl1>rsl2  and rsl1>rsl_thresh:
                bs1.attempted_calls+=1
                if bs1.available_channels>0:
                    activate_call(bs1,j,bs2,True,curr_time)
                    num_total_attempting_users-=1
                    
                else:
                    bs2.attempted_calls+=1
                    if bs2.available_channels>0 and rsl2>rsl_thresh:
                            activate_call(bs2,j,bs1,False,curr_time)
                            num_total_attempting_users-=1
                    else:
                        bs1.call_block_capacity+=1
                        attempting_user_list.pop(j)
                                        
            elif rsl2>rsl1 and rsl2>rsl_thresh:
                bs2.attempted_calls+=1
                if bs2.available_channels>0:
                    activate_call(bs2,j,bs1,False,curr_time)
                    num_total_attempting_users-=1
                    
                else:
                    bs1.attempted_calls+=1
                    if rsl1>rsl_thresh and bs1.available_channels>0:
                        activate_call(bs1,j,bs2,True,curr_time)
                        num_total_attempting_users-=1
                        
                    else:
                        bs2.call_block_capacity+=1
                        attempting_user_list.pop(j)
            else:
                bs1.attempted_calls+=1
                bs2.attempted_calls+=1
                call_block_power+=1
                attempting_user_list.pop(j)
                
def service_active_users(i):
    global successful_handoff
    global attempted_handoff
    for k in active_user_list:
        ul.update_user_location(k)
        us.update_call_duration(k)
        if k.current_duration>k.call_duration or k.flag:
            terminate_call(k)
        else:
            k.current_duration+=1
            rsl_1=rsl.get_rsl(shadow_val,k.location)
            rsl_2=rsl.get_rsl(shadow_val,distance_bw_bstn-k.location)
            if k.bstn1:
                rsl_serv=rsl_1
                rsl_other=rsl_2
            else:
                rsl_serv=rsl_2
                rsl_other=rsl_1
            if(rsl_serv<rsl_thresh):
                drop_call(k)
    
            else: #ccheck ifhandoff has been inintaitaed
                if k.handoff:
                    if k.ho_duration is i:
                        if(rsl_other>rsl_thresh):
                            k.serving_bstn.available_channels+=1
                            k.serving_bstn.completed_calls+=1
                            temp=k.serving_bstn
                            k.serving_bstn=k.other_bstn
                            k.other_bstn=temp
                            k.serving_bstn.successful_ho+=1
                            successful_handoff+=1
                        
                            if k.bstn1:
                                k.bstn1=False
                            else:
                                k.bstn1=True
                        k.handoff =False
                    else:
                        k.other_bstn.failed_ho+=1
                elif(rsl_other>rsl_serv):
                    k.other_bstn.attempted_calls+=1
                    k.other_bstn.attempted_ho+=1
                    k.handoff=True
                    attempted_handoff+=1
                    if k.other_bstn.available_channels>0:
                        k.other_bstn.available_channels-=1
                        k.ho_duration=i+ho_time
                    else:
                        k.other_bstn.call_block_capacity+=1
                
                
##################################################################################
#                         PRINT FUNCTIONS                      
##################################################################################                        
                        
def printop():  

    
    print("STATISTICS FOR BASESTAION 1:")
    print("please note that all the statistics are cumulative")
    print("CHANNELS IN USE:",(30-bs1.available_channels))
    print("ATTEMPTED CALLS:", bs1.attempted_calls)
    print("SUCCESSFUL CALL CONNECTIONS:",bs1.successful_connections)
    print("CALLS COMPLETED: ",bs1.completed_calls)
    print("ATTEMPTED HANDOFFS (from 1 to 2)",bs1.attempted_ho)
    print("SUCCESSFUL HANDOFFS(from 1 to 2)",bs1.successful_ho)
    print("FAILED HANDOFFS(from 1 to 2)",bs1.attempted_ho-bs1.successful_ho)
    print("CALLS BLOCKED FOR CAPACITY",bs1.call_block_capacity)
    print("CALL BLOCKED POWER", call_block_power)
    print("DROPPED CALLS",bs1.dropped_calls)
    print()
    print()
    print("STATISTICS FOR BASESTAION 2:")
    print("please note that all the statistics are cumulative")
    print("CHANNELS IN USE:",(30-bs2.available_channels))
    print("ATTEMPTED CALLS:", bs2.attempted_calls)
    print("SUCCESSFUL CALL CONNECTIONS:",bs2.successful_connections)
    print("CALLS COMPLETED: ",bs2.completed_calls)
    print("ATTEMPTED HANDOFFS(from 2 to 1)",bs2.attempted_ho)
    print("SUCCESSFUL HANDOFFS (from 2 to 1)",bs2.successful_ho)
    print("FAILED HANDOFFS (from 2 to 1)",bs2.attempted_ho-bs2.successful_ho)
    print("CALLS BLOCKED FOR CAPACITY",bs2.call_block_capacity)
    print("CALL BLOCKED POWER", call_block_power)
    print("DROPPED CALLS",bs2.dropped_calls)
    
    
###################################################################################
#                   MAIN SCRIPT
####################################################################################    
    
for i in range (simulation_time+1):
    service_attempting_users(i,currently_active_and_attempting_users)
    service_active_users(i)
    currently_active_and_attempting_users=len(active_user_list)+len(attempting_user_list)
    if i>0 and i%3600 is 0:
        print()
        print("HOUR:",i/3600)
        printop()
        print()
    
print("\n\nSUMMARY REPORT")
print("ALL CALLS ATTEMPTED:",all_call_attempts)
print("ALL CALLS COMPLETED:",completed_calls)
print("ALL DROPPED CALLS(including handoff attempts)",all_dropped_calls)
print("ALL CALLS BLOCKED FOR POWER",call_block_power)
print("ALL CALLS BLOCKED FOR CAPACITY (including handoff attempts)",bs1.call_block_capacity+bs2.call_block_capacity)
print("ALL HANDOFF ATTEMPTS",attempted_handoff)
print("ALL SUCCESSFUL HANDOFFS:",successful_handoff)              

                    
                    
                
            
           
        
            
            
        
        
        
        
        
            
                
            
               
            
            
