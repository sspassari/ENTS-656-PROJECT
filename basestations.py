# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:08:49 2019

@author: Soumyaa
"""

class basestation:
    def __init__(self,active_users):
        self.currently_active_users=active_users
        self.call_block_power=0
        self.dropped_calls=0
        self.call_block_capacity=0
        self.available_channels=30
        self.active_calls=0
        self.completed_calls=0
        self.attempted_calls=0
        self.failed_ho=0
        self.attempted_ho=0
        self.successful_connections=0
        self.successful_ho=0