import autograd.numpy as np
import scipy
from matplotlib import pyplot as plt

from utils import propagate_error

measured_1 = np.array([0.267, 0.602, 0.802, 1.067, 1.314, 1.604])
measured_2 = np.array([0.758, 1.067, 1.287, 1.562])
measured_1_err = np.array([0.02,0.02,0.02,0.02,0.02,0.02])
measured_2_err = np.array([0.02,0.02,0.02,0.02])

N_arr = np.array([1, 2, 3, 4, 5, 6])
N_arr_2 = np.array([3, 4, 5, 6])
N_arr_err = np.array([0,0,0,0,0,0])

range_1 = np.linspace(1, 6 , 100)
range_2 = np.linspace(3, 6 , 100)

L = .868888888889
L_err = 1e-3
d = 1.27e-2
d_err = 0.01e-2
l = 45.6e-2
l_err = 0.1e-2
F = 0.49
F_err = 0.1e-2
alpha = 0.11
alpha_err = 0.1e-2
m = 21.9e-3
m_err = 1e-3

def get_freq_free(d, F, l, alpha,m,L,N):
    return v_func(d, F, l, alpha,m)*N/(2*L)

def get_freq_held(d, F, l, alpha,m,L,N):
    return v_func(d, F, l, alpha,m)*(2*N-1)/(4*L)

def I_func(m,l):
    return (m*l**2)/12

def v_func(d, F, l, alpha,m):
    return np.sqrt(k_func(F, l, alpha)/I_func(m,l))*d

def k_func(F, l, alpha):
    return F*l/(2*alpha)

theoretical_1 = get_freq_free(d, F, l, alpha,m,L,N_arr)
theoretical_1_err = np.array([1,1,1,1,1,1])
for i in range(6):
    theoretical_1_err[i] = propagate_error(get_freq_free, np.array((d, F, l, alpha,m,L,N_arr[i]))
                                           , np.array((d_err, F_err, l_err, alpha_err, m_err,L_err, 0)))
theoretical_1_err = theoretical_1_err
print((d_err, F_err, l_err, alpha_err, m_err,L_err, 0))
print(theoretical_1_err[0])
reg_1 = scipy.stats.linregress(N_arr, measured_1)

plt.plot(range_1, reg_1.slope*range_1 + reg_1.intercept,'-', label = 'regression')
plt.errorbar(N_arr, measured_1, yerr=measured_1_err, fmt='o', label='Results')
plt.plot(range_1, get_freq_free(d, F, l, alpha,m,L,range_1), '--', label='theoretical graph')
plt.ylabel('Frequency [Hz]')
plt.xlabel('frequency number [A.U.]')
plt.legend()
plt.grid()
plt.savefig("free_end.svg", format="svg")
plt.show()


print(reg_1.rvalue**2)
reg_2 = scipy.stats.linregress(N_arr_2, measured_2)

plt.plot(range_2, reg_2.slope*range_2 + reg_2.intercept,'-', label = 'regression')
plt.errorbar(N_arr_2, measured_2, yerr=measured_2_err, fmt='o', label='Results')
plt.plot(range_2, get_freq_held(d, F, l, alpha,m,L,range_2), '--', label='theoretical graph')
plt.ylabel('Frequency [Hz]')
plt.xlabel('frequency number [A.U.]')
plt.legend()
plt.grid()
plt.savefig("held_end.svg", format="svg")
plt.show()

print(reg_2.rvalue**2)
