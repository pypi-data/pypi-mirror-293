"""
File Purpose: collisional cross sections calculations
"""

from .cross_section_tools import CrossTable, CrossMapping
from ..quantity_loader import QuantityLoader

from ...tools import simple_setdefaultvia_property
from ...defaults import DEFAULTS

class CollisionsCrossSectionsLoader(QuantityLoader):
    '''cross section calculations. Mapping stored in self.collcross_map.

    This subclass is especially not intended for direct use; see CollisionsLoader instead.
    e.g. some methods here assume existence of helper methods implemented in CollisionsLoader.
    '''
    cross_mapping_type = CrossMapping

    collisions_cross_mapping = simple_setdefaultvia_property('_collisions_cross_mapping', '_default_cross_mapping',
        doc='''the collisions cross sections mapping to use.
        keys are (fluid1, fluid2) pairs; values are CrossTable objects.
            values can be provided as strings (filenames or defaults) instead, if smart==True;
            see help(self.collcross_mapping) for details.''')

    def _default_cross_mapping(self):
        '''return default CrossMapping object to use as self.collisions_cross_mapping.
        Called when accessing self.collisions_cross_mapping when no value has been set yet.
        '''
        return self.cross_mapping_type()

    @property
    def behavior_attrs(self):
        '''list of attrs in self which control behavior of self.
        here, returns ['collisions_cross_mapping'], plus any behavior_attrs from super().
        '''
        return ['collisions_cross_mapping'] + list(getattr(super(), 'behavior_attrs', []))

    @property
    def cross_table_defaults(self):
        '''dict of {shorthand: (filename, fc)} with shorthand useable in self.set_collisions_crosstab.'''
        return self.cross_mapping_type.cross_table_type.DEFAULTS

    def set_collisions_crosstab(self, fluid1, fluid2, crosstab):
        '''roughly, does self.collisions_cross_mapping[(fluid1, fluid2)] = crosstab,
        but this is a bit more convenient since it allows more shorthand options (see below)

        fluid1, fluid2: int, str, or Fluid
            the fluids to set the crosstab for.
            Fluid --> use the provided value.
            int or str --> infer the Fluid based on self.fluids.
        crosstab: None, str, or CrossTable
            None --> del self.collisions_cross_mapping[(fluid1, fluid2)], if possible.
            else --> self.collisions_cross_mapping[(fluid1, fluid2)] = crosstab.
                -- CrossTable --> will use the provided value.
                -- str --> will use the CrossTable corresponding to this filename or key,
                            key from self.cross_table_defaults.
                        Note: self.collisions_cross_mapping.smart=False can disable this.

        crosstab: still be provided as a string (filename or key from CrossTable.DEFAULTS.keys()),
            as long as self.collisions_cross_mapping.smart is True.
        
        Example, these are all equivalent, if fluid 0 is 'e' and fluid 1 is 'H II':
            self.set_collisions_crosstab('e', 'H II', 'e-h')
            self.set_collisions_crosstab(0, 1, 'e-h-cross.txt')
            self.set_collisions_crosstab(self.fluids.get('e'), self.fluids.get('H II'),
                                        CrossTable.from_file('e-h-cross.txt'))
            self.collisions_cross_mapping[(self.fluids.get(0), self.fluids.get(1))] = 'e-h'
        '''
        with self.using(fluid=fluid1, jfluid=fluid2):
            f1 = self.fluid
            f2 = self.jfluid
        if crosstab is None:
            self.collisions_cross_mapping.pop((f1, f2), None)
        else:
            self.collisions_cross_mapping[(f1, f2)] = crosstab

    def get_collisions_crosstab(self, fluid1, fluid2):
        '''roughly, returns self.collisions_cross_mapping[(fluid1, fluid2)],
        but, this is more convenient, because:
            - fluid1 and fluid2 can be provided in shorthand.
                can provide them as Fluid objects, ints, or strs.
        '''
        with self.using(fluid=fluid1, jfluid=fluid2):
            f1 = self.fluid
            f2 = self.jfluid
        return self.collisions_cross_mapping[(f1, f2)]

    @known_var(aliases=['collcross'])
    def get_collisions_cross_section(self):
        '''cross section between self.fluid and self.jfluid.
        interpolates on self.collcross_mapping based on mass-weighted temperature;
            cross_table = collcross_mapping[(fluid, jfluid)]
            T_sj = (m_j * T_s + m_s * T_j) / (m_j + m_s)
            result_si = cross_table(T_sj, input='T', output='cross_si')
            result = result_si * self.u('area')  # convert to self.units unit system.

        if collcross_mapping[(fluid, jfluid)] is not found:
            either return 0 (as an xarray), or raise QuantInfoMissingError,
            depending on self.collisions_mode. see help(type(self).collisions_mode) for details.
        '''
        # we need to use a loader and self.load_across_dims,
        #    because we can only handle looking up one cross section at a time
        #    (but it's possible that self.fluid or self.jfluid will be a list of fluids).
        __tracebackhide__ = DEFAULTS.TRACEBACKHIDE  # hides traceback from main func but not internal loader.
        def collcross_loader():
            fs, fj = self.fluid, self.jfluid
            if fs == fj:  # exclude same-same collisions
                return self('0')  # 0 as xarray
            try:
                cross_table = self.collisions_cross_mapping[(fs, fj)]
            except KeyError:
                return self._handle_missing_collisions_crosstab()  # if crash, includes KeyError info in traceback.
            T_sj = self('T_sj')
            result_si = cross_table(T_sj, input='T', output='collcross_si')
            result = result_si * self.u('area')
            return result
        return self.load_across_dims(collcross_loader, dims=['fluid', 'jfluid'])
