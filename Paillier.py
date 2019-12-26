from Crypto.Util import number
import math
import random

# constants
n_length = 10
p = number.getPrime(n_length)
q = number.getPrime(n_length)
n = p*q
n2 = n**2
m1 = 15
m2 = 20

# general funcs
def L(x):
  global n
  return (x-1) // n

def lcm(a,b):
  return abs(a*b) // math.gcd(a,b)

def egcd(a, b):
  if a == 0:
    return (b, 0, 1)
  else:
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
  g, x, y = egcd(a, m)
  if g != 1:
    #raise Exception('Modular inverse does not exist')
    return -1
  else:
    return x % m

def quick_pow(a, b, p):
  ret = 1
  a %= p
  while b:
    if b&1:
      ret = (ret * a) % p
    b >>= 1
    a = (a * a) % p
  return ret

random.seed()
lamb = lcm(p-1, q-1)
mu = -1

while mu == -1:
  g = random.randint(0, n2-1)
  mu = modinv(L(quick_pow(g,lamb,n2)), n)

print('PubKey: (n={},g={})'.format(n,g))
print('PrivKey: (lambda={},p={},q={})'.format(lamb,p,q))
print('mu: {}'.format(mu))

r1 = random.randint(0,n-1)
r2 = random.randint(0,n-1)
c1 = quick_pow(g,m1,n2) * quick_pow(r1,n,n2) % n2
c2 = quick_pow(g,m2,n2) * quick_pow(r2,n,n2) % n2
print('c1: {}'.format(c1))
print('c2: {}'.format(c2))

m1_ = L(quick_pow(c1,lamb,n2)) * mu % n
m2_ = L(quick_pow(c2,lamb,n2)) * mu % n
print("m1': {}".format(m1_))
print("m2': {}".format(m2_))

m_ = L(quick_pow(c1*c2,lamb,n2)) * mu % n
print("m': {}".format(m_))