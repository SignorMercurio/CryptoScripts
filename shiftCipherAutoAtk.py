import math

key_space = 26
c = 'OVDTHUFWVZZPISLRLFZHYLAOLYL'
lenc = len(c)
std = 0.065
dev = 99
k = 0

# from wikipedia
p = [0.08167,0.01492,0.02782,0.04253,0.12702,
     0.02228,0.02015,0.06094,0.06966,0.00153,
     0.00772,0.04025,0.02406,0.06749,0.07507,
     0.01929,0.00095,0.05987,0.06327,0.09056,
     0.02758,0.00978,0.02360,0.00150,0.01974,
     0.00074]
q = []

def num2ord(num):
    return ord('A') + num

def ord2num(i):
    return i - ord('A')


for i in range(key_space):
    q.append(c.count(chr(num2ord(i)) ) * 1.0 / lenc)

for j in range(key_space):
    Ij = 0
    for i in range(key_space):
        Ij += p[i] * q[(i+j) % key_space]
    cur_dev = math.fabs(Ij - std)  # deviation
    if (cur_dev < dev):
        dev = cur_dev
        k = j

print('Key: %d' % k)

m = ''
for i in range(lenc):
    m += chr(num2ord(ord2num(ord(c[i])-k) % key_space))

print('Plaintext: %s' % m)
# Key: 7
# Plaintext: HOWMANYPOSSIBLEKEYSARETHERE