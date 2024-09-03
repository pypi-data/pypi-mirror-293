"""
File Purpose: Fluid, FluidList, FluidDimension, FluidHaver, jFluidDimension, jFluidHaver, FluidsHaver
"""
import xarray as xr

from .dimension_tools import (
    DimensionValue, DimensionValueList,
    DimensionValueSetter,
    Dimension, DimensionHaver,
)
from ..errors import FluidKeyError, FluidValueError
from ..tools import (
    alias, elementwise_property,
    xarray_rename,
    UNSET,
    Sentinel,
)
from ..defaults import DEFAULTS


''' --------------------- Fluid & FluidList --------------------- '''

class Fluid(DimensionValue):
    '''fluid... unchanging properties of the fluid.

    name: the name (str) of the fluid. if None, cannot convert to str.
    i: the index (int) of the fluid (within a FluidList). if None, cannot convert to int.

    other inputs should be in "elementary" units, i.e.:
        m: mass, in atomic mass units  (1 for H+)
        q: charge, in elementary charge units  (1 for H+; -1 for e-)

    other_info: any other info associated with this fluid.
        will be saved as attributes.
    '''
    def __init__(self, name=None, i=None, *, m=None, q=None, **other_info):
        super().__init__(name, i)
        self.m = m
        self.q = q
        self.other_info_keys = list(other_info.keys())
        for kw, val in other_info.items():
            setattr(self, kw, val)

    name = alias('s')

    def __repr__(self):
        contents = [repr(val) for val in [self.name, self.i] if val is not None]
        if self.m is not None:
            contents.append(f'm={self.m:.3f}')
        if self.q is not None:
            contents.append(f'q={self.q}')
        return f'{type(self).__name__}({", ".join(contents)})'

    def is_neutral(self):
        '''tells whether self is a neutral fluid. i.e. self.q == 0.
        if self.q is None, returns None instead of bool.
        '''
        if self.q is None: return None
        return self.q == 0

    def is_ion(self):
        '''tells whether self is an ion. i.e. self.q > 0.
        if self.q is None, returns None instead of bool.
        '''
        if self.q is None: return None
        return self.q > 0

    def is_electron(self):
        '''tells whether self is an electron. i.e. self.q < 0.
        if self.q is None, returns None instead of bool.
        '''
        if self.q is None: return None
        return self.q < 0

    def is_charged(self):
        '''tells whether self is a charged fluid. i.e. self.q != 0.
        if self.q is None, returns None instead of bool.
        '''
        if self.q is None: return None
        return self.q != 0

    def to_dict(self):
        '''returns a dictionary containing all the information from the Fluid object.'''
        result_dict = super().to_dict()
        result_dict["name"] = result_dict.pop("s") 
        result_dict["m"] = self.m
        result_dict["q"] = self.q
        for key in self.other_info_keys:
            result_dict[key] = getattr(self, key)
        return result_dict


class FluidList(DimensionValueList):
    '''list of fluids'''
    _dimension_key_error = FluidKeyError
    _dimension_value_error = FluidValueError
    value_type = Fluid

    name = elementwise_property('name')
    m = elementwise_property('m')
    q = elementwise_property('q')

    def is_neutral(self):
        '''return xarray.DataArray telling whether each fluid in self is neutral.'''
        return xr.DataArray([fluid.is_neutral() for fluid in self], coords=self)
    def is_ion(self):
        '''return xarray.DataArray telling whether each fluid in self is an ion.'''
        return xr.DataArray([fluid.is_ion() for fluid in self], coords=self)
    def is_electron(self):
        '''return xarray.DataArray telling whether each fluid in self is an electron.'''
        return xr.DataArray([fluid.is_electron() for fluid in self], coords=self)
    def is_charged(self):
        '''return xarray.DataArray telling whether each fluid in self is charged.'''
        return xr.DataArray([fluid.is_charged() for fluid in self], coords=self)

    def i_neutrals(self):
        '''return indices of neutrals in self'''
        return [i for i, fluid in enumerate(self) if fluid.q == 0]
    def i_ions(self):
        '''return indices of ions in self'''
        return [i for i, fluid in enumerate(self) if fluid.q > 0]
    def i_electrons(self):
        '''return indices of electrons in self'''
        return [i for i, fluid in enumerate(self) if fluid.q < 0]
    def i_charged(self):
        '''return indices of charged fluids in self'''
        return [i for i, fluid in enumerate(self) if fluid.q != 0]

    def neutrals(self):
        '''return FluidList of neutrals from self.'''
        return self[self.i_neutrals()]
    def ions(self):
        '''return FluidList of ions from self.'''
        return self[self.i_ions()]
    def electrons(self):
        '''return FluidList of electrons from self.'''
        return self[self.i_electrons()]
    def charged(self):
        '''return FluidList of charged fluids from self.'''
        return self[self.i_charged()]

    def get_neutral(self):
        '''return the single neutral fluid from self; raise FluidValueError if there isn't exactly 1.'''
        neutrals = self.neutrals()
        if len(neutrals) != 1:
            raise self._dimension_value_error(f'expected exactly 1 neutral fluid, but got {len(neutrals)}')
        return neutrals[0]

    def get_ion(self):
        '''return the single ion fluid from self; raise FluidValueError if there isn't exactly 1.'''
        ions = self.ions()
        if len(ions) != 1:
            raise self._dimension_value_error(f'expected exactly 1 ion fluid, but got {len(ions)}')
        return ions[0]

    def get_electron(self):
        '''return the single electron fluid from self; raise FluidValueError if there isn't exactly 1.'''
        electrons = self.electrons()
        if len(electrons) != 1:
            raise self._dimension_value_error(f'expected exactly 1 electron fluid, but got {len(electrons)}')
        return electrons[0]


''' --------------------- Convenient DimensionValueSetter objects --------------------- '''

class FluidSpecialValueSetter(Sentinel, DimensionValueSetter):
    '''class to set special values for FluidDimension.
    E.g. (fluid_dim.v = SET_ELECTRON) is equivalent to (fluid_dim.v = fluid_dim.values.get_electron())

    getter: str
        will be used as fluid_dim.values.getter() to get the value(s).
    name: str
        name of this object; will only be used in repr.

    additional args & kw go to Sentinel.__new__
    '''
    def __new__(cls, getter, name=None, *args_super, **kw_super):
        result = super().__new__(cls, name, *args_super, **kw_super)
        result.getter = getter
        return result

    def __init__(self, *args__None, **kw__None):
        '''do nothing; all the work is done in __new__.
        Also overrides DimensionValueSetter's __init__ which expects value_to_set input.'''
        pass

    def value_to_set(self, dim):
        '''return the value(s) to set, given the Dimension instance.'''
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE
        values_getter = getattr(dim.values, self.getter)
        return values_getter()

SET_CHARGED = FluidSpecialValueSetter('charged', 'SET_CHARGED')
SET_ELECTRON = FluidSpecialValueSetter('get_electron', 'SET_ELECTRON')
SET_ELECTRONS = FluidSpecialValueSetter('electrons', 'SET_ELECTRONS')
SET_ION = FluidSpecialValueSetter('get_ion', 'SET_ION')
SET_IONS = FluidSpecialValueSetter('ions', 'SET_IONS')
SET_NEUTRAL = FluidSpecialValueSetter('get_neutral', 'SET_NEUTRAL')
SET_NEUTRALS = FluidSpecialValueSetter('neutrals', 'SET_NEUTRALS')


''' --------------------- FluidDimension, FluidHaver --------------------- '''

class FluidDimension(Dimension, name='fluid', plural='fluids',
                     value_error_type=FluidValueError, key_error_type=FluidKeyError):
    '''fluid dimension, representing current value AND list of all possible values.
    Also has various helpful methods for working with this Dimension.
    '''
    pass  # behavior inherited from Dimension.


@FluidDimension.setup_haver
class FluidHaver(DimensionHaver, dimension='fluid', dim_plural='fluids'):
    '''class which "has" a FluidDimension. (FluidDimension instance will be at self.fluid_dim)
    self.fluid stores the current fluid (possibly multiple). If None, use self.fluids instead.
    self.fluids stores "all possible fluids" for the FluidHaver.
    Additionally, has various helpful methods for working with the FluidDimension,
        e.g. current_n_fluid, iter_fluids, take_fluid.
        See FluidDimension.setup_haver for details.
    '''
    def __init__(self, *, fluid=None, fluids=None, **kw):
        super().__init__(**kw)
        if fluids is not None: self.fluids = fluids
        self.fluid = fluid


''' --------------------- jFluidDimension, jFluidHaver --------------------- '''        

class jFluidDimension(Dimension, name='jfluid', plural='jfluids',
                      value_error_type=FluidValueError, key_error_type=FluidKeyError):
    '''jfluid dimension, representing current value AND list of all possible values.
    Also has various helpful methods for working with this Dimension.
    '''
    pass  # behavior inherited from Dimension.


@jFluidDimension.setup_haver
class jFluidHaver(DimensionHaver, dimension='jfluid', dim_plural='jfluids'):
    '''class which "has" a jFluidDimension. (jFluidDimension instance will be at self.jfluid_dim)
    self.jfluid stores the current jfluid (possibly multiple). If None, use self.fluids instead.
    self.jfluids stores "all possible jfluids" for the jFluidHaver.
    Additionally, has various helpful methods for working with the FluidDimension,
        e.g. current_n_fluid, iter_fluids, take_fluid.
        See jFluidDimension.setup_haver for details.

    (Some variables, like 'nusj' depend on multiple fluids; for those variables use fluid and jfluid.)
    '''
    def __init__(self, *, jfluid=None, jfluids=None, **kw):
        super().__init__(**kw)
        if jfluids is not None: self.jfluids = jfluids
        self.jfluid = jfluid

    def getj(self, var, *args__get, jfluid=UNSET, **kw__get):
        '''returns self(var), but for jfluid instead of fluid.
        jfluid: UNSET, None, or any jfluid specifier.
            if provided, use this instead of self.jfluid.

        Example:
                m_s = self('m')
                with self.using(fluids=self.jfluids, fluid=self.jfluid):
                    m_j_0 = self('m')
                m_j_1 = self.getj('m')
            here, the values stored in the variables will be:
                m_s = mass of self.fluid
                m_j_0 = mass of self.jfluid. But, fluid dimension will be labeled 'fluid'
                m_j_1 = mass of self.jfluid. fluid dimension will be labeled 'jfluid'.

        additional args and kwargs are passed to self(var)
        '''
        with self.using(fluids=self.jfluids, fluid=self.jfluid if jfluid is UNSET else jfluid):
            result = self(var, *args__get, **kw__get)
        if not kw__get.get('item', False):  # didn't do result.item(); i.e. result is still an xarray
            result = xarray_rename(result, {'fluid': 'jfluid'})
        return result


''' --------------------- FluidsHaver --------------------- '''

class FluidsHaver(FluidHaver, jFluidHaver):
    '''class which "has" a FluidDimension and a jFluidDimension.
    Most FluidHavers will probably be better off as FluidsHavers,
        since having a jFluid enables to calculate stuff like collision frequencies. 
    '''
    def get_neutral(self, var=None, *args__get, **kw__get):
        '''returns self(var), but for the neutral fluid.
        if var is None, instead returns the neutral fluid itself.

        if there is 1 neutral fluid in self.fluids, returns self(var, fluid=neutral_fluid).
        otherwise, if there is 1 in self.jfluids, returns self.getj(var, jfluid=neutral_fluid).
        otherwise (0 or >1 neutral fluids), raises FluidValueError.
        '''
        try:
            neutral_fluid = self.fluids.get_neutral()
            from_j = False
        except FluidValueError:
            try:
                neutral_fluid = self.jfluids.get_neutral()
                from_j = True
            except FluidValueError:
                raise FluidValueError('expected exactly 1 neutral fluid, but got 0 or multiple')
        if var is None:
            return neutral_fluid
        if from_j:
            return self.getj(var, jfluid=neutral_fluid, *args__get, **kw__get)
        else:
            return self(var, fluid=neutral_fluid, *args__get, **kw__get)
