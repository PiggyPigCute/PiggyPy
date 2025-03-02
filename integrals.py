

def riemann_left(f,a,b,n):
    s = 0
    for i in range(n):
        s += f(a+i*(b-a)/n)
    return s*(b-a)/n

def riemann_right(f,a,b,n):
    s = 0
    for i in range(1,n+1):
        s += f(a+i*(b-a)/n)
    return s*(b-a)/n

def riemann_mid(f,a,b,n):
    s = 0
    for i in range(n):
        s += f(a+(i+0.5)*(b-a)/n)
    return s*(b-a)/n

def riemann_mean(f,a,b,n):
    s = f(a) + f(b)
    for i in range(1,n):
        s += 2*f(a+i*(b-a)/n)
    return s*(b-a)/n/2

