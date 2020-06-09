import numpy as np
from scipy.sparse import dia_matrix
import matrices_lib as matlib
j = complex(0,1)

"""
Here, we adopt the following convention for the indexing of the qudits in a register:
0 is the index of most significant digit, or the left-most digit in the ket representation |xyz> (x is index 0)
"""



class qudit:
    def __init__(self,dimension,amps):

        """
        :param dimension: dimension of the qudit in question
        :param amps: array of non-normalized initial amplitudes for this qudit
        """

        self.dimension = dimension
        amp =[]
        norm = float(np.sqrt(sum(s ** 2 for s in amps)))
        for i in range(len(amps)):  # Normalization of the qudit amplitude vector
            amp.append(amps[i]/norm)
        self.amp = np.asarray(amp, dtype = complex)

class register:
    def __init__(self,qudits):
        """
        :param qudits: ordered list of all the qudits composing this register, from most to least significant
        """
        self.initialize_register(qudits)
        self.qudit_list = qudits
        self.length = len(qudits)
        self.dimension = len(qudits[0].amp)

    def initialize_register(self, qudits):
        """
        :param qudits: array of qudits to be transformed into a single register through kronecker multiplication
        :return: array representing the register

        """
        # Slightly less efficient version, that is tested
        # if len(qudits) == 1:
        #     f = qudits.amp
        # else:
        #     f = np.kron(qudits[0].amp,qudits[1].amp)
        #     for i in range(2,len(qudits)):
        #         f = np.kron(f,qudits[i].amp)
        # self.register = np.array(f,dtype=complex)

        if len(qudits) == 1:    # If our register is 1 qudit long, we keep it as is
            f = qudits.amp
        else:                   # If we have more than 1 qudit, initialize with the amplitudes of the first
            f = qudits[0].amp
            for i in range(1,len(qudits)):  # Then multiply in sequence all the other qudit arrays
                f = np.kron(f,qudits[i].amp)

        self.register = np.array(f,dtype=complex)


    """ Applies the corresponding gates based on the inputs given """
    def hadamard(self, target):
        self.one_qudit_op('hadamard', target)

    def rotation(self, target, angle = 0):
        self.one_qudit_op('r', angle = angle)

    def rotation_k(self, target, k = 1):
        self.one_qudit_op('r_k', k = k)

    def not_gate(self, target):
        self.one_qudit_op('not')


    """ Generates the matrix form of the given one qudit gates in function of the qudit position 
        and specific parameters. Applies the operation to the register """
    def one_qudit_op(self, gate, target, **kwargs):

        # used to define operator matrix size
        d = self.dimension
        l = self.length
        op_size = self.dimension**self.length


        """ Gets the base operator matrix from the 'matrices_lib' code """

        if gate == 'hadamard':
            base_matrix = matlib.h_matrix(d)
        elif gate == 'r':
            base_matrix = matlib.r_matrix(d, kwargs.get('angle'))
        elif gate == 'r_k':
            base_matrix = matlib.r_k_matrix(d, kwargs.get('k'))
        elif gate == 'not':
            base_matrix = matlib.not_matrix(d)

        """ 
            Building the operator matrix:
            If the target qudit is the first in the register, we begin with the basic operator matrix
            and then multiply by the necessary number of identities: op = M .I.I...I 
        """

        if target == 0:
            operator = base_matrix
            for i in range(1,l):
                operator = np.kron(operator, np.identity(d))
        else:

            """ else,  the kronecker multiplication involving M must be made between 
                identities: op = I.I...I. M .I.I...I (kron. prod. non-commutative)"""

            operator = np.identity(d)   # initializes the operator with I
            for i in range(1, target):  # identity multiplication until target position is reached
                operator = np.kron(operator, np.identity(d))
            i = target
            operator = np.kron(operator, base_matrix)    # multiplying the M matrix at the "target" position
            print(operator)
            for i in range(target+1, l):    # fill in the rest with I
                operator = np.kron(operator, np.identity(d))

        """ Applies operator matrix to the register """

        self.register = operator@self.register


    # TODO adapt this gate to our new method
    def c_rotation_k(self, control, target, k, inverse = 1):
        #state = np.where(abs(qdit_control.total) > 0.001)[0][0]
        d = self.dimension
        aux_phase = np.zeros(d, dtype = complex)
        # for k in range(d):
        #     for n in range(d):
        #         aux_phase = *np.exp(2*np.pi*j*inverse/d**k)
        self.refresh(self.qudit_list)



q1 = qudit(2,[0,1,0])
q2 = qudit(2,[1,0,0])
#q3 = qudit(4,[1,0,0,0])

r1 = register([q1,q2])
print('hadamard')
r1.hadamard(0)
print(r1.register)
#print("{}".format(r1.register.round(decimals=3)))
#print("{}".format([r1.qudit_list[i].amp.round(decimals = 3) for i in range(3)]))

