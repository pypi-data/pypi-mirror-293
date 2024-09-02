import numpy as np

__version__ = '0.0.1'

def getB(origin_H, origin_B, h):
    H_limit, B_limit = origin_H, origin_B
    H_down = H_limit[:np.argmin(H_limit)]
    B_down = B_limit[:np.argmin(H_limit)]
    H_up = H_limit[np.argmin(H_limit):]
    B_up = B_limit[np.argmin(H_limit):]
    def Bd(H):
        for i in range(len(H_down)-1):
            if H > H_down[i]:
                return (B_down[i+1]-B_down[i])*(H-H_down[i])/(H_down[i+1]-H_down[i])+B_down[i]
        return B_down[-1]
    def Bu(H):
        for i in range(len(H_up)-1):
            if H < H_up[i+1]:
                return (B_up[i+1]-B_up[i])*(H-H_up[i])/(H_up[i+1]-H_up[i])+B_up[i]
        return B_up[-1]
    def F(H):
        if H >= 0:
            return (Bd(H)-Bu(H))/2/np.sqrt(Bd(H))
        else:
            return np.sqrt(Bd(-H))
    def T(alpha, beta):
        return (Bu(alpha) - Bd(beta))/2 + F(alpha) * F(-beta)
    b = np.zeros(h.shape[0])
    b[0] = T(h[0], -h[0])
    hStack = [[h[0], -h[0]]]
    bStack = [b[0]]
    last_state = 1
    for i in range(1, h.shape[0]):
        now_state = h[i] - h[i - 1]
        if now_state * last_state > 0:
            if now_state > 0:
                if h[i] > hStack[0][0]:
                    hStack = [[h[i], -h[i]]]
                    b[i] = T(h[i], -h[i])
                    bStack = [b[i]]
            if now_state < 0:
                if h[i] < hStack[0][1]:
                    hStack = [[-h[i], h[i]]]
                    b[i] = -T(-h[i], h[i])
                    bStack = [b[i]]
        else:
            if now_state > 0:
                hStack.append([h[i], h[i-1]])
            else:
                hStack.append([h[i - 1], h[i]])
            bStack.append(b[i-1])
        if now_state < 0:
            b[i] = bStack[-1] - 2 * T(hStack[-1][0], h[i])
        if now_state > 0:
            b[i] = bStack[-1] + 2 * T(h[i], hStack[-1][1])
        last_state = now_state
    return b
