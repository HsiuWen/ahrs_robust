#!/usr/bin/env python3
import unittest
import numpy as np
import ahrs

class TestQuaternion(unittest.TestCase):
    def setUp(self) -> None:
        self.q0 = ahrs.Quaternion()
        self.vector3 = np.random.random(3)-0.5
        self.vector3 /= np.linalg.norm(self.vector3)
        self.q3 = ahrs.Quaternion(self.vector3)
        self.vector4 = np.random.random(4)-0.5
        self.vector4 /= np.linalg.norm(self.vector4)
        self.q4 = ahrs.Quaternion(self.vector4)
        self.decimal_precision = 15

    def test_identity_quaternion(self):
        self.assertEqual(self.q0.w, 1.0)
        self.assertEqual(self.q0.x, 0.0)
        self.assertEqual(self.q0.y, 0.0)
        self.assertEqual(self.q0.z, 0.0)
        np.testing.assert_equal(self.q0.v, np.zeros(3))

    def test_versor_from_3d_array(self):
        self.assertAlmostEqual(self.q3.w, 0.0, places=self.decimal_precision)
        self.assertAlmostEqual(self.q3.x, self.vector3[0], places=self.decimal_precision)
        self.assertAlmostEqual(self.q3.y, self.vector3[1], places=self.decimal_precision)
        self.assertAlmostEqual(self.q3.z, self.vector3[2], places=self.decimal_precision)
        np.testing.assert_almost_equal(self.q3.v, self.vector3, decimal=self.decimal_precision)

    def test_versor_from_4d_array(self):
        self.assertAlmostEqual(self.q4.w, self.vector4[0], places=self.decimal_precision)
        self.assertAlmostEqual(self.q4.x, self.vector4[1], places=self.decimal_precision)
        self.assertAlmostEqual(self.q4.y, self.vector4[2], places=self.decimal_precision)
        self.assertAlmostEqual(self.q4.z, self.vector4[3], places=self.decimal_precision)
        np.testing.assert_almost_equal(self.q4.v, self.vector4[1:], decimal=self.decimal_precision)

    def test_wrong_input_array(self):
        self.assertRaises(TypeError, ahrs.Quaternion, True)
        self.assertRaises(TypeError, ahrs.Quaternion, 3.0)
        self.assertRaises(TypeError, ahrs.Quaternion, "[1.0, 2.0, 3.0, 4.0]")
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random((6, 3)))
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random((6, 4)))
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random(2))
        self.assertRaises(ValueError, ahrs.Quaternion, np.random.random(2).tolist())
        self.assertRaises(ValueError, ahrs.Quaternion, np.zeros(3))

    def test_wrong_input_dcm(self):
        self.assertRaises(TypeError, ahrs.Quaternion, dcm=3)
        self.assertRaises(TypeError, ahrs.Quaternion, dcm=3.0)
        self.assertRaises(TypeError, ahrs.Quaternion, dcm="np.identity(3)")
        self.assertRaises(ValueError, ahrs.Quaternion, dcm=np.random.random((3, 3)))
        self.assertRaises(ValueError, ahrs.Quaternion, dcm=-np.identity(3))

if __name__ == "__main__":
    unittest.main()
