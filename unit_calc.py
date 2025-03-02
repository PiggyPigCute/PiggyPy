
SI_UNIT = ["m", "kg", "s", "A", "K", "mol", "cd"]
SI_DIM = ["L", "M", "T", "I", "Θ", "N", "J"]
EXP_NUM = "⁰¹²³⁴⁵⁶⁷⁸⁹"

class unit():
    def __init__(self, base=[0,0,0,0,0,0,0], *args):
        assert len(base) == 7

        val = 1
        if len(args) >= 1:
            val *= args[0]

        self.si = base
        self.val = val

    def __repr__(self) -> str:
        result = (str(self.val))
        for i in range(7):
            if self.si[i] != 0:
                if self.si[i] > 0:
                    result += '*'
                else:
                    result += '/'
                result += SI_UNIT[i]
                if abs(self.si[i]) != 1:
                    result += "**" + str(abs(self.si[i]))
                    # for char in str(abs(self.si[i])): result += EXP_NUM[int(char)]
        return result

    def __str__(self) -> str:
        if isinstance(self.val, float):
            result = ('%g' % self.val) + ' '
        elif isinstance(self.val, int) and self.val == 1:
            result = ""
        else:
            result = str(self.val) + ' '
        for i in range(7):
            if self.si[i] != 0:
                result += SI_UNIT[i]
                if self.si[i] < 0: result += '⁻'
                if self.si[i] != 1: 
                    for char in str(abs(self.si[i])): result += EXP_NUM[int(char)]
                result += '·'
        return result.strip('·').strip(' ')
    
    def get_dim(self):
        return unit(self.si)

    dim = property(get_dim)

    def __abs__(self):
        return unit(self.si, abs(self.val))

    def __eq__(self, other) -> bool:
        if isinstance(other, unit):
            return self.si == other.si and self.val == other.val
        return False
    
    def __ne__(self, other) -> bool:
        if isinstance(other, unit):
            return self.si != other.si or self.val != other.val
        return False

    def __list__(self) -> list:
        return self.si
    
    def __add__(self, other):
        if not isinstance(other, unit):raise(TypeError("unsupported operand type(s) for +: 'unit' and " + repr(type(other).__name__)))
        assert self.si == other.si
        return unit(self.si, self.val + other.val)
    
    def __iadd__(self, other):
        self = self+other
        return self
    
    def __neg__(self):
        return unit(self.si, -self.val)

    def __sub__(self, other):
        if not isinstance(other, unit):raise(TypeError("unsupported operand type(s) for -: 'unit' and " + repr(type(other).__name__)))
        assert self.si == other.si
        return unit(self.si, self.val - other.val)
    
    def __isub__(self, other):
        self = self-other
        return self
    
    def __mul__(self, other):
        if isinstance(other, unit):
            if self.si == (unit()/other).si: # type: ignore
                return self.val/other.val
            new_si = [self.si[i] + other.si[i] for i in range(7)]
            return unit(new_si, self.val*other.val)
        else:
            return unit(self.si, self.val * other)
    
    def __rmul__(self, other):
        return self*other

    def __imul__(self, other):
        self = self*other
        return self
    
    def __truediv__(self, other):
        if isinstance(other, unit):
            if self.si == other.si:
                return self.val/other.val
            new_si = [self.si[i] - other.si[i] for i in range(7)]
            return unit(new_si, self.val/other.val)
        else:
            return unit(self.si, self.val / other)
    
    def __rtruediv__(self, other):
        return other*unit()/self

    def __itruediv__(self, other):
        self = self/other
        return self
    
    def __pow__(self, other):
        new_si = [round(self.si[i]*other) for i in range(7)]
        if any(new_si):
            return unit(new_si, self.val**other)
        return self.val**other
    
    def into(self, other) -> int|float:
        assert isinstance(other, unit)
        assert self.si == other.si
        return self.val/other.val
	
    
    
def unit_print(value:unit, unit:unit, symb="", name=None, *args, **kwargs):
    if name != None:
        print(name + " = ", end="")
    print(value/unit, symb, **kwargs)

def dim(unit:unit):
    return unit.dim

m_  = unit([1,0,0,0,0,0,0])
kg_ = unit([0,1,0,0,0,0,0])
s_  = unit([0,0,1,0,0,0,0])
A_  = unit([0,0,0,1,0,0,0])
K_  = unit([0,0,0,0,1,0,0])
mol_= unit([0,0,0,0,0,1,0])
cd_ = unit([0,0,0,0,0,0,1])

km_ = unit([1,0,0,0,0,0,0], 1e3)
dm_ = unit([1,0,0,0,0,0,0], 1e-1)
cm_ = unit([1,0,0,0,0,0,0], 1e-2)
mm_ = unit([1,0,0,0,0,0,0], 1e-3)
µm_ = unit([1,0,0,0,0,0,0], 1e-6)
nm_ = unit([1,0,0,0,0,0,0], 1e-9)
pm_ = unit([1,0,0,0,0,0,0], 1e-12)
ly_ = unit([1,0,0,0,0,0,0], 9460730472580800) # light-year

t_ = unit([0,1,0,0,0,0,0], 1e3)
g_ = unit([0,1,0,0,0,0,0], 1e-3)
mg_ = unit([0,1,0,0,0,0,0], 1e-6)
µg_ = unit([0,1,0,0,0,0,0], 1e-9)

min_ = unit([0,0,1,0,0,0,0], 60)
h_ = unit([0,0,1,0,0,0,0], 3600)
d_ = unit([0,0,1,0,0,0,0], 86400)
year_ = unit([0,0,1,0,0,0,0], 31557800)
ms_ = unit([0,0,1,0,0,0,0], 1e-3)
µs_ = unit([0,0,1,0,0,0,0], 1e-6)
ns_ = unit([0,0,1,0,0,0,0], 1e-9)


mA_ = unit([0,0,0,1,0,0,0], 1e-3)
mmol_ = unit([0,0,0,0,0,1,0], 1e-3)

kph_ = unit([1,0,-1,0,0,0,0], 1/3.6)
mps_ = unit([1,0,-1,0,0,0,0])
mpss_ = unit([1,0,-2,0,0,0,0])
N_ = unit([1,1,-2,0,0,0,0])
J_ = unit([2,1,-2,0,0,0,0])
eV_ = unit([2,1,-2,0,0,0,0], 1.602176634e-19)
W_ = unit([2,1,-3,0,0,0,0])
V_ = unit([2,1,-3,-1,0,0,0])
Ω_ = unit([2,1,-3,-2,0,0,0])
ohm_ = Ω_
S_ = unit([-2,-1,3,2,0,0,0])
H_ = unit([2,1,-2,-2,0,0,0])
F_ = unit([-2,-1,4,2,0,0,0])
L_ = unit([3,0,0,0,0,0,0], 1e-3)
mL_ = unit([3,0,0,0,0,0,0], 1e-6)
C_ = unit([0,0,1,1,0,0,0])
Pa_ = unit([-1,1,-2,0,0,0,0])
bar_ = unit([-1,1,-2,0,0,0,0], 1e-5)
Hz_ = unit([0,0,-1,0,0,0,0])
Bq_ = Hz_
T_ = unit([0,1,-2,-1,0,0,0])

π__ = 3.1415926535897932
pi__ = π__
c__ = unit([1,0,-1,0,0,0,0], 299792458)
g__ = unit([1,0,-2,0,0,0,0], 9.80665)
ε0__ = unit([-3,-1,4,2,0,0,0], 8.85418782e-12)
h__ = unit([2,1,-1,0,0,0,0], 6.62607015e-34)
e__ = unit([0,0,1,1,0,0,0], 1.602176634e-19)
µ0__ = unit([1,1,-2,-2,0,0,0], 12.566370614e-7)
me__ = unit([0,1,0,0,0,0,0], 9.109e-31)
mp__ = unit([0,1,0,0,0,0,0], 1.67262e-27)
mn__ = unit([0,1,0,0,0,0,0], 1.675e-27)


