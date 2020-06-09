import numpy as np
from scipy.sparse import dia_matrix

j = complex(0,1)

def h_matrix(d):
    """
    :param d: dimension of the target qudit
    :return: complex matrix representing the d-dimensional Hadamard gate
    """

    matrix = np.zeros([d, d], dtype=complex)

    for i in range(d):
        for k in range(d):
            matrix[i][k] = (1/np.sqrt(d))*np.exp(2*np.pi*j*i*k/d)   # Hadamard is nothing more than a Vandermonde matrix :)

    return matrix

def r_matrix(d, angle):
    """
    :param d: dimension of the target qudit
    :param angle: angle assigned to the rotation operator
    :return: complex matrix representing the d-dimensional Rotation gate for a given angle
    """
    matrix = np.zeros([d, d], dtype=complex)

    for i in range(d):
        matrix[i][i] = np.exp(angle*j*i)    # Rotation is given in function of the qudit state "i" and the angle

    return matrix

def r_k_matrix(d, k):
    """
    :param d: dimension of the target qudit
    :param k: parameter used in phase estimation algorithms - defines upon which "decimal" digit the rotation will act
    :return: complex matrix representing the d-dimensional R_k gate
    """
    matrix = np.zeros([d, d], dtype=complex)

    for i in range(d):
        matrix[i][i] = np.exp(2*np.pi*j*i/(d**k))   # Specific rotation used in phase estimation

    return matrix

def not_matrix(d):
    """
    :param d: dimension of the target qudit
    :return: generalised NOT gate. In the d-dimensional case, this generalisation can be seen, in the
    computational base, as adding +1 to the qudits current value (ex: NOT|2> = |3>)
    """

    ones = np.ones(d-1)
    data = np.array([ones])
    offsets = np.array([-1])
    matrix = dia_matrix((data, offsets), shape=(d, d)).toarray()    # defines a matrix with an offset diagonal of 1s

    matrix[0][d-1] = 1  # The 1 that loops the highest state to the lowest (ex: in ternary, NOT|2> = |0>)

    return matrix
