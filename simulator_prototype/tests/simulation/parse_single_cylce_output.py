import tablib
import json

data = tablib.Dataset()
#data.headers = ['clk','rst','const8','const4','const14','pmd','pmwr','pc','pc8','pc4','instr','instr_23_0','instr_19_16',
#                'instr_3_0','instr_15_12','instr_11_8','instr_31_28','instr_27_26','instr_25_20','instr_4_4','imm32','ra1',
#                'ra2','ra3','rwd','rd1','rd2','alub','branch','aluf','aluc','aluv','alun','aluz','aluflag','flag','c','v',
#                'n','z','memrd','wdb','pcwb','pcwr','regsa','regdst','regwrs','wdbs','regwr','exts','alu8rcb','alus',
#                'aluflagwr','memwr','regsrc','pcsrc'
#               ]

data.headers = [
    'clk',
    'rst',
    'wdb',
    'pc4',
    'branch',
    'instr',
    'pcsrc',
    'pcwr',
    'regsa',
    'regdst',
    'regwrs',
    'regwr',
    'exts',
    'alus',
    'aluflagwr',
    'memwr',
    'regsrc',
    'wdbs',
    'imm32',
    'rd1',
    'rd2',
]

with open('single_cycle_data_output.txt', mode='r') as input_json_file:
    input_dict = json.loads(input_json_file.read())

    for step in input_dict["Run"]:
        data.append(['0x{:X}'.format(step[x]["state"]) for x in data.headers])

#print(data.dict)
data = data.transpose()

with open('results/parsed_sco.xls', 'wb') as f:
    f.write(data.xls)
