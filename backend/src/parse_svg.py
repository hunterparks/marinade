from bs4 import BeautifulSoup
import json
import os
dir = os.path.dirname(__file__)
base_output_file = os.path.join(dir, '../../src/app/components/common/simulator')

input_file = open('/Users/Alex/Downloads/pipeline_architecture.svg', 'r')
bus_model_file = open(base_output_file + '/bus/buses.model.ts', 'w')
register_model_file = open(base_output_file + '/register/registers.model.ts', 'w')

text = ''
for line in input_file:
  text += line

soup = BeautifulSoup(text, "xml")
groups = soup.find('g').find_all('g')
paths = []
for group in groups:
  for line in soup.find('g').find_all('path'):
    if line.attrs['fill'] == 'none':
      new_line = str(str(line.attrs['d']).replace('M ', '').replace(' L ', ', ').replace('Z', '').strip())
      paths.append(new_line)
print(str(len(paths)) + ' buses parsed.')
bus_model_file.write('export const BUSES: string[] = ')
bus_model_file.write(json.dumps(paths, indent=2).replace('"', '\''))
bus_model_file.write(';\n')

rects = soup.find('g').find_all('rect')
registers = []
for rect in rects:
  registers.append({
    'color': rect.attrs['fill'],
    'height': rect.attrs['height'],
    'width': rect.attrs['width'],
    'x': rect.attrs['x'],
    'y': rect.attrs['y']
  })
print(str(len(registers)) + ' registers parsed.')
register_model_file.write('export const REGISTERS: any[] = ')
register_model_file.write(json.dumps(registers, indent=2).replace('"', '\''))
register_model_file.write(';\n')
