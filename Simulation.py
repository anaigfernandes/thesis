#IMPORT MODEL
# using REFRAMED
#from reframed.io.sbml import load_cbmodel
#pd = load_cbmodel('testPD.xml', exchange_detection = 'EX')

# using COBRApy
from cobra.io import read_sbml_model
model_pd = read_sbml_model('2405t.xml')

# build a phenotype simulator
from mewpy.simulation import get_simulator

import cobra

#Reactions
number_reactions = len(model_pd.reactions)
reactions_list = []
for i in range(1, 80):
    reactions_model = model_pd.groups.get_by_id("g%d" %(i)).members

    for reac in reactions_model:
        if str(reac.id) not in reactions_list:
            reactions_list.append(str(reac.id))


#DRAINS
#Close all drains
drains = model_pd.groups.get_by_id("g1").members

for reac in drains:
    reac.bounds = (0 , 1000)
    print(reac.name, reac.bounds)

#Define environment
envcond_pd = {'EX_C00864__dra' : (-1000,1000),
    'EX_C00009__dra' : (-1000,1000),
    'EX_C14818__dra' : (-1000,1000),
    'EX_C14819__dra' : (-1000,1000),
    'EX_C00253__dra' : (-1000,1000),
    'EX_C00135__dra' : (-0.2,1000),
    'EX_C00031__dra' : (-1.9,1000),
    'EX_C00120__dra' : (-1000,1000),
    'EX_C00078__dra' : (-0.2,1000),
    'EX_C00073__dra' : (-0.2,1000),
    #'EX_C00007__dra' : (-1000,1000),
    'EX_C00025__dra' : (-0.2,1000),
    'EX_C00037__dra' : (-0.2,1000),
    'EX_C00041__dra' : (-0.2,1000),
    'EX_C00047__dra' : (-0.2,1000),
    'EX_C00049__dra' : (-0.2,1000),
    'EX_C00062__dra' : (-0.2,1000),
    'EX_C00065__dra' : (-0.2,1000),
    'EX_C00079__dra' : (-0.2,1000),
    'EX_C00082__dra' : (-0.2,1000),
    'EX_C00106__dra' : (-1000,1000),
    'EX_C00123__dra' : (-0.2,1000),
    'EX_C00147__dra' : (-1000,1000),
    'EX_C00148__dra' : (-0.2,1000),
    'EX_C00178__dra' : (-1000,1000),
    'EX_C00183__dra' : (-0.2,1000),
    'EX_C00188__dra' : (-0.2,1000),
    'EX_C00242__dra' : (-1000,1000),
    'EX_C00385__dra' : (-1000,1000),
    'EX_C00407__dra' : (-0.2,1000),
    'EX_C03479__dra' : (-1000,1000),
    'EX_C00255__dra' : (-1000,1000),
    'EX_C00283__dra' : (-1000,1000),
    'EX_C00097__dra' : (-0.2,1000),
    'EX_C00314__dra' : (-1000,1000)}

#new_key = 'EX_C00124__cytop' #D-Galactose
#new_key = 'EX_C00185__cytop' #Cellobiose
#new_key = 'EX_C00095__cytop' #Fructose
#new_key = 'EX_C00159__cytop' #Mannose
#new_key = 'EX_C00089__cytop' #Sucrose
#new_key = 'EX_C01083__cytop' #Trehalose


#NO GROWTH MEDIA

#new_key = 'EX_C00243__cytop' #Lactose
#new_key = 'EX_C00507__cytop' #Rhamnose
#new_key = 'EX_C00121__cytop' #Ribose
#new_key = 'EX_C00181__cytop' #Xylose
#new_key = 'EX_C00721__cytop' #Dextrin
#new_key = 'EX_C00369__cytop' #Starch
#new_key = 'EX_C00116__cytop' #Glycerol

#NGAM
constraints_pd = {'R00086__cytop' : (0.6, 0.6)}

#Simulator
simul = get_simulator(model_pd, envcond = envcond_pd, constraints = constraints_pd)

import pandas as pd

#Verify drains

open_drains = 0
dic_drains = {}
c = 0
for reac in drains:
    c += 1
    bounds = simul.get_reaction_bounds(reac.id)
    dic_drains[str(reac.name)]= simul.get_reaction_bounds(reac.id)
    if bounds[0] != 0.0:
        open_drains += 1
close_drains= len(drains) - open_drains
if open_drains == 0:
    print('The drains are all closed')
else: print('ATTENTION: There are %d open drains and %d close drains' %(open_drains,close_drains))

x = pd.DataFrame.from_dict(dic_drains, orient='index', columns=['LB', 'UB'])


dic_drains_bounds = {}

for reac in drains:
    bounds = simul.get_reaction_bounds(reac.id)
    if bounds[0] != 0.0:
        dic_drains_bounds[str(reac.name)] = simul.get_reaction_bounds(reac.id)

y = pd.DataFrame.from_dict(dic_drains_bounds, orient='index', columns=['LB', 'UB'])
y

simul.objective = 'e_Biomass__cytop'
result = simul.simulate(method='pFBA')

#REACTIONS FLUXES
dic_reactions = {}
for i in range(1, len(model_pd.groups) + 1):
    reactions_in_pathway = model_pd.groups.get_by_id("g%d" % (i)).members

    for reac in reactions_in_pathway:
        if result.fluxes[str(reac.id)] != 0:
            z = str(reac.id) + ': ' + str(reac.name)
            dic_reactions[z] = result.fluxes[str(reac.id)]

fluxes = pd.DataFrame.from_dict(dic_reactions, orient='index', columns=['Flux'])

if not bool(dic_reactions): print('NO REACTION HAS FLUX')

#UPTAKE and EXPORT METABOLITES
import pandas as pd
from IPython.display import display_html
from itertools import chain,cycle


dic_upt = {}
dic_exp = {}

for reac in drains:
    if result.fluxes[str(reac.id)] < 0:
        dic_upt[str(reac.name)]= result.fluxes[str(reac.id)]
    if result.fluxes[str(reac.id)] > 0:
        dic_exp[str(reac.name)]= result.fluxes[str(reac.id)]

uptake = pd.DataFrame.from_dict(dic_upt, orient='index', columns=['Flux'])
export = pd.DataFrame.from_dict(dic_exp, orient='index', columns=['Flux'])



print(number_reactions)
print(reactions_list)
print(envcond_pd)
print(constraints_pd)
print(x)
print(y)
print('Biomass: ', result.fluxes["e_Biomass__cytop"])
print('ATP maint.: ', result.fluxes["R00086__cytop"])
print('Reactions fluxes: \n', fluxes)
print('Uptake metabolites: \n', uptake)
print('Export metabolites: \n', export)
