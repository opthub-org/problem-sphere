# Sphere
This problem calculates a sphere function with an arbitrary number of variables and objectives.

## Usage
```
$ echo 2 | ./sphere.py
{"objective": 4}
```

## Environmental Variables
The location of optima can be specified via `SPHERE_OPTIMA` environmental variable, which must be a matrix.

If you need a 1-variable, 1-objective problem with the optimum at the origin (default), then set:
```
SPHERE_OPTIMA=[[0]]
```

If you need a 3-variable, 2-objective problem with `argmin f1=[1, 2, 3]` and `argmin f2=[4, 5, 6]`, then set:
```
SPHERE_OPTIMA="[[1, 2, 3], [4, 5, 6]]"
```
