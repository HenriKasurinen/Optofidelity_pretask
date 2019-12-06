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
        self._home = Coordinate(0.0, 0.0)
        self._position = Coordinate(0.0, 0.0)
        self._z = 10.0


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
                new_z = line_object.spindle_height()
                
                if new_coordinates.y == None and new_z == None:
                    x = float(new_coordinates.x)
                    y = self._position.y
                    client.move_x(x)
                    self._position = Coordinate(x, y)
                elif new_coordinates.x == None and new_z == None:
                    y = float(new_coordinates.y)
                    x = self._position.x
                    client.move_y(y)
                    self._position = Coordinate(x, y)
                elif new_coordinates.y == None and new_coordinates.x == None:
                    z = float(new_z)
                    self._z = z
                    client.move_z(z)
                elif new_z == None:
                    x = float(new_coordinates.x)
                    y = float(new_coordinates.y)
                    z = self._z
                    client.move(x, y, z)   
                    self._position = Coordinate(x, y)                     
                else:
                    x = float(new_coordinates.x)
                    y = float(new_coordinates.y)
                    z = float(new_z)
                    self._position = Coordinate(x, y) 
                    self._z = z
                    client.move(x, y, z)                   
                
            if command == 'G17':
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
            
            if command == 'M06':
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
                z = self._z
                print("Returning home")
                client.move(x, y, z)
                if line_object.has_coordinates(
                        ) and line_object.spindle_height() != None:
                    z = float(line_object.spindle_height())
                    self._z = z
                    client.move_z(z)
                                   
            if command == 'M09':
                client.coolant_off()
              
            if command[0] == 'O':
                print("Program name: ", command[1:])
                
            if command == 'M5':
                print("Spindle stop")
                
            if command == 'M30':
                print("Program ended")     