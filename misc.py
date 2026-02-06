import random as rd

def flist(iterable, f, *args, **kwargs) -> list:
    return [f(i, *args, **kwargs) for i in iterable]

def fmat(matrix, f, *args, **kwargs) -> list[list]:
    return [flist(i, f, *args, **kwargs) for i in matrix]

def cut(dec:float|complex|list, digits:int=3) -> float|complex|list:
    if isinstance(dec, list):
        return flist(dec, cut, digits)
    
    if isinstance(dec, complex):
        if round(dec.imag*10**digits) == 0:
            return cut(dec.real, digits)
        return cut(dec.real, digits) + 1j*cut(dec.imag, digits) #type:ignore
    
    return round(dec*10**digits)/10**digits
    

def rfloat(inf,sup):
    return rd.random()*(sup-inf)+inf

def rdigit():
    return rd.randint(0,9)

def ri():
    return rd.randint(-9,9)

def rf():
    return rfloat(-10,10)

def rj():
    return rf() + 1j*rf()

π = 3.14159265358979323

def is_prime(n:int) -> bool:
    if n < 2:
        return False
    for i in range(2,n-1):
        if n%i == 0:
            return False
    return True

def eratosthenes(n:int) -> list[bool]:
    if n < 2:
        return [False]*n
    table = [i>1 for i in range(n)]
    i = 2
    while i**2 < n:
        j = i*2
        while j < n:
            table[j] = False
            j *= i
        i += 1
    return table
