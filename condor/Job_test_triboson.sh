#!/bin/bash
echo "Starting job on `data`\n" #Data/time of start of job
echo "Running on: `uname -a`\n" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`\n" #Operating System on that node

source /afs/cern.ch/cms/cmsset_default.sh

cd /afs/cern.ch/user/j/jiahua/CROWN

source init.sh vbfhmm
source /cvmfs/sft.cern.ch/lcg/views/LCG_102rc1/x86_64-centos7-gcc11-opt/setup.sh

cd build/bin
export X509_USER_PROXY=$1
voms-proxy-info -all
voms-proxy-info -all -file $1
out_name=$(echo "$3" | awk -F'/' '{print $NF}')
echo ${2}/${out_name}
./vbfhmm_config_triboson_2018  ${2}/${out_name} $3
