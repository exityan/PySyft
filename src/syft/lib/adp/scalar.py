# stdlib
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
import random
from string import ascii_letters
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

# third party
import numpy as np
from scipy import optimize
from scipy.optimize import OptimizeResult
from sympy import Symbol
from sympy import diff
from sympy import symbols

# syft absolute
from syft.core.common.serde import Serializable

# syft relative
from .entity import Entity
from .idp_gaussian_mechanism import iDPGaussianMechanism

scalar_name2obj = {}


@lru_cache(maxsize=None)
def search(run_specific_args: Callable, rranges: Tuple) -> OptimizeResult:
    return optimize.shgo(run_specific_args, rranges)


class Scalar(Serializable):
    def __init__(
        self,
        value: Optional[float] = None,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None,
        poly: Optional[Symbol] = None,
        ent: Optional[Entity] = None,
        name: Optional[str] = None,
    ):

        if name is None:
            name = "".join([random.choice(ascii_letters) for _ in range(5)])

        self.name = name
        self._value = value
        self._min_val = min_val
        self._max_val = max_val
        # Tudor C: What is enabled?
        self.enabled = True

        if poly is not None:
            # if this Scalar is being formed as a function of other Scalar objects
            self._poly = poly
        elif ent is not None:
            # if you're creating a Scalar for the first time (no parents)
            self.scalar_name = self.name + "_" + ent.name
            self._poly = symbols(self.scalar_name)
            scalar_name2obj[self.scalar_name] = self
        else:
            raise Exception("Poly or ent must be not None")

    @property
    def poly(self) -> Symbol:
        return self._poly

    @property
    def value(self) -> float:
        if self._value:
            return self._value
        run_specific_args, index2symbol, _ = self.create_run_specific_args(f=self.poly)
        inputs = [scalar_name2obj[sym]._value for sym in index2symbol]
        return run_specific_args(inputs)

    @property
    def min_val(self) -> Optional[float]:
        return self._min_val

    @property
    def max_val(self) -> Optional[float]:
        return self._max_val

    def __mul__(self, other: "Scalar") -> "Scalar":
        result_poly = self.poly * other.poly
        result = Scalar(value=None, poly=result_poly)
        return result

    def __add__(self, other: "Scalar") -> "Scalar":
        result_poly = self.poly + other.poly
        result = Scalar(value=None, poly=result_poly)
        return result

    def __sub__(self, other: "Scalar") -> "Scalar":
        result_poly = self.poly - other.poly
        result = Scalar(value=None, poly=result_poly)
        return result

    def __str__(self) -> str:
        return str(self.poly) + "=" + str(self.value)

    def __repr__(self) -> str:
        return str(self)

    @property
    def sens(self) -> Optional[float]:
        if self.min_val and self.max_val:
            return self.max_val - self.min_val
        return None

    def neg_deriv(self, name: str) -> Symbol:
        obj = scalar_name2obj[name]
        return -diff(self.poly, obj.poly)

    def create_run_specific_args(
        self, f: Symbol
    ) -> Tuple[Callable, List[str], Dict[str, int]]:
        index2symbol = [str(x) for x in self.poly.free_symbols]
        symbol2index = {sym: i for i, sym in enumerate(index2symbol)}

        # Tudor: Here you weren't using *params
        # Tudor: If I understand correctly, .subs returns
        def _run_specific_args(tuple_of_args: tuple) -> Any:
            kwargs = {sym: tuple_of_args[i] for sym, i in symbol2index.items()}
            return f.subs(kwargs)

        return _run_specific_args, index2symbol, symbol2index

    def get_mechanism(
        self, symbol_name: str = "b", sigma: float = 0.1
    ) -> iDPGaussianMechanism:

        # Step 1: get derivative we want to maximize
        z = self.neg_deriv(symbol_name)
        run_specific_args, index2symbol, symbol2index = self.create_run_specific_args(
            f=z
        )

        rranges = list()
        for i, sym in enumerate(index2symbol):
            obj = scalar_name2obj[sym]
            rranges.append((obj.min_val, obj.max_val))

        # Step 3: maximize the derivative over a bounded range of <entity_name>
        resbrute = search(run_specific_args, tuple(rranges))
        resbrute = resbrute.x

        if isinstance(resbrute, np.float64):
            L = resbrute
        else:
            L = resbrute[symbol2index[symbol_name]]

        input_obj = scalar_name2obj[symbol_name]

        if input_obj._value is None:
            raise ValueError("Tudor: This should be an error, right?")

        # Step 4: create the gaussian mechanism object
        gm1 = iDPGaussianMechanism(
            sigma=sigma,
            value=input_obj._value,
            L=L,
            entity=symbol_name.split("_")[1],
            name="gm_" + symbol_name,
        )

        return gm1

    def get_all_entity_mechanisms(
        self, sigma: float = 0.1
    ) -> Dict[str, List[iDPGaussianMechanism]]:
        sy_names = self.poly.free_symbols
        entity2mechanisms = defaultdict(list)
        for sy_name in sy_names:
            mechanism = self.get_mechanism(symbol_name=str(sy_name), sigma=sigma)
            split_name = str(sy_name).split("_")
            entity_name = split_name[1]
            entity2mechanisms[entity_name].append(mechanism)

        return entity2mechanisms

    @property
    def entities(self) -> Set[str]:
        return {str(sy_name).split("_")[1] for sy_name in self.poly.free_symbols}

    # Tudor: remove the typing from Any to an accountant type
    def publish(self, acc: Any, sigma: float = 1.5) -> float:
        acc_original = acc

        assert sigma > 0

        acc_temp = deepcopy(acc_original)

        # get mechanisms for new publish event
        ms = self.get_all_entity_mechanisms(sigma=sigma)
        acc_temp.append(ms)

        overbudgeted_entities = acc_temp.overbudgeted_entities

        sample = random.gauss(0, sigma)

        while len(overbudgeted_entities) > 0:

            for sy_name in self.poly.free_symbols:
                entity_name = str(sy_name).split("_")[1]
                if entity_name in overbudgeted_entities:
                    sym = scalar_name2obj[str(sy_name)]
                    self._poly = self.poly.subs(sym.poly, 0)

            acc_temp = deepcopy(acc_original)

            # get mechanisms for new publish event
            ms = self.get_all_entity_mechanisms(sigma=sigma)
            acc_temp.append(ms)

            overbudgeted_entities = acc_temp.overbudgeted_entities

        output = self.value + sample

        acc_original.entity2ledger = deepcopy(acc_temp.entity2ledger)

        return output