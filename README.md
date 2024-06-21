# INET-GPLUS is the extention of INET-GPL that includes the framework needed for dynamic resource allocations in the HTB.
This project was developed in the master thesis: Dynamic Resource Allocation and QoE-aware Packet Scheduling using HTB in OMNeT++
Its code can be found on https://github.com/AndyRamb/improved5gNS2

To run this project you need:
- OMNeT++ 6.0.2 or later.
- inet4.5 to be installed and linked within the OMNeT++ program as a project reference to compile and utilise this project.

To utilise the dynamic behaviours implemented an array containing changetimes needs to be defined in the .ini configuration file:
*.router*.ppp[0].queue.scheduler.changeTimes = []

The HTB configuration file has switched formats to be a JSON file. Each class can now also include rate variables for future rates at specific changeTimes.
Within the .ini file you include this:
*.router*.ppp[0].queue.htbTreeConfig = readJSON("<conffile>.json")
