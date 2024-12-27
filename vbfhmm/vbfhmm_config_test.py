from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import event as event
from .producers import triggers as triggers
from .producers import genparticles as genparticles
from .producers import muons as muons
from .producers import fsrPhoton as fsrPhoton
from .producers import jets as jets
from .producers import scalefactors as scalefactors
# add by botao
from .producers import lepton as lepton
from .producers import electrons as electrons
from .producers import met as met
from .producers import p4 as p4
from .producers import cr as cr
from .producers import fatjets as fatjets
# end 
from .quantities import nanoAOD as nanoAOD
from .quantities import output as q
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier
from code_generation.rules import RemoveProducer, AppendProducer
from code_generation.systematics import SystematicShift


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
):

    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )

    configuration.add_config_parameters(
        "global",
        {
            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "data/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root",
                    "2016postVFP": "data/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root",
                    "2017": "data/pileup/Data_Pileup_2017_294927-306462_13TeVSummer17_PromptReco_69p2mbMinBiasXS.root",
                    "2018": "data/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root",
                    # "2022": "not/available/yet",
                    "2022": "data/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root",
                }
            ),
            "golden_json_file": EraModifier(
                {
                    "2016preVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2016postVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                    "2022": "data/golden_json/Cert_Collisions2022_355100_362760_GoldenJSON.txt",
                }
            ),
            "PU_reweighting_hist": "pileup",
            "met_filters": EraModifier(
                {
                    "2016preVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                    ],
                    "2016postVFP": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                    ],
                    "2017": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2018": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        #"Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2022": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        # "Flag_BadPFMuonDzFilter", # only since nanoAODv9 available
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                }
            ),
        },
    )

    # vh add triggers (copying htautau mtau TODO)
    configuration.add_config_parameters(
        ["gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "singlemuon_trigger": EraModifier(
                {
                # vh TODO update pT threshold in trigger matching
                    "2022": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2018": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 26,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_mu17",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
                            "ptcut": 17,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_mu8",
                            "hlt_path": "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
                            "ptcut": 8,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_mu10",
                            "hlt_path": "HLT_TripleMu_10_5_5_DZ",
                            "ptcut": 10,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_mu12",
                            "hlt_path": "HLT_TripleMu_12_10_5",
                            "ptcut": 12,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        #{
                        #    "flagname": "trg_single_mu27",
                        #    "hlt_path": "HLT_IsoMu27",
                        #    "ptcut": 28,
                        #    "etacut": 2.5,
                        #    "filterbit": 3,
                        #    "trigger_particle_id": 13,
                        #    "max_deltaR_triggermatch": 0.4,
                        #},
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "ptcut": 28,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.5,
                            "filterbit": 3,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )

    # muon base selection:
    configuration.add_config_parameters(
        ["global","gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "muon_RoccoR_files": EraModifier(
                {
                    "2016preVFP": "data/RoccoR_files/RoccoR2016aUL.txt",
                    "2016postVFP": "data/RoccoR_files/RoccoR2016bUL.txt",
                    "2017": "data/RoccoR_files/RoccoR2017UL.txt",
                    "2018": "data/RoccoR_files/RoccoR2018UL.txt",
                    "2022": "data/RoccoR_files/RoccoR2018UL.txt",
                }
            ),
        }
    )

    configuration.add_config_parameters(
        ["global","gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "min_muon_pt": 5, # ggh, vbf
            "max_muon_eta": 2.4, # ggh, vbf
            "muon_id": "Muon_mediumId", # ggh, vbf cut-based atm https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Medium_Muon
            "muon_iso_cut": 0.4, # ggh, vbf PFIsoLoose dR=0.4 https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideMuonIdRun2#Particle_Flow_isolation
        },
    )
    configuration.add_config_parameters(
        ["e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "max_muon_dxy": 0.05, # vh
            "max_muon_dz": 0.10, # vh
            "max_sip3d" : 8.0, # vh
            #"min_lepmva" : 0.4, 
            "min_muon_mvaTTH" : 0.4,
        },
    )
    # electron base selection:
    configuration.add_config_parameters(
        "global",
        {
            "ele_id": EraModifier(
                {
                    "2016preVFP": "Electron_mvaFall17V2noIso_WP90",
                    "2016postVFP": "Electron_mvaFall17V2noIso_WP90",
                    "2017": "Electron_mvaFall17V2noIso_WP90",
                    "2018": "Electron_mvaFall17V2noIso_WP90",
                    "2022": "Electron_mvaNoIso_WP90",
                }
            ),
        }
    )
    configuration.add_config_parameters(
        "global",
        {
            "min_ele_pt": 20,
            "max_ele_eta": 2.5,
            "upper_threshold_barrel": 1.444,
            "lower_threshold_endcap": 1.566,
        }
    )
    configuration.add_config_parameters(
        ["e2m","m2m","eemm","mmmm","nnmm","fjmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "max_ele_dxy": 0.05,
            "max_ele_dz": 0.10,
            # "ele_id": "Electron_mvaFall17V2noIso_WP90", # 2022, Electron_mvaNoIso_WP90
            "ele_conv_veto": "Electron_convVeto",
            "ele_missing_hits": 2,
            # also need max_sip3d
            # "min_lepmva": 0.4,
            "min_electron_mvaTTH" : 0.4,
        }
    )
    # Muon scale factors configuration
    configuration.add_config_parameters(
        ["gghmm","vbfhmm","e2m","m2m","eemm","mmmm","nnmm","nnmm_dycontrol","nnmm_topcontrol"],
        {
            "muon_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/MUO/2016preVFP_UL/muon_Z.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_Z.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_Z.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
                    "2022": "data/jsonpog-integration/POG/MUO/2018_UL/muon_Z.json.gz",
                }
            ),
            "muon_low_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/MUO/2016preVFP_UL/muon_JPsi.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/MUO/2016postVFP_UL/muon_JPsi.json.gz",
                    "2017": "data/jsonpog-integration/POG/MUO/2017_UL/muon_JPsi.json.gz",
                    "2018": "data/jsonpog-integration/POG/MUO/2018_UL/muon_JPsi.json.gz",
                    "2022": "data/jsonpog-integration/POG/MUO/2018_UL/muon_JPsi.json.gz",
                }
            ),
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",
            "muon_iso_sf_name": "NUM_TightRelIso_DEN_MediumID",
            "muon_sf_year_id": EraModifier(
                {
                    "2016preVFP": "2016preVFP_UL",
                    "2016postVFP": "2016postVFP_UL",
                    "2017": "2017_UL",
                    "2018": "2018_UL",
                    "2022": "2018_UL",
                }
            ),
            "muon_sf_varation": "sf",  # "sf" is nominal, "systup"/"systdown" are up/down variations
            "muon_low_sf_varation": "nominal",  # "sf" is nominal, "systup"/"systdown" are up/down variations
        },
    )
    # electron scale factors configuration
    configuration.add_config_parameters(
        ["e2m","eemm"],
        {
            "ele_sf_file": EraModifier(
                {
                    "2016preVFP": "data/jsonpog-integration/POG/EGM/2016preVFP_UL/electron.json.gz",
                    "2016postVFP": "data/jsonpog-integration/POG/EGM/2016postVFP_UL/electron.json.gz",
                    "2017": "data/jsonpog-integration/POG/EGM/2017_UL/electron.json.gz",
                    "2018": "data/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz",
                    "2022": "data/jsonpog-integration/POG/EGM/2018_UL/electron.json.gz",
                }
            ),
            "ele_id_sf_name": "UL-Electron-ID-SF",
            "ele_sf_year_id": EraModifier(
                {
                    "2016preVFP": "2016preVFP",
                    "2016postVFP": "2016postVFP",
                    "2017": "2017",
                    "2018": "2018",
                    "2022": "2018",
                }
            ),
            "ele_sf_varation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations
        },
    )

    # jet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_jet_pt": 25, # vh
            "max_jet_eta": 4.7, # vh
            # "jet_id": 2,  # default: 2==pass tight ID and fail tightLepVeto
            "jet_id": EraModifier(
                {
                    # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
                    "2016preVFP": 1,  # 1==pass(loose)
                    "2016postVFP": 1,  # 1==pass(loose)
                    "2017": 2,  # 2==pass(tight)
                    "2018": 2,  # 2==pass(tight)
                    "2022": 2,  # 2==pass(tight)
                }
            ),
            "jet_puid": EraModifier(
                {
                    "2016preVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0==fail, 1==pass(loose), 3==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2017": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2018": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                    "2022": 4,  # 0==fail, 4==pass(loose), 6==pass(loose,medium), 7==pass(loose,medium,tight)
                }
            ),
            "jet_puid_max_pt": 50,  # recommended to apply puID only for jets below 50 GeV
            "deltaR_jet_veto": 0.4, # vh jet-muon dR<0.4 overlap removal
            "jet_reapplyJES": False,
            "jet_jes_sources": '{""}',
            "jet_jes_shift": 0,
            "jet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "jet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/jet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/jet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/jet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
                    "2022": '"data/jsonpog-integration/POG/JME/2018_UL/jet_jerc.json.gz"',
                }
            ),
            "jet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"',
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                    "2022": '"Summer19UL18_JRV2_MC"',
                }
            ),
            "jet_jes_tag_data": '""',
            "jet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"',
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                    "2022": '"Summer19UL18_V5_MC"',
                }
            ),
            "jet_jec_algo": '"AK4PFchs"',
        },
    )
    # fat jet base selection:
    # vhbb run2 approval link: fatjet in slide 4
    # https://indico.cern.ch/event/1198083/contributions/5039217/attachments/2507086/4309256/Calandri_HIGPAG_13092022.pdf
    configuration.add_config_parameters(
        "global",
        {
            "min_fatjet_pt": 150, # vhbb selection 250
            "max_fatjet_eta": 2.5, # vhbb selection
            "min_fatjet_MSD": 50, # soft drop mass > 50 GeV
            # "fatjet_id": 2,  # default: 2==pass tight ID and fail tightLepVeto
            "fatjet_id": EraModifier(
                {
                    # Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto
                    "2016preVFP": 1,  # 1==pass(loose)
                    "2016postVFP": 1,  # 1==pass(loose)
                    "2017": 2,  # 2==pass(tight)
                    "2018": 2,  # 2==pass(tight)
                    "2022": 2,  # 2==pass(tight)
                }
            ),
            # may no need fatjet_puid
            "deltaR_fatjet_veto": 0.8, # vh fatjet-muon dR<0.8 overlap removal
            "fatjet_reapplyJES": False,
            "fatjet_jes_sources": '{""}',
            "fatjet_jes_shift": 0,
            "fatjet_jer_shift": '"nom"',  # or '"up"', '"down"'
            "fatjet_jec_file": EraModifier(
                {
                    "2016preVFP": '"data/jsonpog-integration/POG/JME/2016preVFP_UL/fatJet_jerc.json.gz"',
                    "2016postVFP": '"data/jsonpog-integration/POG/JME/2016postVFP_UL/fatJet_jerc.json.gz"',
                    "2017": '"data/jsonpog-integration/POG/JME/2017_UL/fatJet_jerc.json.gz"',
                    "2018": '"data/jsonpog-integration/POG/JME/2018_UL/fatJet_jerc.json.gz"',
                    "2022": '"data/jsonpog-integration/POG/JME/2018_UL/fatJet_jerc.json.gz"',
                }
            ),
            "fatjet_jer_tag": EraModifier(
                {
                    "2016preVFP": '"Summer20UL16APV_JRV3_MC"', # TODO JER tag
                    "2016postVFP": '"Summer20UL16_JRV3_MC"',
                    "2017": '"Summer19UL17_JRV2_MC"',
                    "2018": '"Summer19UL18_JRV2_MC"',
                    "2022": '"Summer19UL18_JRV2_MC"',
                }
            ),
            "fatjet_jes_tag_data": '""',
            "fatjet_jes_tag": EraModifier(
                {
                    "2016preVFP": '"Summer19UL16APV_V7_MC"', # TODO JES tag
                    "2016postVFP": '"Summer19UL16_V7_MC"',
                    "2017": '"Summer19UL17_V5_MC"',
                    "2018": '"Summer19UL18_V5_MC"',
                    "2022": '"Summer19UL18_V5_MC"',
                }
            ),
            "fatjet_jec_algo": '"AK8PFPuppi"',
        },
    )
    # bjet base selection:
    configuration.add_config_parameters(
        "global",
        {
            "min_bjet_pt": 25, # vh
            "max_bjet_eta": EraModifier( # vh
                {
                    "2016preVFP": 2.4,
                    "2016postVFP": 2.4,
                    "2017": 2.5,
                    "2018": 2.5,
                    "2022": 2.5,
                }
            ),
            "btag_cut_loose": EraModifier(  # loose # (vhmm Run2 use DeepCSV)
                {
                    "2016preVFP": 0.2027, # 2016preVFP: 0.2027, 2016postVFP: 0.1918
                    "2016postVFP": 0.1918, # 2016preVFP: 0.2027, 2016postVFP: 0.1918
                    "2017": 0.1355, # 2017: 0.1355
                    "2018": 0.1208, # 2018: 0.1208
                    "2022": 0.1208,
                }
            ),
            "btag_cut_medium": EraModifier(  # medium
                {
                    "2016preVFP": 0.6001, # 2016preVFP: 0.6001, 2016postVFP: 0.5847
                    "2016postVFP": 0.5847, # 2016preVFP: 0.6001, 2016postVFP: 0.5847
                    "2017": 0.4506, # 2017: 0.4506
                    "2018": 0.4168, # 2018: 0.4168
                    "2022": 0.4168,
                }
            ),
        },
    )

    # veto ttH
    configuration.add_config_parameters(
        "global",
        {
            # "vetottH_max_nbjets_loose" : 1,
            # "vetottH_max_nbjets_medium" : 0,
            # "vh_njets" : 3,
        }
    )

    #veto VH
    configuration.add_config_parameters(
        ["gghmm","vbfhmm"],
        {
            # "vetoVH_max_nmuons" : 2,
            # "vetoVH_max_nelectrons" : 0,
        }
    )

    # vbfhmm cuts
    configuration.add_config_parameters(
        ["vbfhmm"],
        {
            "vbf_nmuons" : 2,
            "flag_DiMuonFromHiggs" : 1,
            "flag_LeptonChargeSumVeto" : 2, # sum lepton charge = 0
            #"lead_muon_pt" : 26,
            # "dimuon_pair" : 1, # dimuon_pair in [110,150] >=1
            "vbf_njets" : 2,
            # "lead_jet_pt" : 35, #lead jet pt > 35
            # "sublead_jet_pt" : 25, #sublead jet pt > 25
            # "dijet_mass" : 400, #dijet mass > 400
            # "dijet_eta" : 2.5, #jet-jet delta eta > 2.5
        }
    )

    ###
    configuration.add_config_parameters(
        ["vbfhmm"],
        {
            "RoccoR_seed": 0,
            "RoccoR_error_set": 0,
            "RoccoR_error_member": 0,
        }
    )
    ###

    """
    ## all scopes misc settings
    configuration.add_config_parameters(
        scopes,
        {
            "pairselection_min_dR": 0.5,
        },
    )
    """
    configuration.add_producers(
        "global",
        [
            event.SampleFlags,
            event.PUweights,
            #event.PrefireWeight, #v9 only
            event.Lumi,
            event.MetFilter,
            muons.BaseMuons, # vh
            # vh muon Rochester corr, FSR recovery, GeoFit? TODO
            # vh muon FSR recovery
            electrons.BaseElectrons,
            jets.JetEnergyCorrection, # vh include pt corr and mass corr
            jets.GoodJets, # vh overlap removal with ?base? muons done [need validation]
            jets.GoodBJetsLoose, 
            jets.GoodBJetsMedium, 
            ###
            jets.NumberOfGoodJets,
            jets.NumberOfLooseB, # vh count loose bjets for ttH veto
            jets.NumberOfMediumB, # vh count medium bjets for ttH veto
            # event.VetottHLooseB, # vh veto ttH no more than 1 loose bjet
            # event.VetottHMediumB, # vh veto ttH no more than 1 medium bjet
            met.MetBasics, # build met vector for calculation
            met.BuildGenMetVector,
            jets.JetCollection,
            jets.Calc_MHT,
            #jets.FilterNJets,
            #jets.LVJet1,
            #jets.LVJet2,
            #jets.LVJet3,
            #jets.LVJet4,
            #fatjets.FatJetEnergyCorrection,
            #fatjets.GoodFatJets,
            #fatjets.NumberOfGoodFatJets,
            #fatjets.FatJetCollection,
            #fatjets.LVFatJet1,
        ],
    )
    configuration.add_producers(
        "vbfhmm",
        [
            muons.GoodMuons, # vh tighter selections on muons
            muons.NumberOfGoodMuons,
           # muons.MuonIDCut,
            event.FilterNMuons, # vh ==3 muons
            muons.MuonCollection, # collect ordered by pt
            ###
            event.Mask_DiMuonPair, # dimuonHiggs index
            event.Flag_DiMuonFromHiggs,
            event.HiggsToDiMuonPair_p4, # select the dimuon pairs in [110,150] and order by pt
            ###
            event.DiMuonMassFromZVeto,# has dimuon from Z return mask equal to 0, otherwise return 1
            # event.VetoVHElectron,
            # event.VetoVHMuon,
            #jets.FilterNJets,
            # event.LeadMuonPtCut,
            # event.LeadJetPtCut,
            # event.SubleadJetPtCut,
            # event.DiJetMassCut,
            # event.DiJetEtaCut,
            lepton.LeptonChargeSumVeto,
            ###
            electrons.NumberOfBaseElectrons,
            electrons.ElectronCollection,
            ###
            jets.LVJet1,
            jets.LVJet2,
            # flag cut
            event.FilterFlagDiMuFromH,
            event.FilterFlagLepChargeSum,
            ###
            muons.Mu1_H,
            muons.Mu2_H,
            ###
            event.mumuH_dR,
            ###
            event.mu1_mu2_dphi,
            #
            muons.LVMu1,
            muons.LVMu2,
            triggers.GenerateSingleMuonTriggerFlagsForDiMuChannel, 
            # vh the trigger-matched muon should have pT > 29 (26) for 2017 (2016,18)
            
            #
            p4.mu1_fromH_pt,
            p4.mu1_fromH_eta,
            p4.mu1_fromH_phi,
            p4.mu2_fromH_pt,
            p4.mu2_fromH_eta,
            p4.mu2_fromH_phi,
            p4.met_pt,
            p4.met_phi,
            p4.H_pt,
            p4.H_eta,
            p4.H_phi,
            p4.H_mass,
            p4.jet1_pt,
            p4.jet1_eta,
            p4.jet1_phi,
            p4.jet1_mass,
            p4.jet2_pt,
            p4.jet2_eta,
            p4.jet2_phi,
            p4.jet2_mass,
            jets.DiJetMass,
            jets.DiJetEta,
            jets.Jet1_QGdiscriminator,#v9 only
            jets.Jet2_QGdiscriminator,
            # jets.nSoftJet5,
            jets.Jet1_qgl,
            jets.Jet2_qgl,
           
            p4.genmet_pt,
            p4.genmet_phi,

            scalefactors.MuonIDIso_SF_vbfhmm, #2 mu from H
            fsrPhoton.muon_fsrPhotonIdx_1,
            fsrPhoton.muon_fsrPhotonIdx_2,

            fsrPhoton.muon_fsrPhoton_pt_1,
            fsrPhoton.muon_fsrPhoton_eta_1,
            fsrPhoton.muon_fsrPhoton_phi_1,
            fsrPhoton.muon_fsrPhoton_dROverEt2_1,
            fsrPhoton.muon_fsrPhoton_relIso03_1,
            fsrPhoton.muon_fsrPhoton_pt_2,
            fsrPhoton.muon_fsrPhoton_eta_2,
            fsrPhoton.muon_fsrPhoton_phi_2,
            fsrPhoton.muon_fsrPhoton_dROverEt2_2,
            fsrPhoton.muon_fsrPhoton_relIso03_2,
#
            muons.Muon_pTErr_1,
            muons.Muon_pTErr_2,
            muons.muon1_iso,
            muons.muon2_iso,

            genparticles.dimuon_gen_collection,
            genparticles.genMu1_H,
            genparticles.genMu2_H,
            p4.genmu1_fromH_pt,
            p4.genmu1_fromH_eta,
            p4.genmu1_fromH_phi,
            p4.genmu1_fromH_mass,
            p4.genmu2_fromH_pt,
            p4.genmu2_fromH_eta,
            p4.genmu2_fromH_phi,
            p4.genmu2_fromH_mass,

        ],
    )

    configuration.add_outputs(
        scopes,
        [
            nanoAOD.run,
            q.lumi,
            nanoAOD.event,
            q.puweight,
            #q.prefireweight, #v9 only
            
            q.nmuons,
            q.njets,
            q.nbjets_loose,
            q.nbjets_medium,

            q.met_pt,
            q.met_phi,
            q.genmet_pt,
            q.genmet_phi,
        ],
    )
    configuration.add_outputs(
        ["vbfhmm","e2m","m2m","eemm","mmmm","nnmm","fjmm"],
        [
            q.mu1_fromH_pt,
            q.mu1_fromH_eta,
            q.mu1_fromH_phi,

            q.mu2_fromH_pt,
            q.mu2_fromH_eta,
            q.mu2_fromH_phi,
            
            q.H_pt,
            q.H_eta,
            q.H_phi,
            q.H_mass,

        ],
    )
    configuration.add_outputs(
        "vbfhmm",
        [
            q.jet1_pt,
            q.jet1_eta,
            q.jet1_phi,
            q.jet1_mass,

            q.jet2_pt,
            q.jet2_eta,
            q.jet2_phi,
            q.jet2_mass,

            q.dijet_mass,
            q.dijet_eta,
            
            q.mumuH_dR,

            #
            q.nelectrons,

            ###
            q.mu1_mu2_dphi,
            
	        q.Flag_dimuon_Zmass_veto,
            q.Flag_LeptonChargeSumVeto,
            q.Flag_DiMuonFromHiggs,
            triggers.GenerateSingleMuonTriggerFlagsForDiMuChannel.output_group,

    #        # gen
    #        
    #        #
            q.id_wgt_mu_1,
            q.iso_wgt_mu_1,
            q.id_wgt_mu_2,
            q.iso_wgt_mu_2,
            q.mu1_fromH_ptErr,
            q.mu2_fromH_ptErr,
            q.pt_rc_1,
            q.pt_rc_2,
            # fsr
            q.fsrPhoton_pt_1,
            q.fsrPhoton_eta_1,
            q.fsrPhoton_phi_1,
            q.fsrPhoton_dROverEt2_1,
            q.fsrPhoton_relIso03_1,
            q.fsrPhoton_pt_2,
            q.fsrPhoton_eta_2,
            q.fsrPhoton_phi_2,
            q.fsrPhoton_dROverEt2_2,
            q.fsrPhoton_relIso03_2,
            #q.id_wgt_mu_3,
            #q.iso_wgt_mu_3,
            q.jet1_qgl,
            q.jet2_qgl,
#            #q.nSoftJet5,
            nanoAOD.nSoftJet5,
#            # nanoAOD.nGenJet,
#            # nanoAOD.Muon_pfRelIso04_all,
#            q.jet1_btagDeepFlavQG,#v9 only
#            q.jet2_btagDeepFlavQG,
            q.muon1_iso,
            q.muon2_iso,
        ],
    )
    #
    if sample != "data":
        configuration.add_modification_rule(
            "vbfhmm",
            AppendProducer(
                producers=[event.ApplyRoccoRMC,],
                samples=sample,
                update_output=False,
            ),
        )
    elif sample == "data":
        configuration.add_modification_rule(
            "vbfhmm",
            AppendProducer(
                producers=[event.ApplyRoccoRData,],
                samples=sample,
                update_output=False,
            ),
        )
    ###3252#
    
    # add genWeight for everything but data
    if sample != "data":
        configuration.add_outputs(
            scopes,
            nanoAOD.genWeight,
        )
    ## As now 2022 data has no Jet_puID, so no possible to do JetPUIDCut
    #if era == "2022":
    #    configuration.add_modification_rule(
    #        "global",
    #        RemoveProducer(
    #            producers=[jets.GoodJets,],
    #            samples=sample,
    #        ),
    #    )
    #    configuration.add_modification_rule(
    #        "global",
    #        AppendProducer(
    #            producers=[jets.GoodJets_2022,],
    #            samples=sample,
    #            update_output=False,
    #        ),
    #    )

    configuration.add_modification_rule(
        "global",
        RemoveProducer(
            #producers=[event.PUweights, jets.JetEnergyCorrection, fatjets.FatJetEnergyCorrection, met.BuildGenMetVector,],
            producers=[event.PUweights, jets.JetEnergyCorrection, met.BuildGenMetVector,],
            samples=["data"],
        ),
    )
    configuration.add_modification_rule(
        scopes,
        RemoveProducer(
            producers=[
                p4.genmet_pt,
                p4.genmet_phi,
            ],
            samples=["data"],
        ),
    )
    ##
    configuration.add_modification_rule(
        ["vbfhmm"],
        RemoveProducer(
            producers=[
                genparticles.dimuon_gen_collection,
                genparticles.genMu1_H,
                genparticles.genMu2_H,
                scalefactors.MuonIDIso_SF_vbfhmm,
                p4.genmu1_fromH_pt,
                p4.genmu1_fromH_eta,
                p4.genmu1_fromH_phi,
                p4.genmu1_fromH_mass,
                p4.genmu2_fromH_pt,
                p4.genmu2_fromH_eta,
                p4.genmu2_fromH_phi,
                p4.genmu2_fromH_mass,
            ],
            samples=["data"],
        ),
    )
    # changes needed for data
    # global scope
    configuration.add_modification_rule(
        "global",
        AppendProducer(
            #producers=[jets.RenameJetsData, fatjets.RenameFatJetsData, event.JSONFilter,],
            producers=[jets.RenameJetsData, event.JSONFilter,],
            samples=["data"],
            update_output=False,
        ),
    )

    configuration.add_shift(
        SystematicShift(
            name="MuonIDUp",
            shift_config={"m2m": {"muon_sf_varation": "systup"}},
            producers={
                "m2m": [
                    # scalefactors.Muon_1_ID_SF,
                    # scalefactors.Muon_2_ID_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="MuonIDDown",
            shift_config={"m2m": {"muon_sf_varation": "systdown"}},
            producers={
                "m2m": [
                    # scalefactors.Muon_1_ID_SF,
                    # scalefactors.Muon_2_ID_SF,
                ]
            },
        )
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
