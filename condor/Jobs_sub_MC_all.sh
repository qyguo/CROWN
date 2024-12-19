DataOrMC=Data
lines=()
PDs=()
addition=
addition=
conf_name=vbfhmm_config_all_resubv7_v2
build_name=build
output_Path=/eos/user/j/jiahua/MC_UL18_trigger/
file_path=/afs/cern.ch/user/j/jiahua/CROWN/condor/Sample_list/data.txt 
#file_path=/afs/cern.ch/work/q/qguo/Hmumu/hmm_slc7/${build_name}/Sample_list/data_UL18.txt 
SamListPath=/afs/cern.ch/user/j/jiahua/CROWN/condor/Sample_list
# Check if the file exists
if [ -e "$file_path" ]; then
    # Read the file line by line
    while IFS= read -r line; do
        #echo "$line"
        lines+=("$line")
    done < "$file_path"
else
    echo "File not found: $file_path"
    exit 0
fi

i=-1
for element in "${lines[@]}"; do
    ((i += 1))
    if [[ $element == "#"* ]]; then
        continue
    fi
    echo "----->><<-----"
    dataSet__=$(echo "$element" | awk -F'/'  '{print $2}')
    dataSet__=$(echo "$dataSet__" | sed 's/-pythia8//')
    dataSet__=$(echo "$dataSet__" | sed 's/_TuneCP5_13TeV//')
    dataSet__=$(echo "$dataSet__" | sed 's/_TuneCP5_withDipoleRecoil_13TeV//')
    Sam_version=$(echo "$element" | awk -F'/'  '{print $3}')
    Sam_version=$(echo "$Sam_version" | sed 's/RunIISummer//')
    #Sam_version=$(echo "$Sam_version" | sed 's/NanoAODv9-106X_mcRun2_asymptotic_v17-v1//')
    ###
    if [[ $DataOrMC == *Data* ]]; then
        if [[ $Sam_version == *HIPM_UL* ]]; then
            Sam_version=$(echo "$Sam_version" | sed 's/Run20//')
            Sam_version="UL"$(echo "$Sam_version" | sed 's/-.*//')
            Sam_version+="_APV"
        else
            Sam_version=$(echo "$Sam_version" | sed 's/Run20//')
            Sam_version="UL"$(echo "$Sam_version" | sed 's/-UL201.*//')
        fi
    elif [[ $DataOrMC == *MC* ]]; then
        if [[ $Sam_version == *preVFP* ]]; then
            Sam_version=$(echo "$Sam_version" | sed 's/RunIISummer//')
            Sam_version=$(echo "$Sam_version" | sed 's/NanoAOD.*//')
            Sam_version+="_preVFP"
        else
            Sam_version=$(echo "$Sam_version" | sed 's/RunIISummer//')
            Sam_version=$(echo "$Sam_version" | sed 's/NanoAOD.*//')
        fi
        #
    else
        echo "What do you want to run?"
        continue
    fi
    ####
    tmp=$(echo "$element" | awk -F'/'  '{print $3}')
    if [[ $tmp == *_ext* ]]; then
        tmp=$(echo "$tmp" | sed 's/.*ext/_ext/')
        Sam_version+=$tmp
    fi
    Sam=${SamListPath}/${dataSet__}_${Sam_version}${addition}.txt
    echo $Sam
    echo ${dataSet__}_${Sam_version}${addition}
    output_Dir=${output_Path}${dataSet__}_${Sam_version}${addition} 
    # Check if the path exists
    if [ -d "$output_Dir" ]; then
        echo "${output_Dir} already exists."
    else
        mkdir -p "${output_Dir}"
        echo "${output_Dir} created"
    fi
    Job_sub_Name=Job_${dataSet__}_${Sam_version}${addition}.sub
    cp Job_template.sub ${Job_sub_Name}
    if [[ $dataSet__ == WWW_* || $dataSet__ == WWZ_* || $dataSet__ == WZZ_* ]]; then
        Job_type=triboson
    elif [[ $dataSet__ == DYJets* ]]; then
        Job_type=dyjets
    elif [[ $dataSet__ == GluGluToContin* || $dataSet__ == ZZTo4L* || $dataSet__ == ZZTo2L2Nu* || $dataSet__ == WZTo3LNu* || $dataSet__ == WWTo2L2Nu* || $dataSet__ == WZTo2L2Q* || $dataSet__ == ZZTo2L2Q* ]]; then
        Job_type=diboson
    elif [[ $dataSet__ == EWK_LLJJ* ]]; then
       Job_type=zjjew
    elif [[ $dataSet__ == GluGluHToMuMu* ]]; then
        Job_type=gghmm
    elif [[ $dataSet__ == VBFHToMuMu* ]]; then
        Job_type=vbfhmm
    elif [[ $dataSet__ == SingleMuon* ]]; then
        Job_type=data    
    elif [[ $dataSet__ == TTTo2L2Nu* || $dataSet__ == TTToSemiLeptonic* || $dataSet__ == *top* || $dataSet__ == ST_s-channel_4f_leptonDecays* || $dataSet__ == tZq_ll* || $dataSet__ == TT* ]]; then
        Job_type=top
    fi
    echo "What!!!", $Job_type
    ##
    if [[ $build_name != build ]]; then
        sed -i "s/\/build\//\/${build_name}\//g" ${Job_sub_Name}
        sed -i "s/build\//${build_name}\//g" Job_test_${Job_type}.sh
    fi
    echo $Job_test_${Job_type}.sh
    if [[ $conf_name != vbfhmm_config ]]; then
        sed -i "s/vbfhmm_config_dyjets/${conf_name}_${Job_type}/" ${Job_sub_Name}
        sed -i "s/vbfhmm_config_${Job_type}/${conf_name}_${Job_type}/" Job_test_${Job_type}.sh
    fi
    ###
    sed -i "2,5s/Job_test_1/Job_test_${Job_type}/" ${Job_sub_Name}
    # sed -i "5s/vbfhmm_config_dyjets/vbfhmm_config_${Job_type}/" ${Job_sub_Name}
    sed -i "9,11s/hello_/${dataSet__}_${Sam_version}_/" ${Job_sub_Name}
    sed -i "9,11s/Jobs/Jobs${addition}/" ${Job_sub_Name}
    sed -i "7s|$|${output_Dir}|" ${Job_sub_Name}
    #sed -i "6s/$/\/${dataSet__}_${Sam_version}${addition}/" ${Job_sub_Name}
    #cp Job_template.sub Job_${dataSet__}_${Sam_version}.sub
    #sed -i "8,10s/hello_/${dataSet__}_${Sam_version}_/" Job_${dataSet__}_${Sam_version}.sub
    #sed -i "6s/$/\/${dataSet__}_${Sam_version}/" Job_${dataSet__}_${Sam_version}.sub
    #echo "Dir_Out_Name = ${dataSet__}_${Sam_version}" >>Job_${dataSet__}_${Sam_version}.sub
    /cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query "file dataset=${element} instance=prod/global" >& $Sam

    PDs=()
    if [ -e "$Sam" ]; then
        # Read the file line by line
        while IFS= read -r PD; do
            PDs+=("$PD")
        done < "$Sam"
    fi
    for index in "${PDs[@]}";do
        #echo -e "input_name = root://cms-xrd-global.cern.ch/${index}\nQueue" >>Job_${dataSet__}_${Sam_version}.sub
        echo -e "input_name = root://cms-xrd-global.cern.ch/${index}\nQueue" >>${Job_sub_Name}
    done
    echo "condor_submit ${Job_sub_Name}"
    echo "condor_submit ${Job_sub_Name}" >> UL18_slc7.log
    #dataSet__=$(echo "$element" | awk -F'/'  '{print $2}')
    #dataSet__1=$(echo "$element" | awk -F'/'  '{print $3}')
    #echo ${dataSet__} ${dataSet__1}
    #dataSet__1=$(echo "$dataSet__1" | sed 's/-UL2018_MiniAODv.*//')
    #dataSet__1=$(echo "$dataSet__1" | sed 's/Run//')
    #echo  ${dataSet__1}
    #dataSet_2=${dataSet__}_${dataSet__1}
    #echo  ${dataSet_2}
    #dataSet_1=$(echo "$dataSet__" | sed 's/_TuneCP5_13TeV.*pythia8//')
    #contains_dyjets=$(echo "$name" | grep -c "DYJetsToLL_M-50")
    #contains_amcatnlo=$(echo "$name" | grep -c "amcatnloFXFX")
    #contains_madgraphMLM=$(echo "$name" | grep -c "madgraphMLM")
    #contains_ext1=$(echo "$name" | grep -c "ext1")
    #if [[ $element == *"DYJetsToLL_M-50"* ]] && [[ $element == *"madgraphMLM"* ]] && [[ $element == *"ext1"* ]]; then
    #    dataSet_2=${dataSet_1}"_madgraphMLM_ext1"
    #elif [[ $element == *"DYJetsToLL_M-50"* ]] && [[ $element == *"madgraphMLM"* ]] && [[ $element != *"ext1"* ]]; then
    #    dataSet_2=${dataSet_1}"_madgraphMLM"
    #else
    #    dataSet_2=$dataSet_1
    #fi
    #echo $dataSet_2 "<===" $element
    #echo $dataSet_2 "<===" $element

    #cp Job_template.sub Job_${}.sub
    #cp crab_Data_tmp_cfg.py crab_Data_cfg_AA_${dataSet_2}.py
    #sed -i "8s|AAAA|${dataSet_2}|" crab_Data_cfg_AA_${dataSet_2}.py
    #sed -i "22s|AAAA|${element}|" crab_Data_cfg_AA_${dataSet_2}.py
    #sed -i "37s|AAAA|${dataSet_2}|" crab_Data_cfg_AA_${dataSet_2}.py
    #echo "crab submit -c  crab_Data_cfg_AA_${dataSet_2}.py --proxy " '''`voms-proxy-info -path`''' >> Job_sub_crab_Data.log
    #cp crab_MC_cfg_empty.py crab_MC_cfg_AA_${dataSet_2}.py
    #sed -i "7s|AAAA|${dataSet_2}|" crab_MC_cfg_AA_${dataSet_2}.py
    #sed -i "21s|AAAA|${element}|" crab_MC_cfg_AA_${dataSet_2}.py
    #sed -i "33s|AAAA|${dataSet_2}|" crab_MC_cfg_AA_${dataSet_2}.py
    #echo "crab submit -c  crab_MC_cfg_AA_${dataSet_2}.py --proxy " '''`voms-proxy-info -path`''' >> Job_sub_crab.log
done
