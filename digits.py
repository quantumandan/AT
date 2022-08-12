"""
Digit Machines:

The canonical permutation maps the k symbols labeled in a base-k numeration.

The tape is the number's fractional part, with '.' as the blank symbol and the current
position of the Read/Write head is given by the integer portion.

n = floor(x) ==> current position of the tape cursor
frac = {x} ==> current TM tape state

In this way, the entirety of an algorithm's operation can be captured as a composition algebra of
canonical permutation maps, the successor function, and the inclusion map; modeled as a power series.

d[n]: R \to N  # function that returns the nth digit of a real number
b[k]: R \to N  # function that returns the minimum prime number of symbols to represent x \in R as a base-k number

# in other words k <= b[k]

DM_STATE(x) := d[floor(x)]({x}|_b[floor(x)])
TM_STATE(x+1) := max(DM_STATE(x), DM_STATE(x+1))

0.123456
1.123456

DM_STATE(0.123456) = 0 # blank
DM_STATE(1.123456) = 1
DM_STATE(2.123456) = 2
DM_STATE(3.123456) = 3
DM_STATE(4.123456) = 4
...
DM_STATE(10.123456) = ..

# TM_STATE --> tropical geometry on functions of base-k numbers
TM_STATE(0.123456) = 0
TM_STATE(1.123456) = max(DM_STATE(0.123456), DM_STATE(1.123456)) ==> 1.123456
TM_STATE(2.123456) = max(DM_STATE(1.123456), DM_STATE(2.123456)) 

0.654321
1.654321

DM_STATE(0.654321) = 0 # blank
DM_STATE(1.654321) = 6
DM_STATE(2.654321) = 5
DM_STATE(3.654321) = 4
DM_STATE(4.654321) = 3
...
DM_STATE(10.654321) = ..

TM_STATE(0.654321) = 
TM_STATE(1.654321) = max(DM_STATE(0.654321), DM_STATE(1.654321)) ==> 1.123456
TM_STATE(2.654321) = max(DM_STATE(1.654321), DM_STATE(2.654321)) 


Use Lagrange interpolation of successor function and use mobius inversion to get transfer function:
----------------------------------------------------------------------------------------------------

# defines the set of interpolation coordinates for a Lagrange polynomial recording the sequence of states
# a Turing Machine takes as a function of applications of the successor function
L(i) = {(i, TM_STATE(x_i))}

# defines a bijection via Lagrange interpolation which specifies a total ordering to a set of symbols
# this is required to decategorify the Turing Machine from real number into a symbol alphabet. While arbitrary,
# the choice of ordering defines a "canonical permutation" which bijectively labels the symbol alphabet with
# a totally ordered set.
cPerm(i) = {(i, a_i)}

# defines a base-n digit sequence of states given by the first n-1th applications of the successor function on
# the Turing Machine's initial state.
S_n(i) = {(i, x_i)} for i < n

L_cP = {(i, L \circ cPerm)}
L_ct = {(t, L_cP/t!)} \congr {(i, \sigma^i cPerm^{-1} \circ S)}
\iota: N \to R st \iota(i): i \mapsto Vec({x_i})
"""
from collections import namedtuple
from typing import *
from numpy.polynomial import Polynomial
import random


AbstractIndexSet = namedtuple("AbstractIndexSet", ["alphabet", "base", "morphism"])


class BaseK_IndexSet(AbstractIndexSet):
    """
    An index set [n] is the set of all integers from zero to n-1. A BaseK_IndexSet
    contains all the integers less than n represented in base n.
    """

    ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    @property
    def M(self):
        return self.morphism

    # Credit to https://stackoverflow.com/a/53675480
    @classmethod
    def to_base(cls, s: str, b: int) -> str:
        res = ""
        while s:
            res += cls.ALPHABET[s % b]
            s //= b
        return res[::-1] or "0"

    def increment(self):
        """
        Bijection that takes [n] to [n + 1] (canonical injection)
        """
        pass


class CanonicalPermutation(BaseK_IndexSet):
    """
    A Digit Machine needs at least as many states as its alphabet. The
    fewest such states mapped bijectively to the integers is called a
    canonical permutation. This is an important consequence of using
    semi-simple algebras, which are unique only up to choice of permutation

    # TODO handle duplicate symbols

    Associates each symbol with a unique positive integer, returning
    a canonical permutation if no repeated symbols, otherwise is the
    canonical injection (which is surjective in the target space)
    """

    def __new__(cls, symbol_alphabet=None, base=None):
        # default to standard CS integer bases (so 0 thru 1 and A thru F)
        alphabet = symbol_alphabet if symbol_alphabet else cls.ALPHABET
        base = base if base else len(alphabet)
        morphism = dict(
            (symbol, cls.to_base(i, base)) for i, symbol in enumerate(alphabet)
        )
        return super(CanonicalPermutation, cls).__new__(
            cls, alphabet=alphabet, base=base, morphism=morphism
        )


# order via totally ordered index set, in this case the decimals
LEXICOGRAPHIC = CanonicalPermutation(base=10)

# represents the current state of a digit machine
State = namedtuple("State", ["digits", "cursor", "index_set"])


class DigitMachine(Polynomial):
    """
    A digit machine uses abstract "decimals" to encode the state of a Turing Machine.
    and models it's operation as a composition of morphisms. We construct a
    an isomorphism between a the real numbers and infinite series and
    deconstruct a real number as an infinite polynomial with integer coefficients.

    DM_STATE^0(x) := . <==> d[0](.)
    DM_STATE^1(x) := d[1]({x})
    DM_STATE^2(x) := nth[floor(x)]({x})

    # TODO WIP, not finalized, there are a number of pedagodgical means of approaching, which is best?
    """

    BLANK_SYMBOL = "."

    def __init__(self, number: str, bijection=LEXICOGRAPHIC, **kwargs):
        current_position, fractional_part = number.split(self.BLANK_SYMBOL)
        digits = "".join(bijection.M[d] for d in fractional_part)
        self.state = State(digits=digits, cursor=current_position, index_set=bijection)
        # reversed ordering of the coeffs to satisfy numpy API for newstyle polynomials
        super().__init__([int(d) for d in digits[::-1]], **kwargs)

    @property
    def D(self):
        """
        Returns the nth digit of the DM machine
        """
        return self.state.digits

    def __getitem__(self, k):
        return self.D[k]  # TODO implement default

    def r_shift(self):
        pass

    def l_shift(self):
        pass

    @classmethod
    def factory(cls, state: State, **kwargs):
        # convert state to inputs for a new digit machine
        number = cls.BLANK_SYMBOL.join((state.cursor, state.digits))
        return cls(number=number, bijection=state.index_set.morphism, **kwargs)

    def move(self, direction):
        # FIXME, reuses the index_set instead of incrementing it
        cursor = self.state.cursor
        if direction < 0:  # right
            cursor -= 1
        elif direction > 0:  # left
            cursor += 1
        new_state = State(
            digits=self.state.digits,
            cursor=cursor,
            index_set=self.state.index_set.morphism,
        )
        return self.factory(new_state)

    # def __iter__(self, haltif=False):
    #     for value in self.tape:
    #         pass
