#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


units = pd.read_excel('stx_fleet.xlsx', sheet_name='units')
inspection = pd.read_excel('stx_fleet.xlsx', sheet_name='inspection')
supervisor = pd.read_excel('stx_fleet.xlsx', sheet_name='super')


# In[3]:


units = units[['Unit_Num', 'tblEnterprise::make', 'tblEnterprise::model', 'tblEnterprise::year', 'First_Name_1', 'Last_Name_1', 'Mobile', 'Mobile_strip', 'Office Email',]]


# In[4]:


supervisor = supervisor[['EmailAddress','Supervisor',]]


# In[5]:


inspection = inspection[[
    ##### Base Information
    'Unit #',
    'Completed by',
    'Registration Expiration Date',
    'Current Mileage',
    ###### Upkeep and Maintenance
    'I track oil changes by:',
    'Oil Change - Percentage (%)',
    'Next Oil Change Due @ (Enter Miles)',
#     'Brake Function (Fluid, Pads, Squeaking...etc.)',
#     'Coolant * IF ENGINE IS COOL*',
#     'Washer Fluid Level',
#     'Lights',
#     'Tires - Condition',
    'Tire - Estimated Tread Depth',
#     'Lug Nuts',
#     'House Keeping - Exterior',
#     'House Keeping (Interior)',
#     'Body',    
    'Windshield - Front (Not cracked or chipped - CLEAR VIEW)',
    'Other Windows (other than Front - Windshield)',
    'Mirrors',
    'Final Comments/Upkeep & Maintenance',
    
    ##### Truck Safety
    'First-Aid Kit',
    'Blood Born Pathogen Kit',
    'H2S Monitor Time Remaining',
    'Fire Extinguisher - Present',
    'Fire Extinguisher - Annual Inspection',
    'Fire Extinguisher - Expiration Date',
    'Fire Extinguisher - Serial # - Present & Visible',  
    'Fire Extinguisher - Serial #',
    'Fire Extinguisher - Monthly Tag Punch Present',
    'Fire Extinguisher - Nozzle Free & Clear',
    'Fire Extinguisher - Charged',
    'Fire Extinguisher - Pin Intact',
    'Cooler',
    'Lock Out/Tag Out - LOTO',
    
    ##### Truck Communication
    '2 Way Radio - Present in Unit',
    '2 Way Radio/Handheld - Functioning/Working',
    'Radio - Turns On with Ignition',
    'Radio - GPS - Visible in SCADA Control Room',
    'Radio - Equipment Intact - Base/Antenna',
    'Hand Held Radio - Installed/Functional',
    'Sirius/XM Radio - Is your radio functioning?',
    'Final Comments - Safety Equipment',
]]


# In[6]:


inspection.columns = inspection.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
        


# In[7]:


# for c in inspection:
#     print(c)


# In[10]:


inspection.columns = [
    # Truck base information
    'unit',
    'completed_by',
    'reg_exp_date',
    'current_mileage',
    # Truck Upkeep and Maintenance
    'oil_track_by',
    'oil_percentage',
    'oil_miles',
    'tire_tread',
    'windshiel',
    'other_windows',
    'mirrors',
    'comments_upkeep_maintenance',
    # Truck Safety
    'first_aid_kit',
    'blood_born_pathogen_kit',
    'h2s_monitor_expired',
    'f_ext_present',
    'f_ext_annual_inspection',
    'f_ext_expiration_date',
    'f_ext_serial_visible',
    'f_ext_serial',
    'f_ext_monthly_tag_punch',
    'f_ext_nozzle_free_and_clear',
    'f_ext_charged',
    'f_ext_pin_intact',
    'cooler',
    'loto',
    # Truck Communication
    'radio_ok',
    'handheld_ok',
    'radio_auto_on',
    'radio_gps',
    'radio_parts_ok',
    'hand_held_ok',
    'sirius_ok',
    # Comments for Safety and Communication
    'comments_safety_equipment',
]


# In[11]:


groupby_unit = {}
for i in inspection.index:
    unit = inspection['unit'][i] 
    groupby_unit[unit] = {
        # Truck Base Information
        'unit':inspection['unit'][i],
        'completed_by':inspection['completed_by'][i],
        'reg_exp_date':inspection['reg_exp_date'][i],
        'current_mileage':inspection['current_mileage'][i],
        # Truck Upkeep and Maintenance
        'oil_track_by':inspection['oil_track_by'][i],
        'oil_percentage':inspection['oil_percentage'][i],
        'oil_miles':inspection['oil_miles'][i],
        'tire_tread':inspection['tire_tread'][i],
        'windshiel':inspection['windshiel'][i],
        'other_windows':inspection['other_windows'][i],
        'mirror':inspection['mirrors'][i],
        'comments_upkeep_maintenance':inspection['comments_upkeep_maintenance'][i],
        # Truck Safety
        'first_aid_kit':inspection['first_aid_kit'][i],
        'blood_born_pathogen_kit':inspection['blood_born_pathogen_kit'][i],
        'h2s_monitor_expired':inspection['h2s_monitor_expired'][i],
        'f_ext_present':inspection['f_ext_present'][i],
        'f_ext_annual_inspection':inspection['f_ext_annual_inspection'][i],
        'f_ext_expiration_date':inspection['f_ext_expiration_date'][i],
        'f_ext_serial_visible':inspection['f_ext_serial_visible'][i],
        'f_ext_serial':inspection['f_ext_serial'][i],
        'f_ext_monthly_tag_punch':inspection['f_ext_monthly_tag_punch'][i],
        'f_ext_nozzle_free_and_clear':inspection['f_ext_nozzle_free_and_clear'][i],
        'f_ext_charged':inspection['f_ext_charged'][i],
        'f_ext_pin_intact':inspection['f_ext_pin_intact'][i],
        'cooler':inspection['cooler'][i],
        'loto':inspection['loto'][i],
        # Truck Communication
        'radio_ok':inspection['radio_ok'][i],
        'handheld_ok':inspection['handheld_ok'][i],
        'radio_auto_on':inspection['radio_auto_on'][i],
        'radio_gps':inspection['radio_gps'][i],
        'radio_parts_ok':inspection['radio_parts_ok'][i],
        'hand_held_ok':inspection['hand_held_ok'][i],
        'sirius_ok':inspection['sirius_ok'][i],
        # Comments for Safety and Communication
        'comments_safety_equipment':inspection['comments_safety_equipment'][i],
    }


# In[36]:


x=0
for k, v in groupby_unit.items():
    if x <= 10:
        # Truck Base Information
        print('-----Unit: ',k)
        print('Completed by: ', v['completed_by'])
        print('---Truck Base Information')
        if (v['reg_exp_date'][-2:]) == str(21):
            print('Registration Exp Date: ', v['reg_exp_date'])
        print('Odometer: ', v['current_mileage'])
        # Truck Upkeep and Maintenance
        print('---Truck Upkeep and Maintenance')
        if str(v['oil_percentage']) != 'nan':
            print('Oil Change - Oil life: ' + str(v['oil_percentage']) + '%')
        if str(v['oil_miles']) != 'nan':
            print('Oil Change - Next at: ' + str(v['oil_miles']) + ' miles')
        if v['tire_tread'] == '< 6/32':
            print('Needs tire inspection, thread at: ', v['tire_tread'])
        if v['windshiel'] != 'Pass':
            print('Winshield needs inspection')
        if v['other_windows'] != 'Pass':
            print('Windows needs inspection')
        if v['mirror'] != 'Pass':
            print('Mirrors need inspection: ', v['mirror'])
        if str(v['comments_upkeep_maintenance']) != 'nan':
            print('- Driver comments: ')
            print('    ',v['comments_upkeep_maintenance'])
        # Truck Safety
        print('---Truck Safety')
        if v['first_aid_kit'] == 'Fail':
            print('First Aid Kit Needed: ', v['first_aid_kit'])
        if v['blood_born_pathogen_kit'] == 'Fail':
            print('Blood Born Pathogen Kit needs replacement: ', v['blood_born_pathogen_kitor'])
        if v['h2s_monitor_expired'] == 'Fail':
            print('H2S Monitor needs replacement: ', v['h2s_monitor_expired'])
        if v['f_ext_present'] == 'Fail':
            print('Unit needs fire extinguisher: ', v['f_ext_present'])
        if v['f_ext_annual_inspection'] == 'Fail':
            print('Fire extinguisher needs anual inspection: ', v['f_ext_annual_inspection'])
        if v['f_ext_expiration_date'] == 'Fail':
            print('Fire extinguisher expiration date: ', v['f_ext_expiration_date'])
        if v['f_ext_serial_visible'] == 'Fail':
            print('Fire extinguisher serial not visible: ', v['f_ext_serial_visible'])
            print('Current fire extinguisher serial: ', v['f_ext_serial'])
        if v['f_ext_monthly_tag_punch'] == 'Fail':
            print('Fire Extinguisher needs monthly punch tag: ', v['f_ext_monthly_tag_punch'])
        if v['f_ext_nozzle_free_and_clear'] == 'Fail':
            print('Fire Extinguisher needs to be relocated: ', v['f_ext_nozzle_free_and_clear'])
        if v['f_ext_charged'] == 'Fail':
            print('Fire Extinguisher needs to be charged: ', v['f_ext_charged'])
        if v['f_ext_pin_intact'] == 'Fail':
            print('Pin needs to be replaced: ', v['f_ext_pin_intact'])
        if v['cooler'] == 'Fail':
            print('Needs cooler: ', v['cooler'])
        if v['loto'] == 'Fail':
            print('Needs LOTO restock: ', v['loto'])
        # Truck Communications
        print('---Truck Communications')
        if str(v['radio_ok']) != 'Pass':
            print('Radio not install in unit: ', v['radio_ok'])
        if (str(v['handheld_ok']) != 'Pass' and str(v['handheld_ok']) != 'nan'):
            print('Handheld radio not present: ', v['handheld_ok'])
        if (str(v['radio_auto_on']) != 'Pass' and str(v['radio_auto_on']) != 'nan'):
            print('Radio without Auto-ON/OFF by ignition: ', v['radio_auto_on'])
        if (str(v['radio_gps']) != 'Pass' and str(v['radio_gps']) != 'nan'):
            print('Radio GPS needs troubleshoot: ', v['radio_gps'])
        if (str(v['radio_parts_ok']) != 'Pass' and str(v['radio_parts_ok']) != 'nan'):
            print('Radio Comms needs inspection: ', v['radio_parts_ok'])
        if str(v['hand_held_ok']) != 'Pass':
            print('Handheld radio not working: ', v['hand_held_ok'])
        if str(v['sirius_ok']) != 'Pass':
            print('XM radio not working: ', v['sirius_ok'])
        # Comments for Safety and Communication
        if (str(v['comments_safety_equipment']) != 'Pass' and str(v['comments_safety_equipment']) != 'nan'):
            print('- Driver comments for safety and communication: ')
            print('    ', v['comments_safety_equipment'])
        print('')
        x += 1
    
    


# In[ ]:




