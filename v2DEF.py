#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  10 10:13:50 2019

@author: fayed
"""
from lef_util import *
from util import *
import math
import random

SCALE = 2000

#This class should parse LEF files and get info about cells

class Parser:
   
    def __init__(self, leff):
        self.file_lef = leff
        self.macros = {}
        self.metal_layer = {}
        self.VIAs = {}
        self.stcks = []
        self.enlist = []
        self.c_height = -1

#This should retrieve cell heigh and return void

    def get_cell_height(self):
        
        for macro in self.macros:
            self.c_height = self.macros[macro].info["SIZE"][1]
            break

#Perform parsing, open file to read and run till the end of the file

    def parse(self):
        f = open(self.file_lef, "r")
        for line in f:
            info = str_to_list(line)
            if len(info) != 0:
                if len(self.stcks) != 0:
                    this_state = self.stcks[len(self.stcks) - 1]
                    nxt = this_state.parse_next(info)
                else:
                    this_state = Statement()
                    nxt = this_state.parse_next(info)
                if nxt == 0:
                    pass
                elif nxt == 1:
                    if len(self.stcks) != 0:
                        object = self.stcks.pop()
                        if isinstance(object, Macro):
                            self.macros[object.name] = object
                        elif isinstance(object, Layer):
                            self.metal_layer[object.name] = object
                        elif isinstance(object, Via):
                            self.VIAs[object.name] = object
                        self.enlist.append(object)
                elif nxt == -1:
                    pass
                else:
                    self.stcks.append(nxt)
        f.close()

#This should parse the .v netlist 
#it also manages the frequency of some elements occurances within the verilog file

class netlistParsing:
    
    def __init__(self, netlist_file):
        self.netlist_loc = netlist_file
        self.pins = []
        self.wires1 = []
        self.intWires1 = []
        self.wires2 = []
        self.cells = []
        self.cells_sameOrd = [] 
        self.cPins = []
        self.p_w_n = []
        self.pins_cells = []
        self.currentLoc = 0
        self.temp = 0
        self.temp2 = 0
        
    def parse(self):
        file = open(self.netlist_loc, "r")
        for x, line in enumerate(file):
            if line:
                if x != 0 and line != '\n' and line != 'endmodule\n':
                    if line.find('input') != -1:  
                        if line.find('[') == -1:
                            self.pins.append(line[6:len(line) - 2])
                          
                        else:
                            bracket = line.find('[')
                            colons = line.find(':')
                            bracket_right = line.find(']')
                            variables = line[bracket_right + 2:line.find(';')]
                            M_bus = line[bracket + 1: colons]
                            for a in range(0, int(M_bus) + 1):
                                self.pins.append(variables + "<" + str(a) + ">")
                    elif line.find('output') != -1:
                        if line.find('[') == -1:
                            self.pins.append(line[7:len(line) - 2])
                         
                        else:
                            bracket = line.find('[')
                            colons = line.find(':')
                            bracket_right = line.find(']')
                            variables = line[bracket_right + 2:line.find(';')]
                            M_bus = line[bracket + 1: colons]
                            for a in range(0, int(M_bus) + 1):
                                self.pins.append(variables + "<" + str(a) + ">")
                    elif line.find('wire') != -1:         
                        if line.find('[') == -1:
                            first_space = line.find(' ')
                            second_space = line.find(' ', first_space + 1, len(line))
                            self.wires1.append(line[first_space + 1: second_space])
                        
                            bracket = line.find('=')
                            self.intWires1.append(line[bracket + 5: bracket + 6])
                      
                    else:  
                        self.currentLoc = self.currentLoc + 1
                        self.temp = 1
                        self.temp2 = 1
                        first_space = line.find(' ')
                        second_space = line.find(' ', first_space + 1, len(line))
                        self.cells.append(line[0:first_space])
                        self.cells_sameOrd.append(line[first_space + 1: second_space])
                        increment = 0
                        increment2 = 0
                        count_dot = 0
                        temp3 = 0
                        for signn in line:
                            temp3 = 0
                            increment2 = increment2 + 1
                            if signn == '(':
                                increment = increment + 1
                                if increment != 1:
                                    paranthesis_left = line.find('(', increment2 - 1)
                                    parenthesis_right = line.find(')', paranthesis_left)
                                    if self.temp == 1:
                                        self.cPins.append([]) 
                                        self.temp = 0
                                    find_sign = line[paranthesis_left + 1:parenthesis_right]
                                    if find_sign.find('[') != -1:
                                        find_sign = find_sign.replace('[', '<')
                                        find_sign = find_sign.replace(']', '>')
                                    underscore = find_sign.find('_');
                                    if underscore != -1:
                                        flagged = 0
                                        underscore2 = find_sign.find('_', underscore + 1)
                                        if underscore2 == -1:
                                            find_sign = find_sign.replace('_', '.')
                                            for check_element in self.wires2:
                                                if check_element == find_sign:
                                                    flagged = 1
                                        for check_element in self.wires2:
                                                if check_element == find_sign:
                                                    flagged = 1
                                        if flagged == 0:
                                            self.wires2.append(find_sign)
                                    self.cPins[self.currentLoc - 1].append(find_sign)
                                    for check_element in self.p_w_n:
                                        if check_element == find_sign:
                                            temp3 = 1
                                    if temp3 == 0:
                                        self.p_w_n.append(find_sign)
                            
                            if signn == '.':
                                if self.temp2 == 1: 
                                    self.pins_cells.append([])
                                    self.temp2 = 0
                                check_dot = line.find('.', increment2 - 1)
                                check_par = line.find('(', increment2 - 1)
                                inst = line[check_dot + 1:check_par]
                                self.pins_cells[self.currentLoc - 1].append(inst)
                
        file.close()
                           
#This is to parse the pins file

class Parse_Pins: 
           
    def __init__(self, Pins_pa):
        self.pins_Loc = Pins_pa
        self.pins = []
        self.edges = []
        self.metal_layer = []
    
    def parse(self):
        file = open(self.pins_Loc, "r")
        for line in file:
            if line:
                space1 = line.find('\t')
                self.pins.append(line[:space1])
                space2 = line.find('\t', space1 + 1)
                self.edges.append(line[space1 + 1:space2])
                self.metal_layer.append(line[space2 + 1:len(line) - 1])
                                
if __name__ == '__main__':

    LEF_Location = input("Your LEF file path is, osu035_stdcells: ")
    LEF_Parsing = Parser(LEF_Location)
    LEF_Parsing.parse()

    netlist_Location = input("Your .v file to be converted's path: ")
    parse_netlist = netlistParsing(netlist_Location)
    parse_netlist.parse()
    
    design = netlist_Location[:netlist_Location.find('.')]
    
    
    Pins_Location = input("Your .txt Pins file: ")
    Pins_Parsingg = Parse_Pins(Pins_Location)
    Pins_Parsingg.parse()

#Identify the aspect ratio and core utilization
    aspect_ratio= input("aspect ratio is: ")
  

    core_utilization= input("core utilization is: ")


    default_micron = 100
    
    nets = parse_netlist.p_w_n
    pins = parse_netlist.pins
    cell_pins = parse_netlist.cPins
    this__cell = parse_netlist.cells_sameOrd
    pins_cell_ = parse_netlist.pins_cells
    check_cell = parse_netlist.cells
    
    define_width = 0
    define_height = 0
    core_area = 0
    cells_area = 0
    core_utilization = 0.85    
    aspect_ratio = 1    
   
    area_of_cell = []
    for cell in check_cell:
        sp_cell = LEF_Parsing.macros[cell]
        area_of_cell.append(sp_cell.info["SIZE"][0] * sp_cell.info["SIZE"][1] * default_micron * default_micron)
            
    for Modified_area in area_of_cell:
        cells_area = cells_area + Modified_area
    
    define_width = math.sqrt((cells_area) / (core_utilization * aspect_ratio))
    
    define_height = aspect_ratio * define_width
    
    temp = define_width % 160
    if temp != 0:
        temp2 = 160 - temp
        define_width = define_width + temp2
    
    cell_height = int(LEF_Parsing.c_height) * default_micron
    temp = define_height % cell_height
    if temp != 0:
        temp2 = cell_height - temp
        define_height = define_height + temp2
        
    
    core_area = define_width * define_height

    write_to_DEF = open(design + ".def", "w+")
    
    write_to_DEF.write('VERSION 5.6 ;\nNAMESCASESENSITIVE ON ;\nDIVIDERCHAR "/" ;\nBUSBITCHARS "<>" ;\nDESIGN ' + design + ' ;\nUNITS DISTANCE MICRONS ' + str(default_micron) + ' ;\n\n')
    
    factor_x = len(pins) * 400
    factor_y = len(pins) * 400
    start_x = -480
    start_y = -400
    
    begin_x = start_x + factor_x
    begin_y = start_y + factor_y
    cell_height = LEF_Parsing.c_height * default_micron 
    
    end_x = math.floor(start_x + factor_x + define_width + factor_x)
    end_y = math.floor(start_y + factor_y + define_height + factor_y)
    
    write_to_DEF.write('DIEAREA ( ' + str(start_x) + ' ' + str(start_y) + ' ) ( ' + str(end_x) + ' ' + str(end_y) + ' ) ;\n\n')
    
    for n in range(1,5):
        if n % 2 == 1:
            st = start_y
            en = end_y
        else:
            st = start_x
            en = end_x
            
        step = LEF_Parsing.metal_layer["metal" + str(n)].pitch * default_micron
        
        direction = LEF_Parsing.metal_layer["metal" + str(n)].direction
        if direction == "HORIZONTAL":
            t = "Y"
        elif direction == "VERTICAL":
            t = "X"
        
        num = (((-st) + en) / int(step)) + 1
        write_to_DEF.write("TRACKS " + t + " " + str(st) + " DO " + str(int(num)) + " STEP " + str(int(step)) + " LAYER metal" + str(n) + " ;\n")
        
    write_to_DEF.write("\n")
    
    write_to_DEF.write("COMPONENTS " + str(len(this__cell)) + " ;\n")
    
    for i,elem in enumerate(this__cell):
        write_to_DEF.write("- " + elem + " " + check_cell[i] + " + PLACED ( 0 0 ) ; \n")
                
    write_to_DEF.write("END COMPONENTS\n\n")

    pins_file = Pins_Parsingg.pins
    side = Pins_Parsingg.edges
    metal_layer = Pins_Parsingg.metal_layer
    
    for i,elem in enumerate(metal_layer):
        if elem == "M1":
            metal_layer[i] = "metal1"
        elif elem == "M2":
            metal_layer[i] = "metal2"
        elif elem == "M3":
            metal_layer[i] = "metal3"
        elif elem == "M4":
            metal_layer[i] = "metal4"
    
    write_to_DEF.write("PINS " + str(len(pins)) + " ;\n")
    
    new_index_M1_y = begin_y
    new_index_M3_y = begin_y
    new_index_M2_x = begin_x
    new_index_M4_x = begin_x
    
    for i,elem in enumerate(pins_file):
        
        step_M1 = LEF_Parsing.metal_layer["metal1"].pitch * default_micron
        
        step_M3 = LEF_Parsing.metal_layer["metal3"].pitch * default_micron
        
        step_M2 = LEF_Parsing.metal_layer["metal2"].pitch * default_micron
        
        step_M4 = LEF_Parsing.metal_layer["metal4"].pitch * default_micron
        
        check_if_used = 0
        write_to_DEF.write("- " + elem + " + NET " + elem + "\n")
        write_to_DEF.write("  + LAYER " + metal_layer[i] + " ( 0 0 ) ( 1 1 )\n")
        
        if side[i] == "L":

            if metal_layer[i] == "metal1":

                write_to_DEF.write("  + PLACED ( " + str(start_x) + " " + str(int(new_index_M1_y)) + " ) N ;\n")
                new_index_M1_y = new_index_M1_y + step_M1
            elif metal_layer[i] == "metal3":
                write_to_DEF.write("  + PLACED ( " + str(start_x) + " " + str(int(new_index_M3_y)) + " ) N ;\n")
                new_index_M3_y = new_index_M3_y + step_M3
                
        elif side[i] == "R":
            
            if metal_layer[i] == "metal1":
                write_to_DEF.write("  + PLACED ( " + str(end_x) + " " + str(int(new_index_M1_y)) + " ) N ;\n")
                new_index_M1_y = new_index_M1_y + step_M1
            elif metal_layer[i] == "metal3":
                write_to_DEF.write("  + PLACED ( " + str(end_x) + " " + str(int(new_index_M3_y)) + " ) N ;\n")
                new_index_M3_y = new_index_M3_y + step_M3
                
        elif side[i] == "U":
            
            if metal_layer[i] == "metal2":
                write_to_DEF.write("  + PLACED ( " + str(int(new_index_M2_x)) + " " + str(start_y) + " ) N ;\n")
                new_index_M2_x = new_index_M2_x + step_M2
            elif metal_layer[i] == "metal4":
                write_to_DEF.write("  + PLACED ( " + str(int(new_index_M4_x)) + " " + str(start_y) + " ) N ;\n")
                new_index_M4_x = new_index_M4_x + step_M4
                
        elif side[i] == "D":
            
            if metal_layer[i] == "metal2":
                write_to_DEF.write("  + PLACED ( " + str(int(new_index_M2_x)) + " " + str(end_y) + " ) N ;\n")
                new_index_M2_x = new_index_M2_x + step_M2
            elif metal_layer[i] == "metal4":
                write_to_DEF.write("  + PLACED ( " + str(int(new_index_M4_x)) + " " + str(end_y) + " ) N ;\n")
                new_index_M4_x = new_index_M4_x + step_M4
       
    write_to_DEF.write("END PINS\n\n")

    write_to_DEF.write("NETS " + str(len(nets)) + " ;\n")
    
    for elem in nets:
        check = 0
        found = []
        repeated1 = []
        repeated = []
        increment5 = 0
        
        write_to_DEF.write("- " + elem + "\n")
        
        for row in range(len(cell_pins)):
            for p in range(len(cell_pins[row])):
                if cell_pins[row][p] == elem:
                    found.append(row)
                    repeated1.append(p)
        for item in pins:
            if item == elem:

                write_to_DEF.write("  ( PIN " + elem + " )\n")
                
        for row in reversed(found):
            increment5 = 0
            called_ = this__cell[row]
            
            for y in range(len(this__cell)):
                if called_ == this__cell[y]:
                    repeated = y

            for second_row in reversed(repeated1):
                increment5 = increment5 + 1
                if increment5 <= 1:
                    write_to_DEF.write("  ( " + this__cell[row] + " " + pins_cell_[repeated][repeated1[-1]] + " )")
            
            if row == found[0]:
                write_to_DEF.write(" ;\n")
            else:
                write_to_DEF.write("\n")
            del repeated1[-1]
    write_to_DEF.write("END NETS\n\nEND DESIGN")
                    
    write_to_DEF.close()
