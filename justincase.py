# def hadamard(self, target):
#     """
#     :param target: position of the qudit to which H is applied - 0 is the most significant digit
#     :return: register array with Hadamard applied
#     TODO: generalize this function for any 1 qudit operation (rotations, NOT)
#
#     """
#     # used to define operator matrix size
#     d = self.dimension
#     l = self.length
#     op_size = self.dimension**self.length
#
#     """
#         Building the operator matrix:
#         If the target qudit is the first in the register, we begin with the basic Hadamard matrix
#         and then multiply by the necessary number of identities: op = H .I.I...I
#     """
#
#     if target == 0:
#         operator = matlib.h_matrix(d)
#         for i in range(1,l):
#             operator = np.kron(operator, np.identity(d))
#     else:
#
#         """ else,  the kronecker multiplication involving H must be made between
#             identities: op = I.I...I. H .I.I...I (kron. prod. non-commutative)"""
#
#         operator = np.identity(d)   # initializes the operator with I
#         for i in range(1, target):  # identity multiplication until target position is reached
#             operator = np.kron(operator, np.identity(d))
#         i = target
#         operator = np.kron(operator, matlib.h_matrix(d))    # multiplying the H matrix at the "target" position
#         print(operator)
#         for i in range(target+1, l):    # fill in the rest with I
#             operator = np.kron(operator, np.identity(d))
#
#     """ Applies operator matrix to the register """
#
#     self.register = operator@self.register




