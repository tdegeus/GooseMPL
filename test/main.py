import unittest
import matplotlib.pyplot as plt
import GooseMPL as gplt
import numpy as np


class Test_fit_powerlaw(unittest.TestCase):

    def test_prefactor_exponent(self):

        x = np.linspace(0, 1, 1000)
        y = 1.2 * x ** 3.4
        prefactor, exponent = gplt.fit_powerlaw(x, y)
        self.assertTrue(np.isclose(prefactor, 1.2))
        self.assertTrue(np.isclose(exponent, 3.4))

    def test_prefactor(self):

        x = np.linspace(0, 1, 1000)
        y = 1.2 * x ** 3.4
        prefactor, exponent = gplt.fit_powerlaw(x, y, exponent=3.4)
        self.assertTrue(np.isclose(prefactor, 1.2))
        self.assertTrue(np.isclose(exponent, 3.4))

    def test_exponent(self):

        x = np.linspace(0, 1, 1000)
        y = 1.2 * x ** 3.4
        prefactor, exponent = gplt.fit_powerlaw(x, y, prefactor=1.2)
        self.assertTrue(np.isclose(prefactor, 1.2))
        self.assertTrue(np.isclose(exponent, 3.4))


if __name__ == '__main__':

    unittest.main()
