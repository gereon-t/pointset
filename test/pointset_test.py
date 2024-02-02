import numpy as np
import unittest
from pointset import PointSet, PointSetError


class TestPointSet(unittest.TestCase):
    """
    TestCase class to test pointset
    """

    @classmethod
    def setUpClass(cls):
        """
        Sorting is slow so only run once
        """
        super(TestPointSet, cls).setUpClass()

        cls.local_point = PointSet(xyz=np.array([1, 2, 3]), epsg=0)

        cls.single_point = PointSet(xyz=np.array([4025252.71577, 493815.41256, 4906612.94912]), epsg=4936)

        multi_point = np.array([4025252.71577, 493815.41256, 4906612.94912]) + np.random.rand(100, 3) * 100
        cls.multi_point = PointSet(xyz=multi_point, epsg=4936)

    def test_single_point_transformation(self):
        start_p = self.single_point.copy()
        self.single_point.to_epsg(25832)
        self.single_point.to_epsg(4937)
        self.single_point.to_epsg(4936)
        self.single_point.to_epsg(0)
        self.single_point.to_local()
        self.single_point.to_epsg(4936)
        np.testing.assert_allclose(start_p.xyz, self.single_point.xyz)

    def test_multi_point_transformation(self):
        start_p = self.multi_point.copy()
        self.multi_point.to_epsg(25832)
        self.multi_point.to_epsg(4937)
        self.multi_point.to_epsg(4936)
        self.multi_point.to_epsg(0)
        self.multi_point.to_local()
        self.multi_point.to_epsg(4936)
        np.testing.assert_allclose(start_p.xyz, self.multi_point.xyz)

    def test_local_error(self):
        with self.assertRaises(PointSetError):
            self.local_point.to_epsg(25832)

    def test_mean(self):
        manual_mean = np.mean(self.multi_point.xyz, axis=0)
        p_mean = self.multi_point.copy()
        p_mean.mean(inplace=True)
        np.testing.assert_allclose(p_mean.xyz[0], manual_mean)
        np.testing.assert_allclose(
            manual_mean,
            self.multi_point.mean().xyz[0],
        )

    def test_setter(self):
        p1 = PointSet(xyz=np.array([1, 2, 3]))
        p1.x = 2
        self.assertEqual(p1.x, 2)

        p1.xyz = self.multi_point.xyz
        p1.x = self.multi_point.x
        p1.y = self.multi_point.y
        p1.z = self.multi_point.z

        p1.epsg = self.multi_point.epsg
        p1.local_transformer = self.multi_point.local_transformer
        p1.pipeline_str = self.multi_point.pipeline_str
        self.assertEqual(p1, self.multi_point)

    def test_addition(self):
        p1 = PointSet(xyz=np.array([1, 2, 3]))
        p2 = PointSet(xyz=np.array([1, -2, 3]))
        p3 = PointSet(xyz=np.array([2, 0, 6]))
        self.assertEqual(p3, p1 + p2)

    def test_subtraction(self):
        p1 = PointSet(xyz=np.array([1, 2, 3]))
        p2 = PointSet(xyz=np.array([1, -2, 3]))
        p3 = PointSet(xyz=np.array([0, 4, 0]))
        self.assertEqual(p3, p1 - p2)

    def test_round_to(self):
        p1 = PointSet(xyz=np.array([12345.678, 98765.4321, 12343.678]))
        p1_rounded_1 = PointSet(xyz=np.array([12346.0, 98765.0, 12344.0]))
        p1_rounded_10 = PointSet(xyz=np.array([12350.0, 98770.0, 12340.0]))
        p1_rounded_200 = PointSet(xyz=np.array([12400.0, 98800.0, 12400.0]))

        self.assertEqual(p1.round_to(1), p1_rounded_1)
        self.assertEqual(p1.round_to(10), p1_rounded_10)
        self.assertEqual(p1.round_to(200), p1_rounded_200)

    def test_hash(self):
        p1 = hash(PointSet(xyz=np.array([1, 2, 3])))
        p2 = hash(PointSet(xyz=np.array([1, 2, 3])))

        self.assertEqual(p1, p2)

    def test_equal(self):
        p1 = PointSet(xyz=np.array([1, 2, 3]))
        p2 = PointSet(xyz=np.array([1, 2, 3]))
        p_none = None

        assert p1 == p2

        with self.assertRaises(NotImplementedError):
            p1 == p_none


if __name__ == "__main__":
    unittest.main()
