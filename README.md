# Python PointSet Class
This package includes a class for handling point-coordinates and their datum using EPSG codes. For datum transformations, this package makes use of the `PyProj` package. It meant to simplify coordinate transformations between EPSG codes.

# Installation
```Console
python3 -m pip install pointset
```

# Usage
The `PointSet` class wraps `pyproj` in order to allow coordinate transformations. In the following, the functionality of the class is explained.

## PointSet with Datum information
In the example above we just generated random positions without any datum information. However the main feature of this class is datum transformations.

First, we define some points in UTM 32N (EPSG: 25832)
```python
xyz_utm = np.array(
    [
        [364938.4000, 5621690.5000, 110.0000],
        [364895.2146, 5621150.5605, 107.4668],
        [364834.6853, 5621114.0750, 108.1602],
        [364783.4349, 5621127.6695, 108.2684],
        [364793.5793, 5621220.9659, 108.1232],
        [364868.9891, 5621310.2283, 107.9929],
        [364937.1665, 5621232.2154, 107.9581],
        [364919.0140, 5621153.6880, 107.8130],
        [364906.8750, 5621199.2600, 108.0610],
        [364951.9350, 5621243.4890, 106.9560],
        [364992.5600, 5621229.7440, 106.7330],
        [365003.7740, 5621203.8200, 106.7760],
        [364987.8850, 5621179.5160, 107.8890],
        [364950.1180, 5621148.5770, 107.9120],
    ]
)

utm_point_set = PointSet(xyz=xyz_utm, epsg=25832)
```
transform point set to another EPSG:
```python
utm_point_set.to_epsg(4936)
print(utm_point_set.mean())
```
Output:
```console
EPSG: 4936
Coordinates:
[[4014743.91215813  499064.14065106 4914468.86763503]]
```
As you can see, the coordinates are now given in a global cartesian frame (EPSG: 4936).
## Local Coordinate Frame
You can transform the coordinates of a pointset in a local ellipsoidal
coordinate frame tangential to the GRS80 ellipsoid for local investigations
using `.to_local()` or `.to_epsg(0)`
```python
utm_point_set.to_local()
print(utm_point_set.mean())
```
Output:
```console
EPSG: 0
Coordinates:
[[-6.15055943e-11 -5.61509442e-10  2.01357074e-10]]
```
Note, that the mean of the PointSet will be zero in local coordinates.
Internally, a `local_transformer` object is created, that takes care of the
transformation to local coordinates.
Especially for comparing PointSets, it might be useful to analyze both
PointSets in the same local coordinate frame. You can do this by setting the
`local_transformer` variable either during instance creation or later:
```python
point_set.local_transformer = utm_point_set.local_transformer
point_set = PointSet(xyz=xyz, epsg=0, local_transformer=utm_point_set.local_transformer)
```
Now, the newly created pointset has the same datum
information as the utm-coordinates.

## PointSet without Datum information

Define PointSet with random numbers

```python 
from pointset import PointSet

xyz = np.random.randn(10000, 3) * 20
point_set = PointSet(xyz=xyz)
```
print the point set to see the EPSG code and the coordinates:
```python 
print(point_set)
```
Output (for example):
```console
EPSG: 0
Coordinates:
[[  2.61185114  26.86022378  24.16762049]
 [-13.10880044  -0.59031669  25.03318095]
 [ 11.7225511   -8.60815889   8.14436657]
 ...
 [  2.92442258 -24.89119898  -2.17729086]
 [  1.45229968  24.66663312  21.73038683]
 [ 15.90327212  28.88909949   4.56549931]]
```
Because we only provided the numpy array and no other parameters,
this PointSet has no datum information. The positions are assumed
to be in a local unknown frame, which is denoted with an EPSG code
of 0.
Therefore, we will get an error if we try to change the EPSG code to
some global frame, e.g. EPSG: 4937
```python 
try:
    point_set.to_epsg(4937)
except PointSetError as e:
    print(e)
```
Output:
```console
Unable to recover from local frame since definition is unknown!
```
However, we can still do some data operations like computing the mean of
the point_set (which will also be a PointSet):
```python
mean_pos = point_set.mean()
```
We can access the raw values of the PointSet coordinates using `x` `y` `z` or `xyz`
```python
print(f"Mean: {mean_pos.xyz}, x = {mean_pos.x:.3f}, y = {mean_pos.y:.3f}, z = {mean_pos.z:.3f}")
```
Output:
```console
Mean: [[-0.03867169  0.21157332  0.0836462 ]], x = -0.039, y = 0.212, z = 0.084
```
It also possible to change the values in this way:
```python
mean_pos.y = 10
print(f"Changed y-value to: {mean_pos.y:.3f}")
```
Output:
```console
Changed y-value to: 10.000
```
To add / substract two PointSets, use normal operators:
```python
added_point_set = point_set + mean_pos
```

You can create a deep copy of the PointSet using .copy():
```python
copied_point_set = point_set.copy()
```