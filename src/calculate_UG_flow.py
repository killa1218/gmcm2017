from scipy.optimize import minimize as mini
import numpy as np
import time
import pickle as pk
from algopy import UTPM

np.random.seed(int(time.time()))

CONGEST_THRESHOLD = 4

toy = ''
print('new')

congesData = np.loadtxt('../data/conges{}.txt'.format(toy))

congestion = congesData[:, 0]
flow_quan = congesData[:, 1]

city_num = len(flow_quan)
campus_num = 4
total_num = city_num + campus_num

conges_ratio = np.concatenate((np.zeros(campus_num), congestion / flow_quan)) # congestion per ton goods

ug_flow_ub = np.loadtxt('../data/od{}.txt'.format(toy)) # upper bond
ug_flow_lb = np.zeros_like(ug_flow_ub) # lower bond

rand = np.random.random(size = ug_flow_ub.shape)

ug_flow = ug_flow_ub * rand

def from_campus(xx):
    xx = xx.reshape((total_num, total_num))

    # return -(xx[:4, :].sum() + xx[:, :4].sum())
    return -(xx[0][98] + xx[1][61] + xx[2][13] + xx[3][98] + xx[98][0] + xx[61][1] + xx[13][2] + xx[98][3])
    # return -xx[0, :].sum()

def get_jac(xx):
    return UTPM.extract_jacobian(from_campus(xx))

def ineq(xx):
    xx = xx.reshape((total_num, total_num))
    to = (ug_flow_ub - xx).sum(0)
    fm = (ug_flow_ub - xx).sum(1)
    total_ag = to + fm
    congest = total_ag * conges_ratio
    return CONGEST_THRESHOLD - congest

print(ineq(ug_flow))

start_time = time.time()

res = mini(
    fun = from_campus,
    x0 = ug_flow,
    bounds = list(zip(ug_flow_lb.reshape(total_num**2), ug_flow_ub.reshape(total_num**2))),
    constraints = {
        'type': 'ineq',
        'fun': ineq
    },
    # jac = get_jac,
    options = {'disp': True},
    method = 'SLSQP'
)

end_time = time.time()

print('Time used: {:.2f}'.format(end_time - start_time))

np.save('../data/ug_flow{}.txt'.format(toy), res.x.reshape((total_num, total_num)))
pk.dump(res, open('../data/res{}.pkl'.format(toy), 'wb'))

print(res.x.reshape((total_num, total_num)))
print(ineq(res.x))
