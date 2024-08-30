'''
Description:  Initial.py
@Date       : 2022/10/25 16:40:46
@Author     : Tao Yang
@version    : 1.0
'''

import json
import devsim
from .model_create import *
from .physics_drift_diffusion import *

def switch_Cylindrical_coordinate(device,region):
    devsim.set_parameter(device=device, name="raxis_variable", value="x")
    devsim.set_parameter(device=device, name="raxis_zero",     value=0)
    devsim.cylindrical_node_volume(device=device, region=region)
    devsim.cylindrical_edge_couple(device=device, region=region)
    devsim.cylindrical_surface_area(device=device, region=region)
    devsim.set_parameter(name="node_volume_model",value="CylindricalNodeVolume")
    devsim.set_parameter(name="edge_couple_model",value="CylindricalEdgeCouple")
    devsim.set_parameter(name="edge_node0_volume_model",value="CylindricalEdgeNodeVolume@n0")
    devsim.set_parameter(name="edge_node1_volume_model",value="CylindricalEdgeNodeVolume@n1")
    devsim.set_parameter(name="element_edge_couple_model",value="ElementCylindricalEdgeCouple")
    devsim.set_parameter(name="element_node0_volume_model",value="ElementCylindricalNodeVolume@en0")
    devsim.set_parameter(name="element_node1_volume_model",value="ElementCylindricalNodeVolume@en1")


def InitialSolution(device, region, circuit_contacts=None, set_contact_type=None, paras=None):
    if paras["Cylindrical_coordinate"]==True:
        switch_Cylindrical_coordinate(device,region)
    else:
        pass
    # Create Potential, Potential@n0, Potential@n1
    CreateSolution(device, region, "Potential")
    
    CreateNodeModel(device, region, "InitialElectron", "abs(NetDoping)")
    CreateNodeModel(device, region, "InitialHole", "abs(NetDoping)")
    devsim.edge_from_node_model(device=device,region=region,node_model="InitialElectron")
    devsim.edge_from_node_model(device=device,region=region,node_model="InitialHole")
    CreateSiliconPotentialOnly(device, region)
    if paras["ac-weightfield"]==True:
        CreateOxidePotentialOnly(device=device, region="SiO2", update_type="default")
        for interface in devsim.get_interface_list(device=device):
            CreateSiliconOxideInterface(device=device, interface=interface)
    # Set up the contacts applying a bias
    for i in devsim.get_contact_list(device=device):
        if set_contact_type and i in set_contact_type:
            contact_type = set_contact_type[i]
        else:
            contact_type = {"type" : "Ohmic"}

        devsim.set_parameter(device=device, name=GetContactBiasName(i), value="0.0")
        #if circuit_contacts and i in circuit_contacts:
        if circuit_contacts in i :
            CreateSiliconPotentialOnlyContact(device, region, i, contact_type, True)
            if paras["ac-weightfield"]==True:
                CreateOxideContact(device=device, region="SiO2", contact=i)
        else:
            ###print "FIX THIS"
            ### it is more correct for the bias to be 0, and it looks like there is side effects
            devsim.set_parameter(device=device, name=GetContactBiasName(i), value="0.0")
            CreateSiliconPotentialOnlyContact(device, region, i, contact_type)
            if paras["ac-weightfield"]==True:
                CreateOxideContact(device=device, region="SiO2", contact=i)


def DriftDiffusionInitialSolution(device, region, irradiation_label=None, irradiation_flux=1e15, impact_label=None, circuit_contacts=None, set_contact_type=None, paras=None):
    if paras["Cylindrical_coordinate"]==True:
        switch_Cylindrical_coordinate(device,region)
    else:
        pass
    ####
    #### drift diffusion solution variables
    ####
    CreateSolution(device, region, "Electrons")
    CreateSolution(device, region, "Holes")

    ####
    #### create initial guess from dc only solution
    ####
    devsim.set_node_values(device=device, region=region, name="Electrons", init_from="IntrinsicElectrons")
    devsim.set_node_values(device=device, region=region, name="Holes",     init_from="IntrinsicHoles")
    #devsim.set_node_values(device=device, region=region, name="Electrons", init_from="InitialElectron")
    #devsim.set_node_values(device=device, region=region, name="Holes",     init_from="InitialHole")

    ###
    ### Set up equations
    ###
    
    CreateSiliconDriftDiffusion(device, region, irradiation_label=irradiation_label, irradiation_flux=irradiation_flux, impact_label=impact_label)
    for i in devsim.get_contact_list(device=device):
        if set_contact_type and i in set_contact_type:
            contact_type = set_contact_type[i]
        else:
            contact_type = {"type" : "Ohmic"}

        if circuit_contacts in i:
            devsim.set_parameter(device=device, name=GetContactBiasName(i), value="0.0")
            CreateSiliconDriftDiffusionAtContact(device, region, i, contact_type, True)
        else:
            devsim.set_parameter(device=device, name=GetContactBiasName(i), value="0.0")
            CreateSiliconDriftDiffusionAtContact(device, region, i, contact_type)

