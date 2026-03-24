
class λ_expr:
    def __init__(self) -> None:
        ...

    def __mul__(self,other):
        return λ_app(self,other)
    
    def __add__(self,other):
        return other
    
    def __eq__(self, value) -> bool:
        return False
    
    def __bool__(self) -> bool:
        return self.β_normal_form() == λT
    
    def __len__(self) -> int:
        return 0

    def free_vars(self) -> set[str]:
        return set()
    
    def bound_vars(self) -> set[str]:
        return set()
    
    def α_rename(self,x,y):
        return self

    def sub(self,x,v):
        def mini_script(i):
            return str(i).replace("0","₀").replace("1","₁").replace("2","₂").replace("3","₃").replace("4","₄").replace("5","₅").replace("6","₆").replace("7","₇").replace("8","₈").replace("9","₉")
        xv_fv = v.free_vars().union(set([x]))
        inter = xv_fv.intersection(self.bound_vars())
        u = self.copy()
        u_bv = u.bound_vars()
        while len(inter)>0:
            y = next(iter(inter))
            i = 1
            while str(y)+mini_script(i) in u_bv:
                i += 1
            u = u.α_rename(y,str(y)+mini_script(i))
            u_bv = u.bound_vars()
            inter = xv_fv.intersection(u_bv)
        return u.valid_sub(x,v)

    def valid_sub(self,x,v):
        return self
    
    def β_contractions(self) -> list:
        return []
    
    def β_reductions(self, limit:int=30, exclusions=[]) -> list:
        if len(exclusions)>limit-1:
            return []
        conts = self.β_contractions()
        reds = [self.copy()]
        new_exclusions = reds+exclusions
        for red in self.β_contractions():
            if not red in new_exclusions:
                reds += red.β_reductions(limit,reds+exclusions)
                new_exclusions = reds+exclusions
        return reds
    
    def copy(self):
        return λ_expr()
    
    def is_normal_form(self) -> bool:
        return True
    
    def β_normal_form(self,limit=30):
        for red in self.β_reductions(limit):
            if red.is_normal_form():
                return red

class λ_var(λ_expr):

    def __init__(self, name) -> None:
        self.name = name
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return "λ_var('"+self.name+"')"
    
    def __eq__(self, other:λ_expr) -> bool:
        return isinstance(other, λ_var) and self.name == other.name
    
    def __add__(self, other:λ_expr) -> λ_expr:
        return λ_abs(self.name, other)
    
    def __len__(self) -> int:
        return 1
    
    def free_vars(self) -> set[str]:
        return set([self.name])
    
    def copy(self) -> λ_expr:
        return λ_var(self.name)
    
    def α_rename(self,x,y) -> λ_expr:
        return λ_var(self.name)

    def valid_sub(self,x,v:λ_expr) -> λ_expr:
        if x == self.name:
            return v
        else:
            return λ_var(self.name)
    
    def β_contractions(self) -> list[λ_expr]:
        return []

class λ_app(λ_expr):
    def __init__(self, s:λ_expr, t:λ_expr) -> None:
        self.s = s
        self.t = t
    
    def __str__(self) -> str:
        str_s, str_t = str(self.s), str(self.t)
        if isinstance(self.s, λ_abs) and len(str_s)>1:
            str_s = '('+str_s+')'
        if len(str_t)>1:
            str_t = '('+str_t+')'
        return str_s + str_t

    def __repr__(self) -> str:
        return "λ_app("+repr(self.s)+","+repr(self.t)+")"
    
    def __eq__(self, other:λ_expr) -> bool:
        return isinstance(other, λ_app) and self.s == other.s and self.t == other.t
    
    def __len__(self) -> int:
        return len(self.s) + len(self.t)
    
    def free_vars(self) -> set[str]:
        return self.s.free_vars().union(self.t.free_vars())
    
    def bound_vars(self) -> set[str]:
        return self.s.bound_vars().union(self.t.bound_vars())

    def copy(self) -> λ_expr:
        return λ_app(self.s.copy(),self.t.copy())
    
    def α_rename(self, x, y) -> λ_expr:
        return λ_app(self.s.α_rename(x,y),self.t.α_rename(x,y))
    
    def valid_sub(self,x,v:λ_expr) -> λ_expr:
        return λ_app(self.s.valid_sub(x,v),self.t.valid_sub(x,v))
    
    def β_contractions(self) -> list[λ_expr]:
        conts = []
        if isinstance(self.s,λ_abs):
            conts.append(self.s.expr.sub(self.s.var,self.t))
        for s_cont in self.s.β_contractions():
            conts.append(λ_app(s_cont,self.t))
        for t_cont in self.t.β_contractions():
            conts.append(λ_app(self.s,t_cont))
        return conts
    
    def is_normal_form(self) -> bool:
        return (not isinstance(self.s,λ_abs)) and self.s.is_normal_form() and self.t.is_normal_form()

class λ_abs(λ_expr):
    def __init__(self, var_name, expression:λ_expr):
        self.var = var_name
        self.expr = expression
    
    def __str__(self) -> str:
        if self.var=='a' and isinstance(self.expr,λ_abs) and self.expr.var=='b' and isinstance(self.expr.expr,λ_var):
            if self.expr.expr.name == 'a': return "T"
            if self.expr.expr.name == 'b': return "⊥"
        if self.var=='f' and isinstance(self.expr,λ_abs) and self.expr.var=='x':
            always_f = True
            expr = self.expr.expr
            i = 0
            while isinstance(expr,λ_app):
                if isinstance(expr.s,λ_var) and expr.s.name == 'f':
                    expr = expr.t
                    i += 1
                else:
                    always_f = False
                    break
            if always_f and isinstance(expr,λ_var) and expr.name == 'x':
                return str(i)
        return "λ" + str(self.var) + "." + str(self.expr)
    
    def __repr__(self) -> str:
        return "λ_abs("+repr(self.var)+","+repr(self.expr)+")"
    
    def __eq__(self, other:λ_expr) -> bool:
        return isinstance(other, λ_abs) and self.expr == other.expr.sub(other.var,λ_var(self.var))
    
    def __add__(self, other:λ_expr) -> λ_expr:
        return λ_abs(self.var, self.expr + other)
    
    def __len__(self) -> int:
        return len(self.expr) + 1

    def free_vars(self) -> set[str]:
        return self.expr.free_vars().difference(set([self.var]))
    
    def bound_vars(self) -> set[str]:
        return self.expr.bound_vars().union(set([self.var]))
    
    def copy(self) -> λ_expr:
        return λ_abs(self.var,self.expr.copy())
    
    def α_rename(self, x, y) -> λ_expr:
        if x==self.var:
            return λ_abs(y,self.expr.sub(x,λ_var(y)))
        else:
            return λ_abs(self.var,self.expr.α_rename(x,y))
    
    def valid_sub(self,x,v:λ_expr) -> λ_expr:
        return λ_abs(self.var,self.expr.valid_sub(x,v))
    
    def β_contractions(self) -> list:
        return [λ_abs(self.var,cont) for cont in self.expr.β_contractions()]
    
    def is_normal_form(self) -> bool:
        return self.expr.is_normal_form()

class LambdaExpressionParserError(Exception):
    def __init__(self, missing_element, text) -> None:
        super().__init__(missing_element+" is missing in the expression "+repr(text))

class LambdaExpressionConversionError(Exception):
    def __init__(self, obj_type) -> None:
        super().__init__("impossible to convert "+obj_type+" into λ-expression")

def λ_parser(text:str) -> λ_expr:
    text = text.replace(" ","")
    if len(text)==1:
        return λ_var(text)
    if text[0] in "λl":
        if len(text)<3 or text[2]!=".":
            raise LambdaExpressionParserError("Dot", text)
        return λ_abs(text[1],λ(text[3:]))
    else:
        if text[-1] == ")":
            b = 1
            i = len(text)-1
            while b>0:
                i -= 1
                if i<0:
                    raise LambdaExpressionParserError("Open bracket", text)
                if text[i] == ')':
                    b += 1
                if text[i] == '(':
                    b -= 1
            if i == 0:
                return λ(text[1:-1])
        else:
            i = len(text)-1
        return λ_app(λ(text[:i]),λ(text[i:]))

def λ(obj:λ_expr|bool|int|str|tuple) -> λ_expr:
    if isinstance(obj, λ_expr):
        return obj
    elif isinstance(obj, bool):
        return λT if obj else λF
    elif isinstance(obj, int):
        expr = λx
        for _ in range(obj):
            expr = λf*expr
        return λf+λx+expr
    elif isinstance(obj, tuple):
        if len(obj) != 2:
            raise LambdaExpressionConversionError("tuple with a length not equal to 2")
        s,t = λ(obj[0]), λ(obj[1])
        ττ = λ_var("ττ")
        return ττ+ττ*s*t
    elif isinstance(obj, str):
        return λ_parser(obj)
    else:
        raise LambdaExpressionConversionError(obj.__class__.__name__)

def print_β_tree(expr:λ_expr, exprs_stores:list[λ_expr]=[], firt_prefix:str="  ", prefix:str="  ", max_length=30) -> None:
    i = len(exprs_stores)
    print(" "*(i%100<10)+str(i%100)+firt_prefix,end="")
    if i==max_length:
        print("max_length exceeded")
        return
    exprs_stores.append(expr.copy())
    for j in range(i):
        if expr == exprs_stores[j]:
            print("line",j)
            return
    print(expr)
    conts = expr.β_contractions()
    for j in range(len(conts)):
        if j < len(conts)-1:
            print_β_tree(conts[j], exprs_stores, prefix+"├─ ", prefix+"│  ")
        else:
            print_β_tree(conts[j], exprs_stores, prefix+"└─ ", prefix+"   ")

def print_β_reductions(expr:λ_expr, limit:int=30):
    reds = expr.β_reductions(limit)
    normal_forms = []
    other_forms = []
    size = len(str(expr))
    for red in reds:
        str_red = str(red)
        if red.is_normal_form():
            normal_forms.append(str_red)
        else:
            other_forms.append(str_red)
        if len(str_red)>size:
            size = len(str_red)
    if len(reds)>=limit and len(expr.β_reductions(limit+1))>len(reds):
        other_forms.append("...")
    if size<24:
        size=23
    color,zero = "[2;36m","[0m"
    def plot_value(red):
        return zero+str(red)+" "*(size-len(str(red)))+color
    def plot_list(n,m,l):
        return ("─"*n if size<24 else "─"*(size-m))+"┤\n"+"\n".join(["│ "+plot_value(red)+" │" for red in l])+"\n"*(len(l)>0)
    print(color+"┌─ Original λ-expression "+"─"*(size-22)+"┐\n│ "+plot_value(expr)+" │\n├─"+"─────"*(size<24)+" Normal form "+plot_list(6,12,normal_forms)+"├─"+"──"*(size<24)+" Other β-reducions "+plot_list(3,18,other_forms)+"└"+"─"*(size+2)+"┘"+zero)

def β(expr:λ_expr, limit=30) -> λ_expr|None:
    return expr.β_normal_form(limit)

λa = λ_var('a')
λb = λ_var('b')
λf = λ_var('f')
λx = λ_var('x')

λT = λa+λb+λa
λF = λa+λb+λb