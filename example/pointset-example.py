from matplotlib import pyplot as plt
from pose.pointset import PointSet, PointSetError
import numpy as np


def main():
    # define PointSet with random numbers
    xyz = np.random.randn(10000, 3) * 20
    point_set = PointSet(xyz=xyz)

    # print the point set to see the EPSG code and the coordinates
    print(point_set)

    # because we only provided the numpy array and no other parameters,
    # this PointSet has no datum information. The positions are assumed
    # to be in a local unknown frame, which is denoted with an EPSG code
    # of 0.
    # Therefore, we will get an error if we try to change the EPSG code to
    # some global frame, e.g. EPSG: 4937
    try:
        point_set.to_epsg(4937)
    except PointSetError as e:
        print(e)

    # However, we can still do some data operations like computing the mean of
    # the point_set (which will also be a PointSet):
    mean_pos = point_set.mean()

    # We can access the raw values of the PointSet coordinates using `x` `y` `z` or `xyz`
    print(f"Mean: {mean_pos.xyz}, x = {mean_pos.x:.3f}, y = {mean_pos.y:.3f}, z = {mean_pos.z:.3f}")

    # It also possible to change the values in this way:
    mean_pos.y = 10
    print(f"Changed y-value to: {mean_pos.y:.3f}")

    # To add / substract two PointSets, use normal operators:
    added_point_set = point_set + mean_pos

    # You can create a deep copy of the PointSet using .copy():
    copied_point_set = point_set.copy()

    ## PointSet with Datum information
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

    # transform point set to another EPSG:
    utm_point_set.to_epsg(4936)
    print(utm_point_set.mean())

    ## Local Coordinate Frame
    # You can transform the coordinates of a pointset in a local ellipsoidal
    # coordinate frame tangential to the GRS80 ellipsoid for local investigations
    # using ".to_local()" or ".to_epsg(0)"
    utm_point_set.to_local()
    print(utm_point_set.mean())

    # Note, that the mean of the PointSet will be zero in local coordinates.
    # Internally, a local transformer object is created, that takes care of the
    # transformation to local coordinates.
    # Especially for comparing PointSets, it might be useful to analyze both
    # PointSets in the same local coordinate frame. You can do this by setting the
    # local_transformer variable either during instance creation or later:
    point_set.local_transformer = utm_point_set.local_transformer
    point_set = PointSet(xyz=xyz, epsg=0, local_transformer=utm_point_set.local_transformer)

    # Now, the randomly created points from the beginning have the same datum
    # information as the utm-coordinates. Therefore, we can transform them into
    # any EPSG:
    point_set.to_epsg(25832)

    # if we transform our utm_point_set from local back to utm, we can plot PointSets
    # in UTM
    utm_point_set.to_epsg(25832)

    plt.figure()
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid()
    plt.plot(point_set.x, point_set.y, ".")
    plt.plot(utm_point_set.x, utm_point_set.y, ".r")
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    main()
