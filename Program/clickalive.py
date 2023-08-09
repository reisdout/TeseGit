# -*- coding: utf-8 -*-
"""
Created on Mon May  8 13:52:40 2023

@author: visitante
"""

from pynput.mouse import Button, Controller
import time
import random

mouse = Controller()

mouse.position = (2049,293)

dx=0

#only2=2009
only2 = 0

j=1;

while True:
    
    for i in range (0,100):
        x= 2049+dx-only2
        y= random.randint(293, 309)
        dx=(dx+10)%1205#os menores dx são 0 e 5
        #if(2049+dx > 2184 and 2049+dx < 2231):
          #dx=dx+48
        mouse.position = (x,y)
        if (x == 2054-only2 or x ==2049-only2):
            mouse.click(Button.left, 1)
            
        time.sleep(1)
    j=(j+1)%2
    if(j == 0):
        mouse.position = (2024,219)
    mouse.click(Button.left, 1)
    print(mouse.position)    
    time.sleep(30)