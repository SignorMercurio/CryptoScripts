# general funcs
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

# constants
p = 11
a,b,c,d = 1,0,1,6 # y^2 = ax^3 + bx^2 + cx + d
sqrt = [-1,1,-1,5,2,4,-1,-1,-1,3,-1]

def E(x):
  return (a*x**3 + b*x**2 + c*x + d) % p

# dy/dx
def dE(x, y):
  return (3*a*x**2 + 2*b*x + c) * modinv(2*y, p)

def add(P, Q):
  x1,y1,x2,y2 = P[0],P[1],Q[0],Q[1]
  if x1==x2 and y1==y2:
    K = dE(x1,y1)
  else:
    K = (y2-y1) * modinv(x2-x1+p, p)
  B = (y1 - K*x1)
  x0 = -(d-B**2) * modinv(x1*x2, p) % p # (x-x1)(x-x2)(x-x0) = ...+d-B^2
  y0 = (K*x0 + B) % p
  return (x0, y0)

def mul(P, x):
  Q = P
  for i in range(x-1):
    Q = add(Q, P)
  return Q

def init():
  for i in range(p):
    y2 = E(i)
    print('x={}, y^2={}'.format(i, y2), end=' ')
    if sqrt[y2] != -1:
      print((i, sqrt[y2]), (i, p-sqrt[y2]))
    else:
      print()


init()
P = (2,7)
s = 5
Q = mul(P,s) # Q = sP
Estr = '{}x^3 + {}x^2 + {}x + {}'.format(a,b,c,d)
print('Pubkey: ({},{},{})'.format(Estr,P,Q))

m = 3
r = 7
c1 = mul(P,r) # (x1,y1)
c2 = mul(Q,r) # (x2,y2)
C = m * c2[0] % p
print('Ciphertext: {}'.format(c1+(C,))) # (x1,y1,C)

C_ = mul(c1,s) # (x',y')
print("(x',y'): {}".format(C_))
m_ = C * modinv(C_[0],p) % p # C * (x')^(-1)
print('Plaintext: {}'.format(m_))