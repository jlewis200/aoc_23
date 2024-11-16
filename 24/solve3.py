#!/usr/bin/env python3

import re
from z3 import *


def read_file(filename):
    with open(filename, encoding="utf-8") as f_in:
        return f_in.readlines()


def parse(lines):

    pairs = []

    for line in lines:
        x0, y0, z0, x1, y1, z1 = map(int, re.split("[,@]", line))
        pairs.append(((x0, y0, z0), (x1, y1, z1)))

    return pairs


def solve(balls, min_val, max_val):
    """
    This is essentially a system of linear equations.

    Let snow balls be represented by matrix B_0, B_1, etc...
    Let rock be represented by R.
    Let t be a vector with a bias of 1 for starting position and time element.
    
    B_0 = x_0 vx_0
          y_0 vy_0
          z_0 vz_0

    R   = x_r vx_r
          y_r vy_r
          z_r vz_r

    t   = 1
          time_steps

    To get future position of a snowball/rock

    B_0_prime = B_0 @ t
    R_prime   = R   @ t

    The impact of snowball_0 and rock will occur at t_0.  At this point they
    share the same coordinates.

    B_0 @ t_0 = R @ t

    Expanding this out it provides 3 equations

    x_0 + vx_0 * t_0 = x_r + vx_r * t_0
    y_0 + vy_0 * t_0 = y_r + vy_r * t_0
    z_0 + vz_0 * t_0 = z_r + vz_r * t_0
   
    In this one set there are 7 unknowns, 6 for the rock and the impact time t_0

    Repeating this for 300 rocks gives 
    - 900 equations
    - 6 unknowns for the rock
    - 300 unknowns for impact times

    Which is sufficient for solving

    Note:  solver alg for z3 Int type takes too long, but solver alg for z3 Real
    type is fast enough.
    """
    times = [Real(f"t_{idx}") for idx in range(len(balls))]
    rock = ((Real("x"), Real("y"), Real("z")), (Real("vx"), Real("vy"), Real("vz")))
    solver = Solver()

    for ball, time in zip(balls, times):
        ball_prime = get_future(ball, time)
        rock_prime = get_future(rock, time)
        solver.add(ball_prime[0] == rock_prime[0])
        solver.add(ball_prime[1] == rock_prime[1])
        solver.add(ball_prime[2] == rock_prime[2])

    print(solver.check()) 

    model = solver.model()
    x = model[rock[0][0]].as_long()
    y = model[rock[0][1]].as_long()
    z = model[rock[0][2]].as_long()

    print(x)
    print(y)
    print(z)
    print(x + y + z)

    
def get_future(ball, t):
    """
    Get the future position of a snowball/rock.
    """
    (x, y, z), (vx, vy, vz) = ball
    return x + vx * t, y + vy * t, z + vz * t


def main(filename="input.txt", min_val=7, max_val=27):
    print(solve(parse(read_file(filename)), min_val, max_val)})


if __name__ == "__main__":
    main("test.txt", 7, 27)
    main(min_val=200000000000000, max_val=400000000000000)
