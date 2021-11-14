from symbol import Symbol

################################ E -> T X
def E_TX_up(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

def E_TX_down(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = tail[0].ast

################################ X 
# -> + T X
def X_PlusTX_up(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def X_PlusTX_down(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = head.tmp + tail[1].ast


# -> - T X
def X_PlusTX_up(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def X_PlusTX_down(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = head.tmp - tail[1].ast

# -> eps
def X_eps_up(head: Symbol, tail: list[Symbol]):
    head.ast = head.tmp


############################### T -> F Y
def T_FY_up(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

def T_FY_down(head: Symbol, tail: list[Symbol]):
    tail[1].tmp = tail[0].ast

############################### Y
# -> * F Y
def Y_TimesFY_up(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def Y_TimesFY_down(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = head.tmp * tail[1].ast

# -> / F Y
def Y_DivFY_up(head: Symbol, tail: list[Symbol]):
    head.ast = tail[2].ast

def Y_DivFY_down(head: Symbol, tail: list[Symbol]):
    tail[2].tmp = head.tmp / tail[1].ast

# -> eps
def Y_eps_up(head: Symbol, tail: list[Symbol]):
    head.ast = head.tmp

############################### F
# -> ( E )
def F_openEclosed_up(head: Symbol, tail: list[Symbol]):
    head.ast = tail[1].ast

# -> i
def F_i_up(head: Symbol, tail: list[Symbol], i):
    head.ast = Num(i)