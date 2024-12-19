from sympy import factorint

g = 2
a = 7
n = 61

# Факторизация n-1
factors = factorint(n-1)
print(factors)

p_list = list(factors.keys())
for i in range(len(p_list)):
    print(f'p{i+1} = {p_list[i]}')

a1, a2, a3 = {0:1}, {0:1}, {0:1}

a1[1] =  g**(n//p_list[0]) % n
a2[1] =  g**(n//p_list[1]) % n
a3[1] =  g**(n//p_list[2]) % n

for i in range(2,p_list[0]):
    a1[i] =  a1[1] ** i % n

for i in range(2,p_list[1]):
    a2[i] = a2[1] ** i % n

for i in range(2,p_list[2]):
    a3[i] = a3[1] ** i % n
print()
print(a1)
print(a2)
print(a3)
print()
b0_1 = (a ** (n // p_list[0])) % n
index = [key for key, value in a1.items() if value == b0_1]
x0_1 = index[0]
print(f"b0_1 = {a}^{n // p_list[0]} mod {n} = {b0_1}, x0_1 = {x0_1}")

b0_2 = (a ** (n // p_list[1])) % n
index = [key for key, value in a2.items() if value == b0_2]
x0_2 = index[0]
print(f"b0_2 = {a}^{n // p_list[1]} mod {n} = {b0_2}, x0_2 = {x0_2}")

b0_3 = (a ** (n // p_list[2])) % n
index = [key for key, value in a3.items() if value == b0_3]
x0_3 = index[0]
print(f"b0_3 = {a}^{n // p_list[2]} mod {n} = {b0_3}, x0_3 = {x0_3}")

print()
x_values = [x0_1, x0_2, x0_3]
m = []
for i, (key, value) in enumerate(factors.items()):
    print(f"x = {x_values[i]} mod {key**value}")
    m.append(key**value)

print(m)

M = [m[0] * m [1] * m[2], 
    m[1]*m[2],
    m[0]*m[2],
    m[0]*m[1]
]
