from typing import Any
from PyLibs.matrix import *

class linspace:
    def __init__(self, *args) -> None:
        if len(args) == 0:
            self.base = []
        elif isinstance(args[0], int):
            self.base = canonic(args[0])
        elif isinstance(args[0], Matrix):
            self.base = args[0].val
        else:
            self.base = args

    def __repr__(self) -> str:
        return "linspace" + repr(self.base)

    def __str__(self) -> str:
        return "LinSpace" + str(self.base)

    def get_dim(self) -> int:
        return len(self.base)
    
    def get_size(self) -> int:
        if self.dim == 0:
            return 0
        else:
            return len(self.base[0])
    
    dim = property(get_dim)
    size = property(get_size)


class linmap:
    def __init__(self, *args) -> None:
        if len(args) == 0:
            self.base = []
        elif isinstance(args[0], int):
            self.base = [[i==j for j in range(args[0])] for i in range(args[0])]
        elif isinstance(args[0], Matrix):
            self.base = args[0].val
        else:
            self.base = args
    
    def __repr__(self) -> str:
        return "linmap" + repr(self.base)
    
    def __str__(self) -> str:
        return "LinMap" + str(self.base)

    def get_dim(self) -> int:
        return len(self.base)
    
    def get_size(self) -> int:
        if self.dim == 0:
            return 0
        else:
            return len(self.base[0])
    
    dim = property(get_dim)
    size = property(get_size)

def mat(obj:linspace|linmap|tuple[int|float,...]|tuple[tuple[int|float,...],...], *bases:tuple[tuple[int|float,...],...]) -> Matrix:
    """Return the matrix form of a linear object
    
    * `mat(𝘴𝘱𝘢𝘤𝘦:linspace)` Return the matrix of the main base of the 𝘴𝘱𝘢𝘤𝘦 using canonical base
    * `mat(𝘴𝘱𝘢𝘤𝘦:linspace, 𝘣𝘢𝘴𝘦:tuple[tuple])` Return the matrix of the main base of the 𝘴𝘱𝘢𝘤𝘦 using the 𝘣𝘢𝘴𝘦
    * `mat(𝘮𝘢𝘱:linmap)` Return the matrix of the 𝘮𝘢𝘱 using canonical bases
    * `mat(𝘮𝘢𝘱:linmap, 𝘣𝘢𝘴𝘦:tuple[tuple])` Return the matrix of the 𝘮𝘢𝘱 using the 𝘣𝘢𝘴𝘦 (domain and codomain), only usable if 𝘮𝘢𝘱 is an endomorphism
    * `mat(𝘮𝘢𝘱:linmap, 𝘣𝘢𝘴𝘦₁:tuple[tuple], 𝘣𝘢𝘴𝘦₂:tuple[tuple])` Return the matrix of the 𝘮𝘢𝘱 using the 𝘣𝘢𝘴𝘦₁ (domain) and the 𝘣𝘢𝘴𝘦₂ (codomain)
    * `mat(𝘷𝘦𝘤𝘵𝘰𝘳:tuple)` Return the matrix of the 𝘷𝘦𝘤𝘵𝘰𝘳 using canonical base
    * `mat(𝘷𝘦𝘤𝘵𝘰𝘳:tuple, 𝘣𝘢𝘴𝘦:tuple[tuple])` Return the matrix of the 𝘷𝘦𝘤𝘵𝘰𝘳 using the 𝘣𝘢𝘴𝘦
    * `mat(𝘧𝘢𝘮𝘪𝘭𝘺:tuple[tuple*])` Return the matrix of the indexed 𝘧𝘢𝘮𝘪𝘭𝘺 of vectors using canonical base
    * `mat(𝘧𝘢𝘮𝘪𝘭𝘺:tuple[tuple*], 𝘣𝘢𝘴𝘦:tuple[tuple*])` Return the matrix of the indexed 𝘧𝘢𝘮𝘪𝘭𝘺 of vectors using the 𝘣𝘢𝘴𝘦
    """
    if isinstance(obj, linspace):
        return Matrix(obj.base)
    elif isinstance(obj, tuple) and len(obj) > 0:
        if isinstance(obj[0], tuple):
            m = Matrix(obj)
        else:
            m = Matrix([obj])
        if len(bases) == 1:
            return ~Matrix(bases[0]) * m.T
        else:
            return m.T
    elif isinstance(obj, linmap):
        m = Matrix(obj.base).T
        if len(bases) == 1:
            p = Matrix(bases[0])
            return ~p * m * p
        if len(bases) == 2:
            p = Matrix(bases[0])
            q = Matrix(bases[1])
            return ~q * m * p
        return m
    return Matrix()



def dim(obj:linspace|linmap):
    return obj.dim

def size(obj:linspace|linmap):
    return obj.dim

def is_indep(*vectors) -> bool:
    m = Matrix([[vectors[i][j] for j in range(len(vectors[0]))] for i in range(len(vectors))])
    return m.det != 0

def zero(i:int) -> tuple:
    return (0,)*i

def cob_mat(old_base, new_base):
    return ~mat(old_base) * mat(new_base)

def canonic(n:int) -> tuple[tuple[int,...],...]:
    return tuple([tuple([int(i==j) for j in range(n)]) for i in range(n)])

