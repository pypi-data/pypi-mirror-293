# Generic MC model

from abc import ABC, abstractmethod

from .._qablet import mc_price
from .base import Model, ModelStateBase


# Define Base Class for State Object for MC Models
# Todo add the abstract methods and what else is expected from this class.
class MCStateBase(ModelStateBase):
    """Class to maintain the state of a single asset MC process."""

    def get_value(self, unit):
        """Return the value of the asset at the current time,
        if this asset is handled by the model, otherwise return None."""
        return None

    @abstractmethod
    def advance(self, new_time: float): ...


# Define Base Class for MC Models
class MCModel(Model):
    """Abstract base class for all Monte Carlo models where the stochastic model
    is implemented in the python class."""

    def price_method(self):
        return mc_price


class MCPricer(ABC):
    """MC Pricer that uses a Py Model."""

    def __init__(self, state_class):
        self.state_class = state_class

    def price(self, timetable, dataset):
        """Calculate price of contract.

        Parameters:
            timetable (dict): timetable for the contract.
            dataset (dict): dataset for the model.

        Returns:
            price (float): price of contract
            stats (dict): stats such as standard error

        """

        model_state = self.state_class(dataset)
        model_state.reset()
        price = mc_price(
            timetable["events"],
            model_state,
            dataset,
            timetable.get("expressions", {}),
        )

        return price, model_state.stats
