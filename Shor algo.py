import qudit_class as qu
import U_gate as Ug
import numpy as np
import time

d = 4
q = 3
a = 150282879

r0 = qu.int_to_qudits(0,d,q)
r1 = qu.int_to_qudits(0,d,q)

print('Iniialisation')
print([i.values for i in r0.register])
print([i.values for i in r1.register])

r0.qft()
print('\n QFT sur r0')

print([i.values for i in r0.register])
print([i.values for i in r1.register])

r0,r1 = Ug.U(a,r0)

print('\n Porte U')
print([i.values for i in r0.register])
print([i.values for i in r1.register])

r0.qft_1()

r0.measure()
r1.measure()

print('\n Measure')
print([i.values for i in r0.register])
print([i.values for i in r1.register])
