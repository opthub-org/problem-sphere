# Sphere
The sphere problem with arbitrary dimensions and objectives.

## Usage
```
$ python sphere.py "[1, 2]"
```

## Environmental Variables
The location of optima can be specified via `SPHERE_OPTIMA`, which may be a scalar, a vector or a matrix.

If you need an n-variable, single-objective problem with the optimum at the origin (default), then set:
```
SPHERE_OPTIMA=0
```

If you need a 3-variable, 2-objective problem with `argmin f1=[1, 2, 3]` and `argmin f2=[4, 5, 6]`, then set:
```
SPHERE_OPTIMA="[[1, 2, 3], [4, 5, 6]]"
```
