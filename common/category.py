from dataclasses import dataclass


@dataclass
class Category:
    objects: object
    morphisms: object


@dataclass
class iProxy:
    def __get__(self, obj, obj_type=None):
        pass

    def __set__(self, obj, value):
        pass

    def __getitem__(self, key):
        pass


class Morphism(dict):
    @property
    def domain(self):
        return list(self.values())

    @property
    def codomain(self):
        return list(self.keys())

    def get_kernel(self, null):
        return list(k for k, v in self.items() if v == null)

    # def __get__(self, obj, obj_type=None):
    #     return self[obj]


class LinearMap(Morphism):
    def __add__(self, X):
        return LinearMap(dict(**self, **X))
