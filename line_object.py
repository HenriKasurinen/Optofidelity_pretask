# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 18:24:05 2019

@author: Henri_2
"""

import re
from coordinate import Coordinate

# extract letter-digit pairs
g_pattern = re.compile('([A-Z])([-+]?[0-9.]+)')
# white spaces and comments start with ';' and in '()'
clean_pattern = re.compile('\s+|\(.*?\)|;.*')
"""This class represents one line
   of GCode"""
class Line_object(object):
    
    """Initialization"""
    def __init__(self, parameters):
        self._parameters = parameters
        
    """Returns wanted argument from the object.
        If argument is not present, returns None"""    
    def get(self, arg_name, default = None):
        for a, b in self._parameters:
            if a == arg_name:
                return float(b)
        return default

        """ Get coordinates from line object 
            as coordinate object"""
    def coordinates(self, default = None):
        x = self.get('X', default)
        y = self.get('Y', default)
        return Coordinate(x, y)
    
        """Move the spindle up and down the z-axis"""
    def spindle_height(self, default = None):
        z = self.get('Z', default)
        return z
    
        """ Checsk if line object as at least
            one coordinate"""
    def has_coordinates(self):
        for a, b in self._parameters:
            if a == 'X' or a == 'Y' or a == 'Z':
                return a, b
            
        """Gets one line of GCode, removes
            redundant characters, and saves
            all commands as letter-digit pairs"""
    def parse_line(self, line):
        line = line.upper()
        line = re.sub(clean_pattern, '', line)
        if len(line) == 0:
            return None
        if line[0] == '%':
            return None
        m = g_pattern.findall(line)
        i = 0
        pairs = []
        for i in range(len(m)):
            pairs.append(m[i])
            
        parameters = pairs
        return Line_object(parameters)
