# -*- coding: utf-8 -*-
"""
Created on Sat May 11 01:45:11 2019

@author: Soumyaa
"""

total_attempting_users = 0
user_list=[]
import basestations as bs
class user:
	def __init__(self,user_id,location,direction):
		self.user_id=user_id
		self.location=location
		self.bstn1=False #to indicate is base station 1 is the serving base station
		self.flag=False #to indicate the end of call, user moving past
		self.handoff=False #to indicate handoff initiation
		self.direction=direction
		self.serving_bstn=bs
		self.other_bstn=bs
		self.call_duration=0
		self.ho_duration=0
		self.current_duration=0

    
