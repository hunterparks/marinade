from bs4 import BeautifulSoup
import json
import os
dir = os.path.dirname(__file__)
base_output_file = os.path.join(dir, '../../src/app/components/common/simulator')

input_file = open('/Users/Alex/Downloads/pipeline_architecture.svg', 'r')
bus_model_file = open(base_output_file + '/bus/buses.model.ts', 'w')
register_model_file = open(base_output_file + '/register/registers.model.ts', 'w')
mux_model_file = open(base_output_file + '/mux/muxes.model.ts', 'w')

# Read the input file and set up beautifulsoup
text = ''
for line in input_file:
  text += line
soup = BeautifulSoup(text, "xml")

# TODO: handle multiple junctions on a single bus
# TODO: make approximations for points that are close together? rounding?
# TODO: clean up duplicates more reliably

# ====================================
# Find the bus junctions (ellipses)
# ====================================
ellipses = soup.find_all('ellipse')
junctions = []
for ellipse in ellipses:
  if ellipse.attrs['rx'] == ellipse.attrs['ry']:
    junctions.append({
      'x': ellipse.attrs['cx'],
      'y': ellipse.attrs['cy'],
    })
# Remove duplicates
junctions = [dict(t) for t in set([tuple(d.items()) for d in junctions])]

# ====================================
# Find the buses (paths without fill)
# ====================================
paths = []
complex_buses = dict()
for line in soup.find_all('path'):
  # Skip the paths with a fill - buses don't have fill
  if line.attrs['fill'] == 'none':
    # Remove the SVG-specific code, create coordinate pairs
    new_line = str(str(line.attrs['d']).replace('M ', '').replace(' L ', ', ').replace('Z', '').strip())
    points = []
    for pair in new_line.split(', '):
      points.append([float(point) for point in pair.split()])
    for i in range(len(points) - 1):
      current = {
        'x': points[i][0],
        'y': points[i][1]
      }
      next = {
        'x': points[i + 1][0],
        'y': points[i + 1][1]
      }
      complex_bus = False
      for junction in junctions:
        crossproduct = (float(junction['y']) - current['y']) * (next['x'] - current['x']) - (float(junction['x']) - current['x']) * (next['y'] - current['y'])
        if abs(crossproduct) > 0.01: continue  # (or != 0 if using integers)

        dotproduct = (float(junction['x']) - current['x']) * (next['x'] - current['x']) + (float(junction['y']) - current['y']) * (next['y'] - current['y'])
        if dotproduct < 0: continue

        squaredlengthba = (next['x'] - current['x']) * (next['x'] - current['x']) + (next['y'] - current['y']) * (next['y'] - current['y'])
        if dotproduct > squaredlengthba: continue
        if complex_buses.get(str(junction), None):
          if new_line not in complex_buses.get(str(junction)):
            complex_buses[str(junction)].append(new_line)
            complex_bus = True
        else:
          complex_buses[str(junction)] = [new_line]
          complex_bus = True
      if not complex_bus:
        paths.append(new_line)
# Remove duplicates
paths = list(set(paths))
paths = [{'paths': [path]} for path in paths]
# Reformat complex buses
for key, value in complex_buses.items():
  paths.append({
    'junction': json.loads(key.replace('\'', '"')),
    'paths': value
  })
# Print the number found
print(str(len(paths)) + ' buses parsed.')
# Write the results to the bus model file
# TODO: write all to a single configuration file
bus_model_file.write('export const BUSES: any[] = ')
bus_model_file.write(json.dumps(paths, indent=2).replace('"', '\''))
bus_model_file.write(';\n')

# ====================================
# Find the registers (rectangles)
# ====================================
rects = soup.find_all('rect')
registers = []
for rect in rects:
  # Get the needed register attributes
  registers.append({
    'color': rect.attrs['fill'],
    'height': rect.attrs['height'],
    'width': rect.attrs['width'],
    'x': rect.attrs['x'],
    'y': rect.attrs['y']
  })
# Remove duplicates
registers = [dict(t) for t in set([tuple(d.items()) for d in registers])]
# Print the number found
print(str(len(registers)) + ' registers parsed.')
# Write the results to the register model file
# TODO: write all to a single configuration file
register_model_file.write('export const REGISTERS: any[] = ')
register_model_file.write(json.dumps(registers, indent=2).replace('"', '\''))
register_model_file.write(';\n')

# ====================================
# Find the muxes (paths with fill)
# ====================================
paths = []
muxes = []
for line in soup.find_all('path'):
  if line.attrs['fill'] != 'none' and line.attrs['fill'] != '#000000':
    new_line = str(str(line.attrs['d']).replace('M ', '').replace(' L ', ', ').replace('Z', '').strip())
    # Get the needed mux attributes
    muxes.append({
      'color': line.attrs['fill'],
      'path': new_line
    })
# Remove duplicates
muxes = [dict(t) for t in set([tuple(d.items()) for d in muxes])]
# Print the number found
print(str(len(muxes)) + ' muxes parsed.')
# Write the results to the mux model file
# TODO: write all to a single configuration file
mux_model_file.write('export const MUXES: any[] = ')
mux_model_file.write(json.dumps(muxes, indent=2).replace('"', '\''))
mux_model_file.write(';\n')
