# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:36:30 2019

@author: Henri_2
"""
import sys, getopt
from interpret import Interpreter
from line_object import Line_object

interpreter = Interpreter()

def do_line(line):
    g = Line_object.parse_line(line)
    interpreter.perform(g)
    return True

def main():
    try:
        # Read file with gcode
        with open(sys.argv[1], 'r') as f:
            for line in f:
                line = line.strip()
                if not do_line(line):
                    break
    except getopt.GetoptError:
      print( 'cnc.py -i <inputfile>')
      sys.exit(2)
    except FileNotFoundError:
        print('Wrong file name')

if __name__ == "__main__":
    main()