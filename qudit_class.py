import time
start_time = time.time()
import numpy as np
import cmath
import matplotlib.pyplot as plt


j = complex(0,1)       #j'ai mis ça comme variable complexe pour faciliter les choses


class qudit:
    def __init__(self,dimension,basis=0, **amp_phase):
        amp = amp_phase.get('amp')      #get the amplitude of the basis component of the given state EX.: (1,2,1) has the relative amplitude 1 to |0>, 2 to |1> and 1 to |2>
        phase = amp_phase.get('phase')
        self.dimension = dimension
        if amp:
            amp = np.asarray(amp)    #amp is received as a tuple, converts to numpy array
            # self.norm = cmath.sqrt(sum(np.multiply(self.total,self.total.conj())))
            # norm_amp = np.array([i/cmath.sqrt(sum(np.multiply(amp,amp))) for i in amp]) #normalize the state
            # self.values = norm_amp
        else:
            amp = np.zeros(dimension)
            amp[basis] = 1
        if phase:
            phase_array = np.asarray(phase)
            phase = np.exp(2*phase_array*np.pi*j)
        else:
            phase = np.ones(dimension)
        self.phases = phase.astype(complex)
        self.values = amp.real
        self.total = np.multiply(self.phases,self.values)
        self.probability = np.array([(abs(i))**2 for i in self.total])
        self.norm = cmath.sqrt(sum(self.probability))
        self.normalize()
        # if phase and len(amp) == len(phase):
        #     phases = np.array([cmath.exp(2*cmath.pi*j*i) for i in phase],dtype=complex)        #receive the phase angle of each state (state in the form e^(2*pi*i*theta)
        #     self.phases = phases
        #     self.total = np.multiply(self.phases,self.values)                    #state in the form: e^(2*pi*i*theta)*|ket>
        #     self.probability = np.array([(abs(i))**2 for i in self.total])

    def normalize(self):
        self.probability = np.array([(abs(i))**2 for i in self.values])
        self.norm = np.sqrt(sum(self.probability))
        self.values = self.values/self.norm
        self.values = self.values.round(decimals = 4)
        self.phases = self.phases.round(decimals = 4)
        self.total = self.values*self.phases
        self.probability = np.array([(abs(i))**2 for i in self.total])
        self.norm = np.sqrt(sum(self.probability))


    ###############################################################################
    #       THE HADAMARD GATE ALWAYS TAKES ONE STATE AND MAPS TO ALL THE OTHERS   #
    #       THE ONLY THING THAT CHANGES IS THE PHASE, THATS WHY NUMPY.ONES        #
    ###############################################################################

    def hadamard(self,direction=1):
        d = self.dimension
        for k in range(d):
            ak = 0
            for n in range(d):
                ak += np.sqrt(1/d)*self.total[n]*np.exp(direction*2*j*n*k*np.pi/d)
            self.values[k] = np.abs(ak)
            self.phases[k] = np.exp(j*np.angle(ak))
        self.normalize()

        # for k in range(len(self.phases)):
        #     self.phases[k] = self.phases[k]*cmath.exp(2*cmath.pi*j*k*self.values[k]/len(self.values))
        # self.values = np.ones(len(self.phases))/cmath.sqrt(len(self.values))
        # self.normalize()

    def measure(self):
         measure = np.random.choice([i for i in range(len(self.values))], p = self.probability)
         self.values, self.total = np.zeros(len(self.values)),np.zeros(len(self.values))
         self.values[measure], self.total[measure] = 1,1
         self.normalize()
         return measure,self

def c_rot(qdit_control, qdit_controlled, angle,c=-1): #control qdit can't be in a states' superposition
    state = np.where(abs(qdit_control.total) > 0.001)[0][0]
    if state != c and c!=-1:
        state = 0
    if state == c:
        state = 1
    for dimension in range(len(qdit_control.values)):
        qdit_controlled.phases[dimension] = qdit_controlled.phases[dimension]*np.exp(angle*j*state*dimension)
    qdit_controlled.normalize()
    return qdit_controlled


class register():
    def __init__(self, qudits):
        self.register = np.array(qudits)
        self.length = len(qudits)
        self.values = 

    def qft(self):
        for qudit in range(len(self.register)):
            self.register[qudit].hadamard()
            if qudit < len(self.register):
                for controlers in range((qudit + 1), len(self.register)):
                    angle = 2*np.pi/(self.register[0].dimension**(controlers - qudit+1))
                    self.register[qudit] = c_rot(self.register[controlers],self.register[qudit],angle)
                    self.register[qudit].normalize()
        # self.register = np.flip(self.register,0)


    def qft_1(self):
        # self.register = np.flip(self.register,0)
        for qudit in range(len(self.register)-1,-1,-1):
            if qudit < ((len(self.register)) - 1):
                for controlers in range(len(self.register) - 1, qudit, -1):
                    angle = 2*np.pi/(self.register[0].dimension**(controlers - qudit+1))
                    self.register[qudit] = c_rot(self.register[controlers],self.register[qudit],-angle)
            self.register[qudit].hadamard(-1)
            self.register[qudit].normalize()


    def measure(self):
        for i in range(len(self.register)):
            self.register[i].measure()

# q1 = qudit(3, amp = (1,0,0), phase = (0,0,0))
# print('q1 - values : {}'.format(q1.values))
# print('q1 - phases : {}'.format(q1.phases))
# print('q1 - total : {}'.format(q1.total))
# q1.hadamard()
# print('q1 - values : {}'.format(q1.values))
# print('q1 - phases : {}'.format(q1.phases))
# print('q1 - total : {}'.format(q1.total))


def proba_test(n,d):
    liste = np.zeros(d)
    for i in range(n):
        q1 = qudit(d)
        q1.hadamard()
        state = q1.measure()
        liste[state[0]]+=1
    return liste


# q1.hadamard_no_sup()
# print('q1 - values : {}'.format(q1.values.round(decimals = 3)))
# print('q1 - phases : {}'.format(q1.phases.round(decimals = 3)))
# print('q1 - total : {}'.format(q1.total.round(decimals = 3)))

#
q1 = qudit(4,amp=(1,0,0,0), phase=(0,0,0,0))
q2 = qudit(4,amp=(0,1,0,0), phase=(0,0,0,0))
q3 = qudit(4,amp=(0,0,1,0), phase=(0,0,0,0))
q4 = qudit(4,amp=(0,0,0,1), phase=(0,0,0,0))
#
#
r1 = register([q1,q2,q3,q4])
# print(r1.register[0].values,r1.register[1].values,r1.register[2].values)
# r1.qft()
# print('qft aplied')
# print('q1 - values : {}'.format(r1.register[0].values))
# print('q1 - phases : {}'.format(r1.register[0].phases))
# print('q1 - total : {}'.format(r1.register[0].total))
# print('q2 - values : {}'.format(r1.register[1].values))
# print('q2 - phases : {}'.format(r1.register[1].phases))
# print('q2 - total : {}'.format(r1.register[1].total))
# print('q3 - values : {}'.format(r1.register[2].values))
# print('q3 - phases : {}'.format(r1.register[2].phases))
# print('q3 - total : {}'.format(r1.register[2].total))
#
# r1.measure()
# print('measure')
# print('q1 - values : {}'.format(r1.register[0].values))
# print('q1 - phases : {}'.format(r1.register[0].phases))
# print('q1 - total : {}'.format(r1.register[0].total))
# print('q2 - values : {}'.format(r1.register[1].values))
# print('q2 - phases : {}'.format(r1.register[1].phases))
# print('q2 - total : {}'.format(r1.register[1].total))
# print('q3 - values : {}'.format(r1.register[2].values))
# print('q3 - phases : {}'.format(r1.register[2].phases))
# print('q3 - total : {}'.format(r1.register[2].total))
# print("--- %s seconds ---" % (time.time() - start_time))



def int_to_qudits(x,d,q):
    qudit_list = [qudit(d) for i in range(q)]
    i=1
    while x!=0 and i<=q:
        x , r = x//d , x % d
        qudit_list[q-i] = qudit(d,r)
        i += 1
    if i>q+1 or x!=0: print("pas assez de qudits")
    return register(list(qudit_list))

def base10_to_d(x,d,q):
    qudit_list = [0 for i in range(q)]
    i=1
    while x>0 and i<=q:

        x, r = x//d, x % d
        qudit_list[q-i] = r
        i += 1
    # if i>q+1 or x!=0 :print("pas assez de qudits")
    return qudit_list

def base_d_to10(x,d):
    q = len(x)
    somme = 0
    for i in range(q):
        somme+= x[q-i-1]*d**i
    return somme

def adder(r1,r2):
    r2.qft()
    for qudit in range(len(r2.register)):
        for counter in range(qudit, len(r1.register)):
            angle = 2*np.pi/(r1.register[0].dimension**(counter - qudit+1))
            r2.register[qudit] = c_rot(r1.register[counter], r2.register[qudit], angle)
    r2.qft_1()
    return r2

#
# r0 = int_to_qudits(32,4,3)
# r1 = int_to_qudits(5,4,3)
# somme = adder(r0,r1)

def euclide_etendu(a,b):
    r,u,v,r1,u1,v1 = a,1,0,b,0,1
    while r1!=0:
        q=r//r1
        r,u,v,r1,u1,v1 = r1,u1,v1,r-q*r1,u-q*u1,v-q*v1
    return r,u,v
