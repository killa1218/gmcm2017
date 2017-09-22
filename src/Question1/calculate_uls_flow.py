import time
import numpy as np
import pickle as pk

from algopy import UTPM
from scipy.optimize import minimize

np.random.seed(int(time.time()))

CONGEST_THRESHOLD = 4

congesData = np.loadtxt('../../data/conges.txt')
congestion = congesData[:, 0]
flow_quan = congesData[:, 1]
city_num = len(flow_quan)
campus_num = 4
total_num = city_num + campus_num
conges_ratio = np.concatenate((np.zeros(campus_num), congestion / flow_quan)) # congestion per ton goods
uls_flow_ub = np.loadtxt('../../data/od.txt') # upper bond
uls_flow_lb = np.zeros_like(uls_flow_ub) # lower bond
rand = np.random.random(size = uls_flow_ub.shape)
init_uls_flow = uls_flow_ub * rand


def from_campus(xx):
    xx = xx.reshape((total_num, total_num))

    # return -(xx[:4, :].sum() + xx[:, :4].sum())
    return -(xx[0][98] + xx[1][61] + xx[2][13] + xx[3][98] + xx[98][0] + xx[61][1] + xx[13][2] + xx[98][3])
    # return -xx[0, :].sum()


def get_jac(xx):
    return UTPM.extract_jacobian(from_campus(xx))


def ineq(xx):
    xx = xx.reshape((total_num, total_num))
    to = (uls_flow_ub - xx).sum(0)
    fm = (uls_flow_ub - xx).sum(1)
    total_ag = to + fm
    congest = total_ag * conges_ratio

    return CONGEST_THRESHOLD - congest


def calculate():
    print('Congestions using initial uls flow:\n', ineq(init_uls_flow))

    start_time = time.time()

    res = minimize(
        fun = from_campus,
        x0 = init_uls_flow,
        bounds = list(zip(uls_flow_lb.reshape(total_num**2), uls_flow_ub.reshape(total_num**2))),
        constraints = {
            'type': 'ineq',
            'fun': ineq
        },
        # jac = get_jac,
        options = {'disp': True},
        method = 'SLSQP'
    )

    end_time = time.time()

    print('Time used: {:.2f}s'.format(end_time - start_time))

    uls_flow = res.x.reshape((total_num, total_num))
    np.savetxt('../../res/Question1/uls_od.txt', uls_flow)
    # pk.dump(res, open('../../data/res.pkl', 'wb'))

    area_total_uls_flow = (uls_flow.sum(0) + uls_flow.sum(1))[4:]
    np.savetxt('../../res/Question1/area_total_uls_flow.txt', area_total_uls_flow)


    print('ULS flow data saved in ../../res/Question1/uls_od.txt')
    print('Congestions after using ULS:\n', ineq(res.x))
