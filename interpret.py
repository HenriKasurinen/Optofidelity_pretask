# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 18:48:28 2019

@author: Henri_2
"""

from __future__ import division

from coordinate import Coordinate
from machineclient import MachineClient

client = MachineClient()

"""This class does the actual 
    interpretation of GCode"""
class Interpreter(object):

    def __init__(self):
        """ Initialization"""
        self._home = Coordinate(0.0, 0.0, 0.0)
        # init variables
        self._position = Coordinate(0.0, 0.0, 0.0)
        self._velocity = 0
        self._spindle_rpm = 0
        self._local = None
        self._absoluteCoordinates = 0
        self._plane = None

        """ Performs interpretation."""    
    def perform(self, line_object):
        if line_object is None:
            return None
        
        #Looping through each letter-digit pair in the line
        for a, b in line_object._parameters:
            
            command = a + b
            if command == 'G00' and line_object.has_coordinates() or \
            command == 'G01' and line_object.has_coordinates():
                    
                if command == 'G00':
                    print("Rapid positioning")
                else:
                    print("Linear interpolation")
                    
                new_coordinates = line_object.coordinates()
                
                if new_coordinates.z == None and new_coordinates.y == None:
                    x = float(new_coordinates.x)
                    y = self._position.y
                    z = self._position.z
                    client.move_x(x)
                    self._position = Coordinate(x, y, z)
                elif new_coordinates.x == None and new_coordinates.z == None:
                    y = float(new_coordinates.y)
                    z = self._position.z
                    x = self._position.x
                    client.move_y(y)
                    self._position = Coordinate(x, y, z)
                elif new_coordinates.y == None and new_coordinates.x == None:
                    z = float(new_coordinates.z)
                    x = self._position.x
                    y = self._position.y
                    client.move_z(z)
                    self._position = Coordinate(x, y, z)
                elif new_coordinates.z == None:
                    x = float(new_coordinates.x)
                    y = float(new_coordinates.y)
                    z = self._position.z
                    client.move(x, y, z)   
                    self._position = Coordinate(x, y, z)                     
                else:
                    x = float(new_coordinates.x)
                    y = float(new_coordinates.y)
                    z = float(new_coordinates.z)
                    self._position = Coordinate(x, y, z) 
                    client.move(x, y, z)                   
                
            if command == 'G17':
                self._plane = "XY plane"
                print("XY plane selected")
                
            if command == 'G21':
                print("Programming in mm")
                
            if command == 'G40':
                print("Tool radius compensation OFF")
            
            if command == 'G49':
                print("Tool length offset compensation CANCEL")
                
            if command == 'G80':
                print("Cancel canned-cyle")
                
            if command == 'G94':
                print("Feedrate unit = [mm/s]")
   
            if command == 'T01':
                tool_name = command[1:]
                client.change_tool(tool_name)
            
            if command == 'M6':
                print("Automatic tool change (ATC)")
            
            if command[0] == 'S':
                speed = command[1:]
                client.set_spindle_speed(speed)
              
            if command == 'M03':
                print("Spindle on (clockwise rotation)")
                client.coolant_on()#Not included in the GCode file
                
            if command == 'G90':
                print("Fixed/simple cycle, for roughing")
            
            if command == 'G54':
                print("Work coordinate system")
                
            if command[0] == 'F':
                value = command[1:]
                client.set_feed_rate(value)
            
            if command == 'G28':
                x = self._home.x
                y = self._home.y
                z = self._home.z
                print("Returning home")
                client.move(x, y, z)
                
            if command == 'M09':
                client.coolant_off()
              
            if command[0] == 'O':
                print("Program name: ", command[1:])
                
            if command == 'M30':
                print("Program ended")     