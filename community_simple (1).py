import csv
import os

from framed import load_cbmodel, save_cbmodel, Environment, pFBA
from framed.community.model import Community
#from optimModels.utils.utils import fix_exchange_reactions_model
from optimModels.simulation.simul_problems import StoicSimulationProblem
from reframed import SteadyCom

community_name = []
organism_list = []
o = []

basePath = "C:/Users/Models"
list_models = []
constraints = {}

for file in os.listdir(basePath):
    if not file.endswith("model.xml"):
        SBML_FILE = (os.path.join(basePath, file))
        Id = file
        newModel = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
        #newModel = fix_exchange_reactions_model(newModel)
        try:
            newModel.biomass_reaction = "R_e_Biomass__cytop"
        except:
            newModel.biomass_reaction = "R_e_Biomass__cyto"
        print(newModel.biomass_reaction)
        list_models.append(newModel)

community = Community('lambic', models = list_models, extracellular_compartment_id = 'C_00001', interacting = True)
newCommModel = community.merged
Environment.empty(newCommModel, inplace=True)

print(newCommModel.id)
newCommModel = fix_exchange_reactions_model(newCommModel)

save_cbmodel(newCommModel, basePath + "/commModel_lambic_beer.xml", flavor='fbc2')
'''
SBML_FILE = (os.path.join(basePath, "commModel_beer.xml"))
model = load_cbmodel(SBML_FILE, exchange_detection_mode='R_EX_')
model.biomass_reaction = "R_Community_Growth"
'''
minimal_medium = ['R_EX_M_pnto__R__e_pool', 'R_EX_M_pi__e_pool', 'R_EX_M_fe3__e_pool', 'R_EX_M_nac__e_pool', 'R_EX_M_ura__e_pool', 'R_EX_M_ade__e_pool', 'R_EX_M_thym__e_pool', 'R_EX_M_gua__e_pool', 'R_EX_M_xan__e_pool', 'R_EX_M_5fthf__e_pool', 'R_EX_M_ribflv__e_pool', 'R_EX_M_nh4__e_pool', 'R_EX_M_C00378__e_pool', 'R_EX_M_4abz__e_pool', 'R_EX_M_fol__e_pool', 'R_EX_M_inost__e_pool', 'R_EX_M_so4__e_pool', 'R_EX_M_mobd__e_pool', 'R_EX_M_pydx__e_pool', 'R_EX_M_5aop__e_pool', 'R_EX_M_btn__e_pool', 'R_EX_M_pydxn__e_pool']

carbon_source = ['R_EX_M_glc__aD__e_pool']

amino = ['R_EX_M_his__L__e_pool', 'R_EX_M_trp__L__e_pool', 'R_EX_M_met__L__e_pool', 'R_EX_M_glu__L__e_pool', 'R_EX_M_gly__e_pool', 'R_EX_M_ala__L__e_pool', 'R_EX_M_lys__L__e_pool', 'R_EX_M_asp__L__e_pool', 'R_EX_M_arg__L__e_pool', 'R_EX_M_ser__L__e_pool', 'R_EX_M_phe__L__e_pool', 'R_EX_M_tyr__L__e_pool', 'R_EX_M_leu__L__e_pool', 'R_EX_M_pro__L__e_pool', 'R_EX_M_val__L__e_pool', 'R_EX_M_thr__L__e_pool', 'R_EX_M_ile__L__e_pool', 'R_EX_M_cys__L__e_pool']

oxygen = ['R_EX_M_o2__e_pool']

#so4 = ['R_EX_M_so4__e_pool']

#KO_pool = ['R_EX_M_no2__e_pool', 'R_EX_nh4_e_model_nvulgaris', 'R_EX_hco3_e_model_nvulgaris', 'R_EX_hdca_e_model_nvulgaris']


for r_id, rxn in newCommModel.reactions.items():
    if rxn.is_exchange:
        rxn.lb = -1000 if rxn.lb is None else rxn.lb
        rxn.ub = 1000 if rxn.ub is None else rxn.ub

print(newCommModel.biomass_reaction)

simulProb = StoicSimulationProblem(newCommModel, objective={'R_Community_Growth': 1}, method="pFBA")

#pfba = simulProb.simulate()

#essential = simulProb.find_essential_drains()
#print("Essential; ", essential)

for i in minimal_medium:
    constraints.update ({i:(-1000, 0)})

for i in amino:
    constraints.update({i: (-0.2, 0)})

for i in oxygen:
    constraints.update({i: (-0.1, 0)})

#for i in KO_pool:
#    constraints.update({i: (0, 0)})

for i in carbon_source:
    constraints.update({i: (-2, 0)})

#for i in so4:
#    constraints.update({i: (-1, 0)})


print(constraints)
'''

sol = StoicSimulationProblem(newCommModel, objective={'R_Community_Growth': 1}, method="pFBA", constraints= constraints)

commpfba = sol.simulate()


print("Biomass: " + str(commpfba.get_fluxes_distribution()['R_Community_Growth']))


for r_id, rxn in newCommModel.reactions.items():
    if rxn.is_exchange:
        if commpfba.get_fluxes_distribution()[r_id] != 0:
            print('Rxn: ' + str(r_id) + " Flux: " + str(commpfba.get_fluxes_distribution()[r_id]))

print('================================================================')

comm_sol = pFBA(model)
org_fluxes = community.split_fluxes(comm_sol.values)

for x in list_models:
    name = x.id
    if name in community.organisms:
        for r_id, rxn in newCommModel.reactions.items():
            if r_id.endswith('_dra_'+ name):
                if commpfba.get_fluxes_distribution()[r_id] != 0:
                    print('Rxn: ' + str(r_id) + " Flux: " + str(commpfba.get_fluxes_distribution()[r_id]))
'''

print('===============================================')
print('=== SteadyComm ===')

steady_sol = SteadyCom(community, constraints=constraints)

print(steady_sol, '\n', steady_sol.values)

print('===============================================')
print('=== SteadyComVA ===')

steady_solva = SteadyComVA(community, obj_frac=0.5, constraints=constraints)

print(steady_solva)
