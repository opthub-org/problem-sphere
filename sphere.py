# coding: utf-8
"""
The sphere problem.
"""
import json
import os
import sys
import logging

import numpy as np


_logger = logging.getLogger(__name__)


def sphere(x, z):
    return np.sum((x - z)**2).tolist()


def main():
    verbosity = 0
    if len(sys.argv) > 1:
        for c in sys.argv[1]:
            verbosity += -10 if c == 'v' else 10 if c == 'q' else 0
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    _logger.info('Log level is set to %d.', log_level)

    try:
        optima = np.array(json.loads(os.getenv('SPHERE_OPTIMA', '0.0')))
        _logger.debug('optima = %s', optima)

        x = input()
        _logger.debug('input = %s', x)

        variable = np.array(json.loads(x))
        _logger.debug('variable = %s', variable)

        objective = sphere(variable, optima)
        _logger.debug('objective = %s', objective)
        constraint = 0
    except Exception as e:
        _logger.error(e)
        constraint = 1

    print(json.dumps({'objective': objective, 'constraint': constraint}))


if __name__ == '__main__':
    main()
