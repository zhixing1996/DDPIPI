from math import sqrt, pi

def L(x, y, z):
    return pow(x, 2) + pow(y, 2) + pow(z, 2) - 2 * x * y - 2 * x * z - 2 * y * z

def Phi2(s, m):
    if L(s, m[0]**2, m[1]**2) < 0: return 0
    return pi * pow(2 * s, -1) * sqrt(L(s, m[0]**2, m[1]**2))

def PhiN(s, N, m):
    if N == 2:
        return Phi2(s, m)
    if N > 2:
        m_n = m[-1]
        sprime_low = (sum(m[:-1]))**2
        sprime_up = (sqrt(s) - m_n)**2
        step = 0.0002
        N_split = int((sprime_up - sprime_low)/step)
        sprime = [sprime_low + i * step for i in range(N_split)]
        return pow(16 * pi**2 * s, -1) * sum([sqrt(L(s, sp, m_n**2)) * PhiN(sp, N - 1, m[:-1]) * step for sp in sprime])
