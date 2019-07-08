#
# Interface classes for oxygen reaction in lead-acid batteries
#
import pybamm
from .base_interface import BaseInterface
from . import kinetics, diffusion_limited


class BaseInterfaceOxygenLeadAcid(BaseInterface):
    """
    Base lead-acid interface class

    Parameters
    ----------
    param :
        model parameters
    domain : str
        The domain to implement the model, either: 'Negative' or 'Positive'.


    **Extends:** :class:`pybamm.interface.BaseInterface`
    """

    def __init__(self, param, domain):
        super().__init__(param, domain)
        self.reaction_name = " oxygen"

    def _get_exchange_current_density(self, variables):
        """
        A private function to obtain the exchange current density for a lead acid
        deposition reaction.

        Parameters
        ----------
        variables: dict
            The variables in the full model.

        Returns
        -------
        j0 : :class: `pybamm.Symbol`
            The exchange current density.
        """
        c_e = variables[self.domain + " electrolyte concentration"]
        # If c_e was broadcast, take only the orphan
        if isinstance(c_e, pybamm.Broadcast):
            c_e = c_e.orphans[0]

        if self.domain == "Negative":
            j0 = pybamm.Scalar(0)
        elif self.domain == "Positive":
            j0 = self.param.j0_p_Ox_ref * c_e  # ** self.param.exponent_e_Ox

        return j0

    def _get_open_circuit_potential(self, variables):
        """
        A private function to obtain the open circuit potential and entropic change

        Parameters
        ----------
        variables: dict
            The variables in the full model.

        Returns
        -------
        ocp : :class:`pybamm.Symbol`
            The open-circuit potential
        dUdT : :class:`pybamm.Symbol`
            The entropic change in open-circuit potential due to temperature

        """
        if self.domain == "Negative":
            ocp = self.param.U_n_Ox
        elif self.domain == "Positive":
            ocp = self.param.U_p_Ox

        dUdT = pybamm.Scalar(0)

        return ocp, dUdT

    def _get_number_of_electrons_in_reaction(self):
        # TODO: remove the  / 2
        return self.param.ne_Ox / 2


class ForwardTafel(BaseInterfaceOxygenLeadAcid, kinetics.BaseForwardTafel):
    """
    Extends :class:`BaseInterfaceOxygenLeadAcid` (for exchange-current density, etc) and
    :class:`kinetics.BaseForwardTafel` (for kinetics)
    """

    def __init__(self, param, domain):
        super().__init__(param, domain)


class BackwardTafel(BaseInterfaceOxygenLeadAcid, kinetics.BaseBackwardTafel):
    """
    Extends :class:`BaseInterfaceOxygenLeadAcid` (for exchange-current density, etc) and
    :class:`kinetics.BaseBackwardTafel` (for kinetics)
    """

    def __init__(self, param, domain):
        super().__init__(param, domain)


class LeadingOrderDiffusionLimited(
    BaseInterfaceOxygenLeadAcid, diffusion_limited.LeadingOrder
):
    """
    Extends :class:`BaseInterfaceOxygenLeadAcid` (for exchange-current density, etc) and
    :class:`kinetics.BaseLeadingOrderDiffusionLimited` (for kinetics)
    """

    def __init__(self, param, domain):
        super().__init__(param, domain)
