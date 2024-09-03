"""
File Purpose: UnitsManager
"""

PHYSICAL_CONSTANTS_SI = dict(amu=1.66054e-27,  # kg, atomic mass unit
)

class UnitsManager():
    '''manages units, including conversion factors and physical constants in different unit systems.

    units: str
        the current unit system. E.g., 'si' or 'base'.
    sic: dict
        dict of known conversion factors, from 'base' units to 'si' units.
        E.g. (length in 'base' units) * (sic['l']) = (length in 'si' units)
        "sic" for "SI Conversion factors"
    '''
    def __init__(self, units='si', sic=dict(), **kw_super):
        self.units = units
        self.sic0 = sic
        self.sic = sic
        self.populate_sic()
        super().__init__(**kw_super)

    def __call__(self, ustr, units=None, units_input='base'):
        '''return ustr in [units] system. 

        ustr: str
            quantity or conversion factor, to get in the desired units.
            quantity example:
                self('amu', 'si') --> 1 atomic mass unit in SI units (kg) == 1.66054e-27
            conversion factor example:
                self('l', 'si') --> conversion factor from units_input length to SI units for length.
        units_input: str, default 'base'
            unit system for input.
            if 'base', get value from conversion factors known by self.sic.
        '''
        if units is None:
            units = self.units
        if units == units_input:
            return 1  # no conversion necessary in this case
        sic = self.sic
        if ustr in sic:  # this is a known conversion factor
            if (units == 'si') and (units_input == 'base'):
                return sic[ustr]      # multiply by this to convert from 'base' to 'si'
            elif (units == 'base') and (units_input == 'si'):
                return 1 / sic[ustr]  # multiply by this to convert from 'si' to 'base'
            else:
                # [TODO] handle other unit systems?
                raise NotImplementedError(f'unit system conversion for {units!r} and {units_input!r}')
        else:
            if ustr == 'amu':
                if units == 'si':
                    return PHYSICAL_CONSTANTS_SI['amu']
                elif units == 'base':
                    return PHYSICAL_CONSTANTS_SI['amu'] / sic['m']
            # [TODO] handle conversions between constants.
            raise NotImplementedError('[TODO]')


    def docu(self, ustr, doc):
        '''record doc for ustr in self.udocs. self.help() will show these docs.
        docu should be used for conversion factors.
        E.g. self.docu('l', 'length')
        '''
        try:
            udocs = self.udocs
        except AttributeError:
            self.udocs = dict()
        self.udocs[ustr] = doc

    def docc(self, cstr, doc):
        '''record doc for cstr in self.cdocs. self.help() will show these docs.
        docc should be used for quantities.
        E.g. self.docu('amu', 'atomic mass unit, ~mass of one proton')
        '''
        try:
            cdocs = self.cdocs
        except AttributeError:
            self.cdocs = dict()
        self.cdocs[cstr] = doc

    def help(self):
        '''print help for all known quantities and conversion factors.'''
        # [TODO] prettier spacing in printout
        # [TODO] also print numerical values
        print('known conversion factors:')
        for ustr, doc in self.udocs.items():
            print(f'    {ustr}: {doc}')
        print('known conversion factors:')
        for cstr, doc in self.cdocs.items():
            print(f'    {cstr}: {doc}')

    def populate_sic(self):
        '''fill self.sic with conversion factors for other units, based on the ones provided.
        E.g., sic['u'] = sic['l'] / sic['t'], if 'l' and 't' are provided, since velocity = length / time.

        ideally, this function should only rely on some minimal set of known conversion factors,
            e.g. 'l', 't', and 'm'.
        to get the values of those conversion factors, given some more-derived already-known conversions,
            you should use a different function instead.
            E.g., self.sic_from_PIC(eps0, ...) gives a dict of 'l', 't', and 'm' given the units for a PIC code.
        '''
        sic = self.sic
        docu = self.docu
        if 'u' not in sic:
            if 'l' in sic and 't' in sic:
                sic['u'] = sic['l'] / sic['t']
                docu('u', 'velocity')
        # [TODO] populate other conversion factors...
        # [TODO] maybe encapsulate the if statements into a function, to make things cleaner,
        #    e.g. can_make('u', reqs=('l', 't')) would check that 'u' not in sic, but 'l' and 't' are.

    def sic_from_PIC(self, *, eps0, q_over_m):  # maybe more args too, I'm not sure.
        '''returns dict of conversion factors, given the units for a PIC code.'''
        # the '*' means everything after that must be provided by keyword (not just positional),
        #   that will probably help prevent errors from accientally messing up the order.
        raise NotImplementedError('[TODO]')
