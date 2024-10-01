import os

from reframed import load_cbmodel, save_cbmodel
from reframed import Community, Environment
from reframed import SteadyCom, SteadyComVA

#from optimModels.utils.utils import fix_exchange_reactions_model

basePath = "C:/Users/LENOVO/Desktop/com"

constraints = {}
list_models = []

for file in os.listdir(basePath):
    if file.endswith("_smetana.xml"):
        print(file)
        SBML_FILE = (os.path.join(basePath, file))
        Id = file
        model = load_cbmodel(SBML_FILE, exchange_detection='R_EX_')
        # newModel = fix_exchange_reactions_model(model, include_sink=False)
        try:
            model.biomass_reaction = "R_e_Biomass__cytop"
        except:
            model.biomass_reaction = "R_e_Biomass__cyto"

        for r_id, rxn in model.reactions.items():
            if r_id.startswith('R_EX_'):
                rxn.lb = -10000
        #print(model.id)
        list_models.append(model)

# print(list_models)

community = Community('com_model', list_models)

community_model = community.merged_model

basePath = "C:/Users/LENOVO/Desktop/com/commModel_lambic_beer.xml"

save_cbmodel(community_model, basePath)#, flavor='fbc2')

print('AQUI')
'''
for i in community.merged_model.reactions:
    if "_dra" in i:
        constraints.update({i:(-1000,1000)})
    if "_pool" in i:
        constraints.update({i:(-1000,1000)})
'''

for r_id, rxn in community.merged_model.reactions.items():
    if r_id.startswith('R_EX_'):
        rxn.lb = 0

print(community_model.get_exchange_reactions())
# print(constraints)

minimal_medium = ['R_EX_pnto__R__e', 'R_EX_pi__e', 'R_EX_fe3__e', 'R_EX_nac__e', 'R_EX_btn__e', 'R_EX_ura__e',
                  'R_EX_ade__e', 'R_EX_thym__e', 'R_EX_gua__e', 'R_EX_xan__e', 'R_EX_5fthf__e', 'R_EX_ribflv__e',
                  'R_EX_h2s__e', 'R_EX_pydxn__e', 'R_EX_nh4__e', 'R_EX_mobd__e', 'R_EX_C00378__e', 'R_EX_4abz__e',
                  'R_EX_fol__e', 'R_EX_inost__e', 'R_EX_so4__e', 'R_EX_5aop__e', 'R_EX_pydx__e', 'R_EX_fe2__e']
carbon_source = ['R_EX_glc__D__e']
amino = ['R_EX_his__L__e', 'R_EX_trp__L__e', 'R_EX_met__L__e']  # , 'R_EX_glu__L__e', 'R_EX_gly__e', 'R_EX_ala__L__e',
# 'R_EX_lys__L__e', 'R_EX_asp__L__e', 'R_EX_arg__L__e', 'R_EX_ser__L__e', 'R_EX_phe__L__e', 'R_EX_tyr__L__e',
# 'R_EX_leu__L__e', 'R_EX_pro__L__e', 'R_EX_val__L__e', 'R_EX_thr__L__e', 'R_EX_ile__L__e', 'R_EX_cys__L__e']
oxygen = ['R_EX_o2__e']
biomass_exchange = ['R_EX_e_Biomass__e']
 
constraints = {'R_TI1000156_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.012457893228680123,
               'R_TO0000054_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.18597055436593352}
'''   
constraints ={'R_TR1000054_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.013371149626504542,
              'R_TR2000054_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.1396,
 'R_TO1000207_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.0011365705366094573,
 'R_T0_glycine_mito__cytop_mito_model_Bbruxellensis_07_2021': -0.8631624704066497,
 'R_TR1000107_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.01155248397471791,
 'R_TR1000017_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.002806355623424681,
 'R_TI1000084_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.0013794843353339865,
 'R_TO0000121_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.00023313061520860862,
 'R_T_Lisoleucine__cytop_mito_model_Bbruxellensis_07_2021': 0.018425377461145698,
 'R_TO1000221_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 2.7975822970110946,
 'R_TO2mito__cytop_mito_model_Bbruxellensis_07_2021': 0.07431686737411713,
 'R_T_lvaline__cytop_mito_model_Bbruxellensis_07_2021': -1.6783041883084096,
 'R_TI1000161_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.22330661241159355,
 'R_T__S__Malate_mito__cytop_mito_model_Bbruxellensis_07_2021': -0.9886550345575386,
 'R_T_CTPCMP__cytop_mito_model_Bbruxellensis_07_2021': 0.0000786653448219305,
 'R_TO0000129_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.006557100627384389,
 'R_TO0000220_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.0001923775963205798,
 'R_TI1000033_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.0029738690194637102,
 'R_TZ2900058_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.4251532399579847,
 'R_T_BIOMASS__cytmem_model_Bbruxellensis_07_2021': 0.03999854905635185,
 'R_TR1001977_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.010809267460427867,
 'R_T_h_endo__e_r__model_Bbruxellensis_07_2021': 0.00001674474996205135,
 'R_TR1000393_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.00007055539180975389,
 'R_T_Lalanine__cytop_mito_model_Bbruxellensis_07_2021': 0.008765090147258014,
 'R_T_Fe2__cytop_mito_model_Bbruxellensis_07_2021': 0.00005097822936946932,
 'R_T_ProtoporphyrinogenIX__cytop_mito_model_Bbruxellensis_07_2021': 0.00005097822936946932,
 'R_TI1000156_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.008540239243615468,
 'R_TI1000066_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.005311788155378527,
 'R_TO_Oxobutanoate__cytop_mito_model_Bbruxellensis_07_2021': -0.018425377461145698,
 'R_TI6900100_MITO__mito_model_Bbruxellensis_07_2021': 0.14848080006012584,
 'R_TR1000053_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.015037556714028316,
 'R_T_CO2_endo__e_r__model_Bbruxellensis_07_2021': -0.0000027907916603418916,
 'R_T_Glycerol3phosphate__cytop_mito_model_Bbruxellensis_07_2021': 0.00003933267241096525,
 'R_TO1000305_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.00007389223516603948,
 'R_TR1000039_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.0009627539905885021,
 'R_TZ2900054_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.16532571501453402,
 'R_TI1000035_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.9965436289334634,
 'R_T_h2o__cytop_mito_model_Bbruxellensis_07_2021': -0.8482730102283751,
 'R_T_Glycerol_e__cytmem_model_Bbruxellensis_07_2021': 0.10977179211348907,
 'R_TR1000041_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.007000990999702404,
 'R_TZ2900025_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.000030144789300570834,
 'R_T_Citrate_isocitrate__cytop_mito_model_Bbruxellensis_07_2021': 0.9186735221614655,
 'R_T_C18coa_endo__e_r__model_Bbruxellensis_07_2021': 0.0000027907916603418916,
 'R_T_Oxaloacetate__cytop_mito_model_Bbruxellensis_07_2021': 0.1371607642117595,
 'R_TR0000009_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.02660650069408177,
 'R_TR1000051_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.004692918644812484,
 'R_T_Ethanol__cytop_mito_model_Bbruxellensis_07_2021': -2.0984295127107315,
 'R_TO0010516_e__e_model_Bbruxellensis_07_2021': 14.162276163885473,
 'R_TR1000215_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.0001271635051556735,
 'R_T_Orthophosphate_endo__e_r__model_Bbruxellensis_07_2021': 0.000008372374981025676,
 'R_T_CO2_golgi__golg_model_Bbruxellensis_07_2021': -0.0004703558898838255,
 'R_T_CoA_endo__e_r__model_Bbruxellensis_07_2021': -0.0000027907916603418916,
 'R_TO0000065_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.026269180412322908,
 'R_T_C20CoA_endo__e_r__model_Bbruxellensis_07_2021': 0.0000027907916603418916,
 'R_TO_4Ethylguaiacol__cytmem_model_Bbruxellensis_07_2021': 0.002811450531293354,
 'R_T_CO2__cytop_mito_model_Bbruxellensis_07_2021': -0.47031361963133794,
 'R_T_lOrnithine__cytop_mito_model_Bbruxellensis_07_2021': -0.023370670351105904,
 'R_T_hco3_endo__e_r__model_Bbruxellensis_07_2021': 0.0000027907916603418916,
 'R_TR1000218_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.00008946027843671767,
 'R_T_Phosphatidylserine_golgi_V1__golg_model_Bbruxellensis_07_2021': 0.0004703558898838255,
 'R_T_DGlucono15lactone6phosphate_endo__e_r__model_Bbruxellensis_07_2021': -0.000005581583320683783,
 'R_TO00000NH3_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 1.311230589164839,
 'R_TI1000064_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.010809267460427867,
 'R_T_FRDcm__cytop_mito_model_Bbruxellensis_07_2021': 0.7075436259546776,
 'R_TO1000644_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.00004094597508854563,
 'R_T_Acetaldehyde__cytop_mito_model_Bbruxellensis_07_2021': 2.0984295127107315,
 'R_T_atpamp_endo__e_r__model_Bbruxellensis_07_2021': -0.0000027907916603418924,
 'R_TR1000104_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.0001286372008974975,
 'R_TO0000060_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.010259981139452071,
 'R_T_CO2_e__cytmem_model_Bbruxellensis_07_2021': 4.107147206065413,
 'R_T_Phosphatidylethanolamine_golgi__golg_model_Bbruxellensis_07_2021': -0.0004703558898838255,
 'R_TO1000128_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.005904182190055218,
 'R_TO2ext__cytmem_model_Bbruxellensis_07_2021': 0.1,
 'R_T0_serine_mito__cytop_mito_model_Bbruxellensis_07_2021': 0.41940604755372485,
 'R_T_atp_endo__e_r__model_Bbruxellensis_07_2021': 0.000008372374981025676,
 'R_T_amp_endo__e_r__model_Bbruxellensis_07_2021': -0.0000027907916603418924,
 'R_TO0000119_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.003235703985138779,
 'R_T_5_Aminolevulinate___cytop_mito_model_Bbruxellensis_07_2021': -0.00040782583495575455,
 'R_TO0000027_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.3573644402139271,
 'R_T_Dglucose6phosphate__e_r__model_Bbruxellensis_07_2021': 0.000005581583320683783,
 'R_T_Phosphatidate__cytop_mito_model_Bbruxellensis_07_2021': 0.0000786653448219305,
 'R_TR1000069_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.004368995555092447,
 'R_TR1900007_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -14.162225185656103,
 'R_TO2903031_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.7075436259546776,
 'R_TR2000161_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.21558578780378834,
 'R_TR0011422_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.0013265411362436176,
 'R_T_formate__cytop_mito_model_Bbruxellensis_07_2021': -0.02475820113415574,
 'R_TR1000132_CYTMEM__cytmem_model_Bbruxellensis_07_2021': -0.006227000716127978,
 'R_T_lactate_pyruvate__cytop_mito_model_Bbruxellensis_07_2021': 2.7004368720124425,
 'R_T_acetylcoa_endo__e_r__model_Bbruxellensis_07_2021': 0.0000027907916603418916,
 'R_TO1000023_mito__cytop_mito_model_Bbruxellensis_07_2021': 0.8752727665318407,
 'R_T_lactate__cytop_mito_model_Bbruxellensis_07_2021': 0.09714542499865209,
 'R_T_atp__cytop_mito_model_Bbruxellensis_07_2021': 0.9888516979195934,
 'R_T_Ammonia__cytop_mito_model_Bbruxellensis_07_2021': 1.3035972984805488,
 'R_T_3_Methyl_2_oxobutanoic_acid__cytop_mito_model_Bbruxellensis_07_2021': 1.6345616194660273,
 'R_TI1000322_CYTMEM__cytmem_model_Bbruxellensis_07_2021': 0.00871003140442062,
 'R_TR1000054_CYTMEM__cytmem_model_pdamnosus_comp': -0.3913959362573012,
 'R_TO1000207_CYTMEM__cytmem_model_pdamnosus_comp': 0.003863517131275274,
 'R_TO1000064_CYTMEM__cytmem_model_pdamnosus_comp': 0.010809267460427867,
 'R_TZ2900105_CYTMEM__cytmem_model_pdamnosus_comp': 0.13108032987722057,
 'R_TO1000033_CYTMEM__cytmem_model_pdamnosus_comp': 0.0029738690194637102,
 'R_TO3000331_CYTMEM__cytmem_model_pdamnosus_comp': 0.0007304487030412107,
 'R_TO00000504_CYTMEM__cytmem_model_pdamnosus_comp': -0.00040062626731940127,
 'R_TO1000119_CYTMEM__cytmem_model_pdamnosus_comp': 0.002669080699345789,
 'R_TO1001977_CYTMEM__cytmem_model_pdamnosus_comp': 0.010809267460427867,
 'R_TO1000092_CYTMEM__cytmem_model_pdamnosus_comp': 0.01471385317634407,
 'R_TO1000066_CYTMEM__cytmem_model_pdamnosus_comp': 0.005311788155378527,
 'R_TR1000129_CYTMEM__cytmem_model_pdamnosus_comp': -0.006557100627384389,
 'R_TZ4900019_CYTMEM__cytmem_model_pdamnosus_comp': 0.006145409075857143,
 'R_TO1000156_CYTMEM__cytmem_model_pdamnosus_comp': 0.008540239243615468,
 'R_TR1000039_CYTMEM__cytmem_model_pdamnosus_comp': 0.0009627539905885021,
 'R_TR0000255_CYTMEM__cytmem_model_pdamnosus_comp': -0.0010923555749030823,
 'R_TO1000041_CYTMEM__cytmem_model_pdamnosus_comp': 0.007000990999702404,
 'R_TO1000065_CYTMEM__cytmem_model_pdamnosus_comp': 0.0012458774379117753,
 'R_TR_Orthophosphate_CYTMEM__cytmem_model_pdamnosus_comp': -0.5831182477865751,
 'R_TO1000035_CYTMEM__cytmem_model_pdamnosus_comp': 0.024274124778380552,
 'R_TR2000221_CYTMEM__cytmem_model_pdamnosus_comp': -2.7975822970110946,
 'R_TI3000277_CYTMEM__cytmem_model_pdamnosus_comp': 0.0013265411362436176,
 'R_TR0000314_CYTMEM__cytmem_model_pdamnosus_comp': -0.0007220738068397919,
 'R_TO1000132_CYTMEM__cytmem_model_pdamnosus_comp': 0.006227000716127978,
 'R_TZ4900020_CYTMEM__cytmem_model_pdamnosus_comp': 1.598060197953179,
 'R_TO1000051_CYTMEM__cytmem_model_pdamnosus_comp': 0.004692918644812484,
 'R_TI0000100_CYTMEM__cytmem_model_pdamnosus_comp': 0.10977179211348907,
 'R_TO1900076_CYTMEM__cytmem_model_pdamnosus_comp': 0.007720824607805196,
 'R_TO1000069_CYTMEM__cytmem_model_pdamnosus_comp': 0.004368995555092447,
 'R_T_Nicotinate__cytmem_model_pdamnosus_comp': 0.0005079687734799165,
 'R_TO1000107_CYTMEM__cytmem_model_pdamnosus_comp': 0.01155248397471791,
 'R_T_Pantothenate__cytmem_model_pdamnosus_comp': 0.0002325019660127936,
 'R_T_Biomass__cytmem_model_pdamnosus_comp': 0.03999854905635185,
 'R_TO1000017_CYTMEM__cytmem_model_pdamnosus_comp': 0.002806355623424681,
 'R_TO1000060_CYTMEM__cytmem_model_pdamnosus_comp': 0.0008082826559078072,
 'R_TZ4900024_CYTMEM__cytmem_model_pdamnosus_comp': 0.03842995275703677,
 'R_TO1000322_CYTMEM__cytmem_model_pdamnosus_comp': 0.00871003140442062,
 'R_TI3000378_CYTMEM__cytmem_model_pdamnosus_comp': 0.0006725204043848586,
 'R_TO1000084_CYTMEM__cytmem_model_pdamnosus_comp': 0.0013794843353339865,
 'R_TO1000128_CYTMEM__cytmem_model_pdamnosus_comp': 0.0025813364185469354,
 'R_TO1000053_CYTMEM__cytmem_model_pdamnosus_comp': 0.015037556714028316,
 'R_TO1900148_CYTMEM__cytmem_model_pdamnosus_comp': 0.4047670858838057,
 'R_TR0000011_CYTMEM__cytmem_model_pdamnosus_comp': -0.619507319003884,
 'R_TZ2900110_CYTMEM__cytmem_model_pdamnosus_comp': 0.4251532399579847}
'''
for r_id, rxn in community.merged_model.reactions.items():
    # print(r_id)
    if r_id in minimal_medium:
        rxn.lb = -1000

    if r_id in amino:
        rxn.lb = -0.2

    if r_id in oxygen:
        rxn.lb = -0.1

    if r_id in carbon_source:
        rxn.lb = -0.5
    if r_id in constraints.keys():
        rxn.lb = constraints[r_id]/10
        rxn.ub = constraints[r_id]*10
        print(rxn.lb)
 
print('aqui')

print('===============================================')

for r_id, rxn in community.merged_model.reactions.items():
    if r_id.startswith("R_T"):
        if rxn.lb > 0 and rxn.lb < 1:
            print(r_id, rxn.lb, rxn.ub)

for r_id, rxn in community.merged_model.reactions.items():
    if "Biomass" in r_id:
        print(r_id)

print('===============================================')
print(constraints)
print('===============================================')
print('=== SteadyComm ===')

steady_sol = SteadyCom(community)#, constraints=constraints)

print(steady_sol)

print('===============================================')
# print(steady_sol.values)
print('=== SteadyComVA ===')

steady_solva = SteadyComVA(community)#, constraints=constraints)

print(steady_solva)

# print('aqui')
for r_id, rxn in community.merged_model.reactions.items():
    if r_id.startswith("R_T"):
        # print(r_id)
        pass
