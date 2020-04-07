import qudit_class as qu
import numpy as np
import time
a=5


#Multiplier of one register with one constant
def MULC(x,b):
    r0 = x
    d = x.register[0].dimension
    q = x.length
    r1 = qu.register([qu.qudit(d) for i in range(q)])
    r1.qft()
    # print([i.total for i in r1.register])
    r0,r1 = MAC(r0,r1,b)
    r1.qft_1()
    # r0.qft()
    # b_1 = qu.euclide_etendu(b,d)[1]
    # r0,r1 = MAC(r1,r0,b_1%d,-1)
    # r1.qft_1()
    # print([a.values for a in r0.register])
    # print([a.values for a in r1.register])
    return r1

def MAC(x,phia,b,signe = 1):
    d = x.register[0].dimension
    q = x.length
    for i in range(q):
        phia = GCADDC(x.register[q-i-1],phia,b,signe)
        b = d*b
    return x,phia

def GCADDC(e,phia,b,signe=1):
    d = e.dimension
    # q = len(phia.register)
    for i in range(1,d):
        phia = CADDC(e,phia,i,i*b,signe)
        # a = [qu.qudit(d) for i in range(q)]
        # for k in range(q):
        #     a[k].values = phia.register[k].values.copy()
        #     a[k].phases = phia.register[k].phases.copy()
        #     a[k].total = phia.register[k].total.copy()
        #     a[k].normalize()
        # phib = qu.register(a)
        # phib.qft_1()
        # print('a',[x.values for x in phib.register])
    return phia

def CADDC(e,phia,c,b,signe=1):
    q = len(phia.register)
    d = phia.register[0].dimension
    b_base_d = qu.base10_to_d(b,d,q)
    for i in range(1,q+1):
        bi_liste = b_base_d[i-1:]
        bi = qu.base_d_to10(bi_liste,d)
        phia.register[i-1] = qu.c_rot(e,phia.register[i-1],signe*2*np.pi*d**(-q+i-1)*bi,c)
    return phia


# B = MULC(x,2)

# print([a.values for a in B[0].register])
# print([a.values for a in B[1].register])
#
# d = 4
# n = 12
# q = int(np.log(n)/np.log(d))+2
# print(q,'qudits de dimension',d,'sont utilisés')
# x = qu.int_to_qudits(n,d,q)
# b = 3
# # e = qu.qudit(4,3)
# # phia = qu.register([qu.qudit(4,i) for i in range(3)])
# # print([a.probability.round(decimals=4) for a in phia.register])
# # phia.qft()
# # c = 3
# #
# # X = CADDC(e,phia,c,b)
# #
# # X.qft_1()
#
#
# # X= GCADDC(e,phia,b)
# # X,phia = MAC(x,phib,b)
# print('Calcul en cours ...')
# start_time = time.time()
# X = MULC(x,b)
# end_time = time.time()
# print('Calcul terminé en',end_time-start_time,'secondes')
# print([a.probability.round(decimals=4) for a in X.register])





#Multiplier of two registers

def MULC2(x,b):
    r0 = x
    d = x.register[0].dimension
    q = x.length
    r1 = qu.register([qu.qudit(d) for i in range(q)])
    r1.qft()
    # print([i.total for i in r1.register])
    r0,r1 = MAC2(r0,r1,b)
    r1.qft_1()
    # r0.qft()
    # b_1 = qu.euclide_etendu(b,d)[1]
    # r0,r1 = MAC(r1,r0,b_1%d,-1)
    # r1.qft_1()
    # print([a.values for a in r0.register])
    # print([a.values for a in r1.register])
    return r1

def MAC2(x,phia,b,signe = 1):
    d = x.register[0].dimension
    q = x.length
    for i in range(q):
        phia = GCADDC2(x.register[q-i-1],phia,b,signe)
        b = MULC(b,d)
    return x,phia

def GCADDC2(e,phia,b,signe=1):
    d = e.dimension
    # q = len(phia.register)
    for i in range(1,d):
        z = MULC(b,i)
        phia = CADDC2(e,phia,i,z,signe)
        # a = [qu.qudit(d) for i in range(q)]
        # for k in range(q):
        #     a[k].values = phia.register[k].values.copy()
        #     a[k].phases = phia.register[k].phases.copy()
        #     a[k].total = phia.register[k].total.copy()
        #     a[k].normalize()
        # phib = qu.register(a)
        # phib.qft_1()
        # print('a',[x.values for x in phib.register])
    return phia

def CADDC2(e,x,c,b,signe=1):
        d = x.register[0].dimension
        q = len(x.register)
        # self.qft() #prepare the register
        #print('inital qft: ', [i.total.round(decimals = 3) for i in self.register])
        for qudit in range(q):
            phase = np.ones(d, dtype=complex)
            bi_liste = []
            for k in range(qudit, len(b.register)):
                state = np.where(b.register[k].probability > 0.001)[0][0]
                bi_liste.append(state)
            bi = qu.base_d_to10(bi_liste,d)
                    # phase[m] = phase[m]*np.exp(qu.j*2*np.pi*m*state/(dim**(k)))
            x.register[qudit] = qu.c_rot(e,x.register[qudit],signe*2*np.pi*d**(-q+qudit)*bi,c)
            #print('phase is : ', phase.round(decimals = 3))
            x.register[qudit].total = np.multiply(x.register[qudit].total,phase)
        return x

# d = 4
# n = 12
# q = int(np.log(n)/np.log(d))+2
# print(q,'qudits de dimension',d,'sont utilisés')
# x = qu.int_to_qudits(n,d,q)
# b = 3
# b = qu.int_to_qudits(b,d,q)
# # print([i.values for i in b.register])
# # print([i.values for i in x.register])
# print('Calcul en cours ...')
# start_time = time.time()
# X = MULC2(x,b)
# end_time = time.time()
# print('Calcul terminé en',end_time-start_time,'secondes')
#
#
# print([a.probability.round(decimals=4) for a in X.register])

def puis_mod(x,k,d):
    if k%2 == 0:
        if k == 0:
            return 1
        else:
            z = puis_mod(x,k//2,d)
            return (z*z)%d
    else:
        if k !=1:
            z = puis_mod(x,(k-1)//2,d)
            return (z*z*x)%d
        else:
            return x%d


def puis_list(n,d,q):
    liste = [n%d**q]
    for i in range(q-1):
        liste.append(puis_mod(liste[-1],d,d**q))
    return liste


def liste_produits(n,x):
    d = x.register[0].dimension
    q = len(x.register)
    liste = puis_list(n,d,q)
    Produits = []
    for i in range(q):
        Produits.append(puis_quant(qu.int_to_qudits(liste[i],d,q),x.register[q-i-1],d,q))
    return Produits

def puis_quant(n,qudit,d,q):
    k = np.where(abs(qudit.total) > 0.001)[0][0]
    if k%2 == 0:
        if k == 0:
            return qu.int_to_qudits(1,d,q)
        else:
            z = puis_quant(n,qu.int_to_qudits(k//2,d,q).register[0],d,q)
            return MULC2(n,n)
    else:
        if k !=1:
            z = puis_quant(x,qu.int_to_qudits((k-1)//2,d,q).register[0],d,q)
            return MULC2(z,MULC2(z,n))
        else:
            return n

a = 11
x = qu.int_to_qudits(6,4,3)

# print([[i.values for i in j.register] for j in liste_produits(a,x)])

def U(a,x):
    q = len(x.register)
    d = x.register[0].dimension
    Liste = [i for i in liste_produits(a,x)]
    res = Liste[0]
    for k in range(1,q):
        res = MULC2(res,Liste[k])
    return x,res

UX = U(a,x)

# print([i.values for i in UX[1].register])


