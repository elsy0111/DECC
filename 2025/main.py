import math

e = 0.9

def rad_to_deg(rad):
    deg = rad * 180 / 3.141592653589793
    deg = int(deg * 1000)
    return deg

def after_collision_theta(vz, theta_):
    theta = math.atan((vz * math.cos(theta_) * e) / (vz * math.sin(theta_)))
    return theta - theta_

def simulate(vz, theta_, theta, minus):
    vx = vz * math.sin(theta_)
    vy = vz * math.cos(theta_) * e
    v = (vx ** 2 + vy ** 2) ** 0.5
    L = (v ** 2 * math.sin(2 * theta)) / 9807
    t_end = 2 * v * math.sin(theta) / 9807
    vy_end = abs(vy - 9807 * t_end)
    vx_end = vx
    t_minus = (math.sqrt(vy_end ** 2 + 2 * 9807 * minus) - vy_end) / 9807
    L += vx_end * t_minus
    return L

def search_theta_(vz, L, minus):
    # print("L",L)
    theta_ans = 0
    abs_diff = 100000000
    for i in range(10000):
        theta_deg = 5000 + i * 4
        theta = math.radians(theta_deg / 1000)
        L_ = simulate(vz, theta, after_collision_theta(vz, theta), minus)
        # print("L_",L_, "theta",theta_deg/1000)
        # print("L_",L_, "theta",theta_deg/1000)
        if abs_diff > abs(L - L_):
            # print("L",L,"L_",L_)    
            abs_diff = abs(L - L_)
            theta_ans = theta
    return theta_ans

def main(sn, holes):
    # print(sn)
    # print(holes)
    did = 0
    closest = (10000000, 10000000)
    sec_closest = (10000000, 10000000)
    Tn = -1
    for idx, hole in enumerate(holes):
        if hole[0] != 0:
            continue
        if hole[0] < closest[0] and hole[1] < closest[1]:
            sec_closest = closest
            closest = hole
            Tn = idx + 1
    # print("closest",closest)
    dummy = "1,5000,0,0,0"

    if closest == (10000000, 10000000):
        print(dummy)
        return
    Nu = 1
    Rr = 0
    Wt = 2200
    P = closest[1]
    while did < 21:
        # vz = sqrt(2gx) (mm/s)
        vz = (2 * 9807 * (700 - 20 * did)) ** 0.5
        # print("vz",vz)
        did += 1
        # print("vz",vz)
        if vz == 0:
            print(dummy)
            return
        minus = 20 * did
        theta = search_theta_(vz, P, minus)
        # print(P, end=",")
        # print("L =", simulate(vz, theta, after_collision_theta(vz, theta), minus))
        theta = rad_to_deg(theta)
        # print("theta",rad_to_deg(theta))
        print(Tn,theta,Rr,Nu,Wt,sep=",",end="\n")

    None

if __name__ == '__main__':
    for i in range(1):
        in_ = input().split()
        sn = int(in_[0])
        holes = []
        for j in range(sn):
            holes.append((int(in_[j * 2 + 1]), int(in_[j * 2 + 2])))
        main(sn, holes)
