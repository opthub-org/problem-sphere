#!/bin/env python
# coding: utf-8
"""
The sphere problem.
"""
import json
import logging
from os import path

import click
from jsonschema import validate, ValidationError
import numpy as np


_logger = logging.getLogger(__name__)


optima_jsonschema = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Optima of Sphere function",
  "type": "array",
  "minItems": 1,
  "items": {
    "type": "array",
    "minItems": 1,
    "items": {
      "type": "number"
    }
  }
}"""

variable_jsonschema = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Variable of Sphere function",
  "type": "array",
  "minItems": %d,
  "maxItems": %d,
  "items": {
    "type": "number"
  }
}"""


def load_config(ctx, value):
    """Load `ctx.default_map` from a file.

    :param ctx: Click context
    :param value: File name
    :return dict: Loaded config
    """
    if not path.exists(value):
        return {}
    with open(value) as f:
        ctx.default_map = yaml.safe_load(f)
    return ctx.default_map


def sphere(x, z):
    return np.sum((x - z)**2, axis=1).tolist()


@click.command(help='Sphere function minimization problem.')
@click.option('-o', '--optima', default='[[0]]', help='Sphere function minimization problem.')
@click.option('-q', '--quiet', count=True, help='Be quieter.')
@click.option('-v', '--verbose', count=True, help='Be more verbose.')
@click.option('-c', '--config',
              type=click.Path(dir_okay=False), default='config.yml',
              is_eager=True, callback=load_config, help='Configuration file.')
@click.version_option('1.0.0')
def main(optima, quiet, verbose, config):
    verbosity = 10 * (quiet - verbose)
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    _logger.info('Log level is set to %d.', log_level)

    optima_json = json.loads(optima)
    validate(optima_json, json.loads(optima_jsonschema))

    optima = np.array(optima_json)
    _logger.debug('optima = %s', optima)
    n_variable = optima.shape[1]

    variable_str = input()
    _logger.debug('input = %s', variable_str)

    variable_json = json.loads(variable_str)
    validate(variable_json, json.loads(variable_jsonschema % (n_variable, n_variable)))
    variable = np.array(variable_json)
    _logger.debug('variable = %s', variable)

    objective = sphere(variable, optima)
    _logger.debug('objective = %s', objective)

    print(json.dumps({'objective': objective}))
    _logger.info('Successfully exit')


if __name__ == '__main__':
    try:
        main(auto_envvar_prefix="SPHERE")  # pylint: disable=no-value-for-parameter
    except Exception as e:
        _logger.error(e)
        print(json.dumps({'objective': None, 'error': str(e)}))
