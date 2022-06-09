from dataclasses import dataclass


@dataclass
class Category:
    """
    Standin for Sagemath categories
    """

    objects: object
    morphisms: object


@dataclass
class iProxy:
    """
    WIP utiity class for working with HOM-sets

    TODO: this belongs in its own module
    """

    def __get__(self, obj, obj_type=None):
        pass

    def __set__(self, obj, value):
        pass

    def __getitem__(self, key):
        pass


class Morphism(dict):
    """
    Poor man's morphisms for objects obeying rank nullity theorem
    """

    @property
    def domain(self):
        return list(self.values())

    @property
    def codomain(self):
        return list(self.keys())

    def get_kernel(self, null):
        return list(k for k, v in self.items() if v == null)

    # TBD: unfortunately, we'll prolly need info about morphism, this might be a hack to accomplish that
    # def __get__(self, obj, obj_type=None):
    #     return self[obj]


class LinearMap(Morphism):
    """
    Temporary standin for a linear map until Sagemath is integrated (if the performance hit isn't too much)
    """

    def __add__(self, X):
        return LinearMap(dict(**self, **X))
