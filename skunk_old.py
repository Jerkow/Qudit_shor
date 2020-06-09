import numpy as np

j = complex(0,1)

class qudit:
    def __init__(self,dimension,amps):
        self.dimension = dimension
        amp =[]
        norm = float(np.sqrt(sum(s ** 2 for s in amps)))
        for i in range(len(amps)):
            amp.append(amps[i]/norm)
        self.amp = np.asarray(amp, dtype = complex)

class register:
    def __init__(self,qudits):
        self.refresh(qudits)
        self.qudit_list = qudits
        self.length = len(qudits)
        self.dimension = len(qudits[0].amp)

    def refresh(self, qudits):
        if len(qudits) == 1:
            f = qudits.amp
        else:
            f = np.kron(qudits[0].amp,qudits[1].amp)
            for i in range(2,len(qudits)):
                f = np.kron(f,qudits[i].amp)
        self.register = np.array(f,dtype=complex)

    def hadamard(self, pos):
        d = self.dimension
        for p in pos:
            aux_amp = np.copy(self.qudit_list[p].amp)
            for k in range(d):
                ak = 0
                for n in range(d):
                    ak += np.sqrt(1/d)*aux_amp[n]*np.exp(2*j*n*k*np.pi/d)
                self.qudit_list[p].amp[k] = ak
        self.refresh(self.qudit_list)

    def c_rotation_k(self, control, target, k, inverse = 1):
        #state = np.where(abs(qdit_control.total) > 0.001)[0][0]
        d = self.dimension
        aux_phase = np.zeros(d, dtype = complex)
        for k in range(d):
            for n in range(d):
                aux_phase = *np.exp(2*np.pi*j*inverse/d**k)
        self.refresh(self.qudit_list)

q1 = qudit(4,[0,1,0,0])
q2 = qudit(4,[1,0,0,0])
q3 = qudit(4,[1,0,0,0])

r1 = register([q1,q2,q3])
print('hadamard')
r1.hadamard([0,1,2])
print("{}".format(r1.register.round(decimals=3)))
#print("{}".format([r1.qudit_list[i].amp.round(decimals = 3) for i in range(3)]))

