# coding: utf-8
"""
The sphere problem.
"""
import json
import os
import sys

import numpy as np


def sphere(x, z):
    return np.sum((x - z)**2)


def main():
    optima = np.array(json.loads(os.getenv('SPHERE_OPTIMA', '0.0')))
    variable = np.array(json.loads(sys.argv[1]))
    objective = sphere(variable, optima)
    print('{objective: %s}' % objective)


if __name__ == '__main__':
    main()
