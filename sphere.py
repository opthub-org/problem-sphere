#!/bin/env python
"""
The multiobjective unconstrained sphere problem.

minimize f_1(x_1, ..., x_n), ..., f_m(x_1, ..., x_n)
where f_i(x) = ||x - z_i||^2
"""
import json
import logging
from os import path
from traceback import format_exc

import click
from jsonschema import validate
import numpy as np
import yaml


LOGGER = logging.getLogger(__name__)

OPTIMA_JSONSCHEMA = """{
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

VARIABLE_JSONSCHEMA_1D = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Variable of Sphere function",
  "type": "number"
}"""
VARIABLE_JSONSCHEMA_ND = """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Variable of Sphere function",
  "type": "array",
  "minItems": {0},
  "maxItems": {0},
  "items": {
    "type": "number"
  }
}"""


def variable_jsonschema(dim: int):
    """Return a JSON schema for n-design variable.

    :param dim: dimension
    :return str: JSON schema
    """
    return VARIABLE_JSONSCHEMA_1D if dim == 1 else VARIABLE_JSONSCHEMA_ND.format(dim)


def load_config(ctx: click.Context, value: str):
    """Load `ctx.default_map` from a file.

    :param ctx: Click context
    :param value: File name
    :return dict: Loaded config
    """
    if not path.exists(value):
        return {}
    with open(value, encoding="utf-8") as file:
        ctx.default_map = yaml.safe_load(file)
        if not isinstance(ctx.default_map, dict):
            raise TypeError(f"The content of `{value}` must be dict, but {type(ctx.default_map)}.")
    return ctx.default_map


def json_list(ctx, param, value):
    """Load a list from a JSON string.

    :param value: JSON string
    :return list: Loaded list
    """
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, list):
        ctx.fail(
            f"Invalid option: {param.name}={value}, which must be list or str."
        )
    return value


def sphere(variable, optima):
    """Calculate the value of multiobjective sphere function.

    :param variable: design variables
    :param optima: optima
    :return list: objective vector
    """
    return np.sum((variable - optima) ** 2, axis=1).tolist()


@click.command(help="Sphere function minimization problem.")
@click.option(
    "-o",
    "--optima",
    callback=json_list,
    default="[[0]]",
    help="Sphere function minimization problem.",
)
@click.option("-q", "--quiet", count=True, help="Be quieter.")
@click.option("-v", "--verbose", count=True, help="Be more verbose.")
@click.option(
    "-c",
    "--config",
    type=click.Path(dir_okay=False),
    default="config.yml",
    is_eager=True,
    callback=load_config,
    help="Configuration file.",
)
@click.version_option("1.0.0")
def main(optima, quiet, verbose, config):  # pylint: disable=unused-argument
    """Evaluate a given solution on a multiobjective unconstrained sphere problem."""
    verbosity = 10 * (quiet - verbose)
    log_level = logging.WARNING + verbosity
    logging.basicConfig(level=log_level)
    LOGGER.info("Log level is set to %d.", log_level)

    LOGGER.info("Validate SPHERE_OPTIMA...")
    validate(optima, json.loads(OPTIMA_JSONSCHEMA))
    LOGGER.info("...Validated")

    optima = np.array(optima)
    LOGGER.debug("optima = %s", optima)
    n_objective, n_variable = optima.shape

    LOGGER.info("Recieve a solution...")
    variable_str = input()
    LOGGER.debug("input = %s", variable_str)
    LOGGER.info("...Recieved")

    LOGGER.info("Parse the solution...")
    variable_json = json.loads(variable_str)
    LOGGER.info("...Parsed")

    LOGGER.info("Validate the solution...")
    validate(variable_json, json.loads(variable_jsonschema(n_variable)))
    LOGGER.info("...Validated")

    variable = np.array(variable_json)
    LOGGER.debug("variable = %s", variable)

    LOGGER.info("Compute sphere function value...")
    objective = sphere(variable, optima)
    LOGGER.debug("objective = %s", objective)
    LOGGER.info("...Computed")

    print(json.dumps({"objective": objective[0] if n_objective == 1 else objective}))


if __name__ == "__main__":
    try:
        LOGGER.info("Start")
        main(  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
            auto_envvar_prefix="SPHERE"
        )
        LOGGER.info("Successfully finished")
    except Exception as e:  # pylint: disable=broad-exception-caught
        LOGGER.error(format_exc())
        print(json.dumps({"objective": None, "error": str(e)}))
