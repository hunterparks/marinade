from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

import json
import os
import re

current_directory = os.path.dirname(__file__)
input_file = open('/Users/alex/Downloads/pipeline_architecture (7).svg', 'r')
output_file = os.path.join(current_directory, '../../src/app/models/simulator/simulator.model.ts')

# Clear the contents of the file
open(output_file, 'w').write('export const ARCHITECTURE: any = {\n')

# Read the input file and set up beautifulsoup
input_text = ''
for line in input_file:
    input_text += line
soup = BeautifulSoup(input_text, "xml")


class Element(ABC):

    @abstractmethod
    def parse_svg(self, svg):
        pass

    @abstractmethod
    def to_dict(self):
        pass

    @abstractmethod
    def validate(self, svg):
        return False


class Collection:
    component_type = None
    typescript_type = None

    def __init__(self, component_type):
        self.elements = []
        if component_type == 'bus':
            self.typescript_type = 'any[]'
            self.component_type = 'bus'
        elif component_type == 'controller':
            self.typescript_type = 'any[]'
            self.component_type = 'controller'
        elif component_type == 'label':
            self.typescript_type = 'any[]'
            self.component_type = 'label'
        elif component_type == 'mux':
            self.typescript_type = 'any[]'
            self.component_type = 'mux'
        elif component_type == 'stage':
            self.typescript_type = 'any[]'
            self.component_type = 'stage'
        elif component_type == 'stage-register':
            self.typescript_type = 'any[]'
            self.component_type = 'stage-register'

    def to_typescript(self):
        return json.dumps([element.to_dict() for element in self.elements], indent=2).replace('"', '\'')

    def commit(self):
        if self.typescript_type:
            print(self.component_type + ': ' + str(len(self.elements)) + ' parsed.')
            file = open(output_file, 'a')
            file.write('\'' + self.component_type + '\': ')
            file.write(self.to_typescript())
            file.write(',\n')
            file.close()
            return True
        return False

    def add(self, element):
        if element.__class__.__name__.lower() == self.component_type or (element.__class__.__name__.lower() == 'register' and self.component_type in ['stage', 'stage-register', 'controller']):
            if element.valid:
                self.elements.append(element)

    def __len__(self):
        return len(self.elements)

    def __unicode__(self):
        return self.to_typescript()


class Bus(Element):

    name = ''
    width = 1

    def __init__(self, junction=None, path=None):
        self.valid = True
        if junction:
            self.junctions = [junction]
        else:
            self.junctions = []
        if paths:
            self.paths = [path]
        else:
            self.paths = []

    def to_dict(self):
        return {
          'junctions': [junction.to_dict() for junction in self.junctions],
          'name': self.name,
          'paths': [path.to_dict() for path in self.paths],
          'width': self.width
        }

    def parse_svg(self, svg):
        pass

    def validate(self, svg):
        return True

    @staticmethod
    def intersection(junction, path):
        for i in range(len(path.points)-1):
            if abs(path.points[i].y - path.points[i+1].y) < 5:  # horizontal line with 4 pixel tolerance
                if abs(path.points[i].y - junction.y) < 5:  # same vertical level with 4 pixel tolerance
                    if path.points[i].x > path.points[i+1].x:  # right to left
                        if junction.x < path.points[i].x and junction.x > path.points[i+1].x:
                            return True
                    elif path.points[i].x < path.points[i+1].x:  # left to right
                        if junction.x < path.points[i+1].x and junction.x > path.points[i].x:
                            return True
            elif abs(path.points[i].x - path.points[i+1].x) < 5:  # vertical line with 4 pixel tolerance
                if abs(path.points[i].x - junction.x) < 5:  # same horizontal level with 4 pixel tolerance
                    if path.points[i].y > path.points[i+1].y:  # down to up
                        if junction.y < path.points[i].y and junction.y > path.points[i+1].y:
                            return True
                    elif path.points[i].y < path.points[i+1].y:  # up to down
                        if junction.y < path.points[i+1].y and junction.y > path.points[i].y:
                            return True
            # check at points
            if path.points[i].y < (junction.y + 5) and path.points[i].y > (junction.y - 5) \
               and path.points[i].x < (junction.x + 5) and path.points[i].x > (junction.x - 5):
                return True
        return False


class Point(Element):

    def __init__(self, svg):
        self.x, self.y = self.parse_svg(svg)

    def parse_svg(self, svg):
        self.validate(svg)
        return [float(x) for x in svg.split(' ')]

    def to_dict(self):
        return {
            'x': self.x,
            'y': self.y
        }

    def validate(self, svg):
        self.valid = True


class Junction(Point):

    def __eq__(self, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return self.x == other.x and self.y == other.y
        return False

    def parse_svg(self, svg):
        self.validate(svg)
        return float(svg.attrs['cx']), float(svg.attrs['cy'])

    def validate(self, svg):
        self.valid = svg.attrs['rx'] == svg.attrs['ry']


class Path(Element):

    def __init__(self, svg):
        self.points = self.parse_svg(svg)

    def __eq__(self, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return self.to_dict() == other.to_dict()
        return False

    def parse_svg(self, svg):
        points = []
        svg_str = str(str(svg.attrs['d']).replace('M ', '').replace(' L ', ', ').replace('Z', '').strip())
        for point in svg_str.split(', '):
            points.append(Point(point))
        self.validate(svg)
        return points

    def to_dict(self):
        return ', '.join(str(point.x) + ' ' + str(point.y) for point in self.points)

    def validate(self, svg):
        return True


class Label(Element):

    def __init__(self, svg):
        self.size, self.text, self.x, self.y = self.parse_svg(svg)

    def parse_svg(self, svg):
        x = float(svg.attrs['x'])
        y = float(svg.attrs['y'])
        size = 6
        self.validate(svg)
        if self.valid:
            return size, svg.get_text(), x, y
        return -1, '', -1, -1

    def to_dict(self):
        return {
            'size': self.size,
            'text': self.text,
            'x': self.x,
            'y': self.y,
        }

    def validate(self, svg):
        self.valid = re.sub(r'\s+', ' ', svg.get_text()).strip() != '[Not supported by viewer]'


class Mux(Element):

    def __init__(self, svg):
        self.path = self.parse_svg(svg)

    def parse_svg(self, svg):
        path = str(str(svg.attrs['d']).replace('M ', '').replace(' L ', ', ').replace('Z', '').strip())
        self.validate(svg)
        return path

    def to_dict(self):
        return {
            'path': self.path
        }

    def validate(self, svg):
        self.valid = True


class Register(Element):

    def __init__(self, svg):
        self.type, self.height, self.width, self.x, self.y = self.parse_svg(svg)

    def parse_svg(self, svg):
        color = svg.attrs['fill'].lower()
        if color == '#ff3333':
          self.type = 'stage'
        elif color == '#97d077':
          self.type = 'stage-register'
        elif color == '#ffff33':
          self.type = 'controller'
        height = svg.attrs['height']
        width = svg.attrs['width']
        x = svg.attrs['x']
        y = svg.attrs['y']
        self.validate(svg)
        return self.type, height, width, x, y

    def to_dict(self):
        return {
            'height': self.height,
            'width': self.width,
            'x': self.x,
            'y': self.y
        }

    def validate(self, svg):
        self.valid = True


# ====================================
# Find the bus text
# ====================================
labels = Collection('label')
for label in soup.find_all('text'):
    labels.add(Label(label))

junctions = []
for junction in soup.find_all('ellipse'):
    junctions.append(Junction(junction))
paths = []
for line in soup.find_all('path'):
    if line.attrs['fill'] == 'none':
        paths.append(Path(line))

buses = Collection('bus')
count = 0
print(len(junctions), len(paths))

# associate path branches and junctions
for path in paths:
    path_has_junction = False
    for junction in junctions:
        if Bus.intersection(junction, path):
            path_has_junction = True
            create_bus = True  # max one bus should be created for path/junction pair
            for bus in buses.elements:
                if path in bus.paths and junction in bus.junctions:  # not sure if necessary? path/junction pairs only appear once, shouldn't already be together
                    create_bus = False
                elif path in bus.paths:
                    bus.junctions.append(junction)  # junction not accounted for, add it
                    create_bus = False
                elif junction in bus.junctions:
                    bus.paths.append(path)  # path not accounted for, add it
                    create_bus = False
                else:
                    pass  # this can be taken out, just for reading clarity
            if create_bus:
                buses.add(Bus(junction, path))
    if not path_has_junction:
        buses.add(Bus([], path))

# transfer path labels to bus labels (EACH BUS SHOULD HAVE ONE)
# TODO
# iterate through labels
for label in labels.elements:
    # iterate through buses
    for bus in buses.elements:
        bus_named = False
        # iterate through paths in bus
        for path in bus.paths:
            # does path have a label associated with it?
            if abs(path.points[0].y - path.points[1].y) < 15: # path is horizontal, most likely comes from a component
                if label.x > path.points[0].x-15 and label.x < path.points[1].x+15 and path.points[0].y > (label.y-10) and path.points[0].y - label.y < 25:
                    # associate label to bus, remove association from path
                    bus_parts = label.text.replace(']', '').split('[')
                    if len(bus_parts) > 1:
                      bus_width_parts = bus_parts[1].split('..')
                      bus.width = int(bus_width_parts[0]) - int(bus_width_parts[1]) + 1
                    bus.name = label.text.replace(']', '').split('[')[0]
                    bus_named = True
            if bus_named:
                break
                    # break loop
            # else do nothing

# ====================================
# Find the muxes (paths with fill)
# ====================================
muxes = Collection('mux')
for line in soup.find_all('path'):
    if line.attrs['fill'] != 'none' and line.attrs['fill'] != '#000000':
        muxes.add(Mux(line))

# ====================================
# Find the registers (rectangles)
# ====================================
registers = {
  'stage': Collection('stage'),
  'stage-register': Collection('stage-register'),
  'controller': Collection('controller')
}
for rect in soup.find_all('rect'):
    typed_rect = Register(rect)
    registers[typed_rect.type].add(typed_rect)

buses.commit()
registers['controller'].commit()
muxes.commit()
registers['stage'].commit()
registers['stage-register'].commit()

file = open(output_file, 'a')
file.write('};\n')
