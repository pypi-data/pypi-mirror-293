"""
File Purpose: calculating plasma heating, e.g. equilibrium T from E & collisions
"""
import numpy as np

from .plasma_parameters import PlasmaParametersLoader

from ..tools import format_docstring


class PlasmaHeatingLoader(PlasmaParametersLoader):
    '''plasma heating.'''
    # [EFF] these methods are efficient for EPPIC where B, nusn, kappa are constants.
    # [TODO][EFF] rewrite to avoid redundant calculations even those are not constant.

    _heating_eq_notes = '''
        From assuming u_n=0 and derivatives=0 in heating & momentum equations, which yields:
            T_s = T_n + Eheat_perp_coeff * |E_perp|^2 + Eheat_perp_coeff * |E_par|^2'''

    # # # GET HEATING # # #
    @known_var(deps=['m_n', 'skappa', 'mod_B', 'u_n'])
    @format_docstring(_heating_eq_notes=_heating_eq_notes)
    def get_Eheat_perp_coeff(self):
        '''Eheat_perp = Eheat_perp_coeff * |E_perp|^2. for E heating perp to B. Units of Kelvin.
        Eheat_perp_coeff = (m_n / (3 kB)) (kappa^2 / B^2) (1 / (1 + kappa^2))
        {_heating_eq_notes}
        '''
        assert np.all(self('u_n')==0), 'Eheat implementation assumes u_n=0'
        skappa = self('skappa')
        return (self('m_n') / (3 * self.u('kB'))) * (skappa**2 / self('mod2_B')) / (1 + skappa**2)

    @known_var(deps=['m_n', 'skappa', 'mod_B', 'u_n'])
    @format_docstring(_heating_eq_notes=_heating_eq_notes)
    def get_Eheat_par_coeff(self):
        '''Eheat_par = Eheat_par_coeff * |E_par|^2. for E heating parallel to B. Units of Kelvin.
        Eheat_par_coeff = (m_n / (3 kB)) (kappa^2 / B^2)
        {_heating_eq_notes}
        '''
        assert np.all(self('u_n')==0), 'Eheat implementation assumes u_n=0'
        skappa = self('skappa')
        return (self('m_n') / (3 * self.u('kB'))) * (skappa**2 / self('mod2_B'))

    @known_var(deps=['Eheat_perp_coeff', 'E_perpmag_B'])
    @format_docstring(_heating_eq_notes=_heating_eq_notes)
    def get_Eheat_perp(self):
        '''Eheat_perp = Eheat_perp_coeff * |E_perp|^2. heating perp to B. Units of Kelvin.
        Eheat_perp = (m_n / (3 kB)) (kappa^2 / B^2) (1 / (1 + kappa^2)) |E_perp|^2
        {_heating_eq_notes}
        '''
        return self('Eheat_perp_coeff') * self('E_perpmag_B')**2

    @known_var(deps=['Eheat_par_coeff', 'E_parmag_B'])
    @format_docstring(_heating_eq_notes=_heating_eq_notes)
    def get_Eheat_par(self):
        '''Eheat_par = Eheat_par_coeff * |E_par|^2. heating parallel to B. Units of Kelvin.
        Eheat_par = (m_n / (3 kB)) (kappa^2 / B^2) |E_par|^2
        {_heating_eq_notes}
        '''
        return self('Eheat_par_coeff') * self('E_parmag_B')**2

    @known_var(deps=['Eheat_perp', 'Eheat_par'])
    @format_docstring(_heating_eq_notes=_heating_eq_notes)
    def get_Eheat(self):
        '''Eheat = Eheat_perp + Eheat_par. total heating from electric field. Units of Kelvin.
        {_heating_eq_notes}
        '''
        return self('Eheat_perp') + self('Eheat_par')

    @known_var(deps=['Eheat', 'T_n'])
    def get_T_from_Eheat(self):
        '''T_from_Eheat = T_n + Eheat. Units of Kelvin.'''
        return self('T_n') + self('Eheat')
