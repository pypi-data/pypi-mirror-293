import pytest
from carg_io.abstracts import Parameter, ParameterSet, units, NaN
from carg_io.spaces import Space
import numpy as np

__author__ = "eelco van Vliet"
__copyright__ = "eelco van Vliet"
__license__ = "MIT"


def test_space():
    class Box(ParameterSet):
        Length:Parameter = 1 * units.meter
        Width:Parameter = 1* units.meter
        Height:Parameter = 1* units.meter

        @property
        def Volume(self) -> Parameter:
            l = self.Length['m']
            w = self.Width['m']
            h = self.Height['m']
            return Parameter('Volume', l*w*h*units.meter**3)

    
    space = Space(Box)
    space.expand(Box.Length, 'm', np.linspace(1,10,10))
    space.expand(Box.Width, 'm', np.linspace(1,10,10))
    space.expand(Box.Height, 'm', np.linspace(1,10,10))

    space.add_criteria("Volume", 'm**3', lambda v: v < 10*10*9)

    # There should be four cases that will not pass this criteria:
    # everything 10 m, or any combination of two parameters being 10 m.
    # = 4 cases


    assert len(space) == 10**3-4
    


