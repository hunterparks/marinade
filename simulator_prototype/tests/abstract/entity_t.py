import unittest
import sys
sys.path.insert(0,'../../')
from components.abstract.entity import Entity

class Entity_t(unittest.TestCase):

    def test_Entity(self):
        "Prove Constructor fails as abstract"
        with self.assertRaises(Exception):
            test = Entity()

if __name__ == '__main__':
    unittest.main()
