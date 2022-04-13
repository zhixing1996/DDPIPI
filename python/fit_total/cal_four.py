from tools.phi_n import PhiN
import sys, os

m1 = 0.13957
m2 = 0.13957
m3 = 1.86965
m4 = 1.86965
m_4 = [m1, m2, m3, m4]

step = 0.001
Mup = 5.
N_it_four = int((Mup - m1 - m2 - m3 - m4)/step)
ss_four = [(m1 + m2 + m3 + m4 + i * step) for i in range(N_it_four)]
ps_four = []
for s in ss_four[1:]:
    ps = PhiN(s*s, 4, m_4)
    ps_four.append(ps)
    print('{}/{} is done'.format(s, ss_four[-1]))

if not os.path.exists('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/'):
    os.makedirs('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/')

with open('/scratchfs/bes/jingmq/bes/DDPIPI/v0.2/run/ana/fit/four_body_phase_space.txt', 'w') as f:
    for s, ps in zip(ss_four, ps_four):
        f.write(str(s) + ' ' + str(ps) + '\n')
