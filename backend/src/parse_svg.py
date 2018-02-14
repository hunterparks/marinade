from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

import json
import os
import re

current_directory = os.path.dirname(__file__)
base_output_file = os.path.join(current_directory, '../../src/app/components/common/simulator')

input_file = open('/Users/Alex/Downloads/pipeline_architecture.svg', 'r')

# Read the input file and set up beautifulsoup
input_text = ''
for line in input_file:
    input_text += line
soup = BeautifulSoup(input_text, "xml")

# TODO: handle multiple junctions on a single bus
# TODO: make approximations for points that are close together? rounding?


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
    typescript_file = None
    typescript_name = None
    typescript_type = None

    def __init__(self, component_type):
        self.elements = []
        if component_type == 'label':
            self.typescript_file = base_output_file + '/label/labels.model.ts'
            self.typescript_name = 'LABELS'
            self.typescript_type = 'any[]'
            self.component_type = 'label'
        elif component_type == 'mux':
            self.typescript_file = base_output_file + '/mux/muxes.model.ts'
            self.typescript_name = 'MUXES'
            self.typescript_type = 'any[]'
            self.component_type = 'mux'
        elif component_type == 'register':
            self.typescript_file = base_output_file + '/register/registers.model.ts'
            self.typescript_name = 'REGISTERS'
            self.typescript_type = 'any[]'
            self.component_type = 'register'
        elif component_type == 'bus':
            self.typescript_file = base_output_file + '/bus/buses.model.ts'
            self.typescript_name = 'BUSES'
            self.typescript_type = 'any[]'
            self.component_type = 'bus'

    def to_typescript(self):
        return json.dumps([element.to_dict() for element in self.elements], indent=2).replace('"', '\'')

    def commit(self):
        if self.typescript_name and self.typescript_type and self.typescript_file:
            print(self.component_type + ': ' + str(len(self.elements)) + ' parsed.')
            file = open(self.typescript_file, 'w')
            file.write('export const ' + self.typescript_name + ': ' + self.typescript_type + ' = ')
            file.write(self.to_typescript())
            file.write(';\n')
            return True
        return False

    def add(self, element):
        if element.__class__.__name__.lower() == self.component_type:
            if element.valid:
                self.elements.append(element)

    def __len__(self):
        return len(self.elements)

    def __unicode__(self):
        return self.to_typescript()


class Bus(Element):

    def __init__(self, junction=None, path=None):
        self.valid = True
        # if junctions:
        self.junctions = [junction]
        # if paths:
        self.paths = [path]

    def to_dict(self):
        return {
          'junctions': [junction.to_dict() for junction in self.junctions],
          'paths': [path.to_dict() for path in self.paths]
        }

    def parse_svg(self, svg):
        pass

    def validate(self, svg):
        return True

    @staticmethod
    def intersection(junction, segment):
      crossproduct = (junction.x - segment.points[0].y) * (segment.points[1].x - segment.points[0].x) - \
                     (junction.x - segment.points[0].x) * (segment.points[1].y - segment.points[0].y)
      if abs(crossproduct) > 0.01:
          return False

      dotproduct = (junction.x - segment.points[0].x) * (segment.points[1].x - segment.points[0].x) + \
                   (junction.y - segment.points[0].y) * (segment.points[1].y - segment.points[0].y)
      if dotproduct < 0:
          return False

      squaredlengthba = (segment.points[1].x - segment.points[0].x) * (segment.points[1].x - segment.points[0].x) + \
                        (segment.points[1].y - segment.points[0].y) * (segment.points[1].y - segment.points[0].y)
      if dotproduct > squaredlengthba:
          return False
      return True



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
        parent = svg.find_previous('g').attrs['transform'].replace('translate(', '').replace(')', '')
        x = float(svg.attrs['x']) + float(parent.split(',')[0])
        y = float(svg.attrs['y']) + float(parent.split(',')[1])
        size = svg.attrs['font-size']
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
        self.color, self.path = self.parse_svg(svg)

    def parse_svg(self, svg):
        color = svg.attrs['fill']
        path = str(str(svg.attrs['d']).replace('M ', '').replace(' L ', ', ').replace('Z', '').strip())
        self.validate(svg)
        return color, path

    def to_dict(self):
        return {
            'color': self.color,
            'path': self.path
        }

    def validate(self, svg):
        self.valid = True


# TODO: classify into more components, currently is just any rectangle
class Register(Element):

    def __init__(self, svg):
        self.color, self.height, self.width, self.x, self.y = self.parse_svg(svg)

    def parse_svg(self, svg):
        color = svg.attrs['fill']
        height = svg.attrs['height']
        width = svg.attrs['width']
        x = svg.attrs['x']
        y = svg.attrs['y']
        self.validate(svg)
        return color, height, width, x, y

    def to_dict(self):
        return {
            'color': self.color,
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
labels.commit()

# ====================================
# Find the registers (rectangles)
# ====================================
registers = Collection('register')
for rect in soup.find_all('rect'):
    # Get the needed register attributes
    registers.add(Register(rect))
registers.commit()

# ====================================
# Find the muxes (paths with fill)
# ====================================
muxes = Collection('mux')
for line in soup.find_all('path'):
    if line.attrs['fill'] != 'none' and line.attrs['fill'] != '#000000':
        muxes.add(Mux(line))
muxes.commit()

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
for junction in junctions: # iterate through all junctions
  for path in paths: # iterate through all paths
      junction_added = False
      path_added = False
      if Bus.intersection(junction, path): # if current path/junction pair intersects...
        for bus in buses.elements: #iterate through all existing buses
          if junction in bus.junctions: # if current junction already is part of a bus
            bus.paths.append(path)
            path_added = True
          if path in bus.paths: # or if current path is already part of a bus
            bus.junctions.append(junction)
            junction_added = True
      if not (path_added or junction_added):
        buses.add(Bus(junction, path))
buses.commit()
print(len(buses))
