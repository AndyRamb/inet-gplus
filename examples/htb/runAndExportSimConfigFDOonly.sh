#!/bin/bash

inet="../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5"
inet_gpl="../../inet-gpl"


helpFunction()
{
   echo ""
   echo "Will run a single run from a single config and ini file."
   echo "Usage: $0 -i iniFile -c config -t numThreads"
   echo -e "\t-i Omnet++ INI file containing the congfig to run"
   echo -e "\t-c Config for the scenario you want to run"
   echo -e "\t-s Number of slices in the scenario you want to run"
   echo -e "\t-n Number of applications"
   exit 1 # Exit script after printing help
}

while getopts "i:c:s:n:" opt
do
   case "$opt" in
      i ) iniFile="$OPTARG" ;;
      c ) config="$OPTARG" ;;
      s ) slices="$OPTARG" ;;
      n ) nApps="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$iniFile" ] || [ -z "$config" ] || [ -z "$slices" ] || [ -z "$nApps" ]
then
   echo "Some or all of the parameters are empty";
   helpFunction
fi

###### Run a single simulation config. Note: The config should only have one run here!!! ######
###### You may need to relink the paths depending on your machine!!!!! ######

### Marcin's Version ###
# opp_runall -j1 -b1 opp_run ${iniFile} -u Cmdenv -c ${config} -l ../../../omnetpp-5.5.1/samples/inet4/src/INET -m -n .:../src:../../../omnetpp-5.5.1/samples/inet4/src:../../../omnetpp-5.5.1/samples/inet4/examples:../../../omnetpp-5.5.1/samples/inet4/tutorials:../../../omnetpp-5.5.1/samples/inet4/showcases

########
# opp_runall -j1 -b1 opp_run ${iniFile} -u Cmdenv -c ${config} -l ../../../../../installs/omnetpp-5.5.1/samples/inet4/src/INET -m -n .:../src:../../../../../installs/omnetpp-5.5.1/samples/inet4/src:../../../../../installs/omnetpp-5.5.1/samples/inet4/examples:../../../../../installs/omnetpp-5.5.1/samples/inet4/tutorials:../../../../../installs/omnetpp-5.5.1/samples/inet4/showcases

### OMNeT++ 6.0 version ###
#../src/improved5gNS ${iniFile} -m -u Cmdenv -c ${config} -n .:../src:../../inet/examples:../../inet/showcases:../../inet/src:../../inet/tests/validation:../../inet/tests/networks:../../inet/tutorials:../../inet-gpl/src:../../inet-gpl/examples --image-path=../../inet/images -l ../../inet/src/INET -l ../../inet-gpl/src/INETGPL ../src/improved5gNS ${iniFile} -m -u Cmdenv -c ${config} -n .:../src:../../inet/examples:../../inet/showcases:../../inet/src:../../inet/tests/validation:../../inet/tests/networks:../../inet/tutorials:../../inet-gpl/src:../../inet-gpl/examples --image-path=../../inet/images -l ../../inet/src/INET -l ../../inet-gpl/src/INETGPL 

### OMNeT++ 6.0 Andreas version###
#opp_run ${iniFile} -m -u Cmdenv -c ${config} -n .:../src:${inet}/examples:${inet}/showcases:${inet}/src:${inet}/tests/validation:${inet}/tests/networks:${inet}/tutorials:${inet_gpl}/src:${inet_gpl}/examples --image-path=${inet}/images -l ${inet}/src/inet -l ${inet_gpl}/src/inetgpl ../src/improved5gNS ${iniFile} -m -u Cmdenv -c ${config} -n .:../src:${inet}/examples:${inet}/showcases:${inet}/src:${inet}/tests/validation:${inet}/tests/networks:${inet}/tutorials:${inet_gpl}/src:${inet_gpl}/examples --image-path=${inet}/images -l ${inet}/src/INET -l ${inet_gpl}/src/INETGPL 
#cd ../../inet-gpl/examples
#opp_run -m -u Cmdenv -c ${config} -n ../../src:..:../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/examples:../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/showcases:../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/src:../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tests/validation:../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tests/networks:../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tutorials --image-path=../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/images -l ../../src/INETGPL -l ../../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/src/INET ${iniFile}

#../src/improved5gNS ../../inet-gpl/examples/htb/omnetpp.ini -m -u Cmdenv -c scenarioUDP1 -n .:../src:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/examples:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/showcases:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/src:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tests/validation:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tests/networks:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tutorials:../../inet-gpl/src:../../inet-gpl/examples --image-path=../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/images -l ../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/src/inet -l ../../inet-gpl/src/inetgpl ../src/improved5gNS ../../inet-gpl/examples/htb/omnetpp.ini -m -u Cmdenv -c scenarioUDP1 -n .:../src:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/examples:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/showcases:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/src:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tests/validation:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tests/networks:../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/tutorials:../../inet-gpl/src:../../inet-gpl/examples --image-path=../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/images -l ../../../Downloads/omnetpp-6.0.1/project/Fordypningsprosjekt/inet4.5/src/inet -l ../../inet-gpl/src/inetgpl 


### INET Server Version ###
# opp_runall -j1 -b1 opp_run ${iniFile} -u Cmdenv -c ${config} -l /home/marcin/omnetpp-5.5.1/samples/inet4/src/INET -m -n .:../src:/home/marcin/omnetpp-5.5.1/samples/inet4/src:/home/marcin/omnetpp-5.5.1/samples/inet4/examples:/home/marcin/omnetpp-5.5.1/samples/inet4/tutorials:/home/marcin/omnetpp-5.5.1/samples/inet4/showcases

### Vagrant 1 ###
# opp_run ${iniFile} -u Cmdenv -c ${config} -m -n .:../src:../../../../inet4/src:../../../../inet4/examples:../../../../inet4/tutorials:../../../../inet4/showcases -l ../../../../inet4/src/INET 2>&1 | tee  ${config}.txt # Vagrant 1

### Vagrant 2 ###
# opp_runall -j1 -b1 opp_run ${iniFile} -u Cmdenv -c ${config} -m -n .:../src:../../../../../inet4/src:../../../../../inet4/examples:../../../../../inet4/tutorials:../../../../../inet4/showcases -l ../../../../../inet4/src/INET 2>&1 | tee ${config}.txt # Vagrant 2

### Vagrant 3 ###
# opp_runall -j1 -b1 opp_run ${iniFile} -u Cmdenv -c ${config} -m -n .:../src:../../../../../inet4/src:../../../../../inet4/examples:../../../../../inet4/tutorials:../../../../../inet4/showcases -l ../../../../../inet4/src/INET 2>&1 | tee ${config}.txt # Vagrant 2

###### Export results from OMNet++ to csv ######
cd results
#######
./export_results_individual_NS_onlyFDO.sh -f 0 -l 0 -r ${slices} -s ${config} -o ${config} -t ${config} -d ${config}

### Export some queue scalars as well ###
# ./export_results_individual_NS_onlyR1Queues.sh -f 0 -l 0 -r ${slices} -s ${config} -o ../../../analysis/${config} -t ${config} -d ${config}

###### Extract necessary information from the csv's ######
cd ${config}
name="scenarioUDP1_0_VID0_LVD0_FDO1_SSH0_VIP0" #$(ls)
cd ..
python3 parseResHTBtest.py ${config} ${slices} ${name} ${nApps}
#python3 parseResHTBtest.py scenarioUDP1 0 scenarioUDP1_1_VID0_LVD0_FDO1_SSH0_VIP0 5
# python3 parseResNE.py ${config} ${slices} ${name} # Extract required information from the scavetool csv's

echo "Simulation, exports and initial plots are complete for ${config}";