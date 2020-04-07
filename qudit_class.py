import time
start_time = time.time()
import numpy
import cmath

j = complex(0,1)       #j'ai mis ça comme variable complexe pour faciliter les choses

class qudit:

    def __init__(self, **amp_phase):
        amp = amp_phase.get('amp')      #get the amplitude of the basis component of the given state EX.: (1,2,1) has the relative amplitude 1 to |0>, 2 to |1> and 1 to |2>
        phase = amp_phase.get('phase')
        if amp:
            amp = numpy.asarray(amp)    #amp is received as a tuple, converts to numpy array
            norm_amp = numpy.array([i/cmath.sqrt(sum(numpy.multiply(amp,amp))) for i in amp]) #normalize the state
            self.values = norm_amp

    ###############################################
    #       THIS PHASE PART IS NOT WORKING WELL   #
    #       NEITHER CHANGING ANYTHING             #
    ###############################################

        if phase and len(amp) == len(phase):
            phases = numpy.array([cmath.exp(2*cmath.pi*j*i) for i in phase])        #receive the phase angle of each state (state in the form e^(2*pi*i*theta)
            self.phases = phases
            self.total = numpy.multiply(self.phases,self.values)                    #state in the form: e^(2*pi*i*theta)*|ket>

    ###############################################################################
    #       THE HADAMARD GATE ALWAYS TAKES ONE STATE AND MAPS TO ALL THE OTHERS   #
    #       THE ONLY THING THAT CHANGES IS THE PHASE, THATS WHY NUMPY.ONES        #
    ###############################################################################

    def hadamard_no_sup(self):
        for k in range(len(self.phases)):
            self.phases[k] = self.phases[k]*cmath.exp(2*cmath.pi*j*k*self.values[k]/len(self.values))
        self.values = numpy.ones(len(self.phases))/cmath.sqrt(len(self.values))
        self.total = numpy.multiply(self.phases,self.values)

    def hadamard(self):                                             #general function, works with or without superposition (I guess)
        indices = numpy.where(self.values != 0)[0]                      #where the value is not zero, its a base state, so the Hadamard gate will act there
        aux_phases = numpy.zeros(len(self.values))                      #auxiliary array to accumulate the sum of all phases for each state (it stores the contribution of each basis state in the given vector for the final basis state)
        for k in range(len(indices)):                                   #applies the Hadamard gate for each basis state in the given vector
            aux_phases_2 = numpy.zeros(len(self.values))                #array that will store how each of the given basis states will contribute to the fase of the final states' superposition
            for counter in range(len(self.values)):
                aux_phases_2[counter] = self.phases[indices[k]]*self.phases[counter]*cmath.exp(2*cmath.pi*j*counter*indices[k]/len(self.values)) #funcionando
            aux_phases += aux_phases_2 #"funcionando"
        self.phases = aux_phases #phase of all the states
        self.values = numpy.ones(len(self.values))/cmath.sqrt(len(self.values))  #superposition of all the states
        self.total = numpy.multiply(self.phases,self.values)/cmath.sqrt(len(indices)) #sqrt(len(indices)) because it represents how many times the Hadamard gate was applied hence, how many times we will have the same basis state with different phases, EX.: |0>[e^(2*pi*i*theta1) + e^(2*pi*i*theta1)], so we must "normalize the basis state" cause it will be summed N times (where N is the number of elements != than 0 in the given state)


q1 = qudit(amp = (1,1,1,1), phase = (0,0,0,0))   #phase is not changing anything
print("values: {}".format(q1.values.round(decimals=2)))         #initial values of q1
print("phases: {}".format(q1.phases.round(decimals=2)))
print("total: {}".format(q1.total.round(decimals=2)))

q1.hadamard()

print("Hadamard Gate applied")
print("values: {}".format(q1.values.round(decimals=2)))
print("phases: {}".format(q1.phases.round(decimals=2)))
print("total: {}".format(q1.total.round(decimals=2)))
print("--- %s seconds ---" % (time.time() - start_time))
