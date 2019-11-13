#### Verilog Netlist to DEF

```

HOW TO USE THE UTILITY:
An example Resizer command script to translate Verilog to DEF is shown
below.

```
Inside the project directory, write the following commands:
v2DEF.py
LEF_library_file.lef
verilog_netlist_file.v
pins_file.txt
aspect_ratio, eg: 1
core utilization, eg: 0.7

The corresponding DEF file should be outputted in the project directory folder

```

Limitations: 

You have to be inside the project directory for the utility to work; the .v netlist and .txt pins files also have to be inside the project directory and not in a separate folder or even another folder within the project. They have to be in the same directory of the v2DEF.py source code.

``` 
Assumptions: 
 core_area = design_area / (utilization / 100)
 core_width = sqrt(core_area / aspect_ratio)
 core_height = core_width * aspect_ratio
 core = ( core_space, core_space ) ( core_space + core_width, core_space + core_height )
 die = ( 0, 0 ) ( core_width + core_space * 2, core_height + core_space * 2 )

