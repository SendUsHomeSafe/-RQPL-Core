import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from relativity.relativity import (
    C_LIGHT,
    G_CONST,
    einstein_field_equation,
    gravitational_force,
    is_timelike_interval,
    lorentz_factor,
    relativistic_energy,
    rest_energy,
    spacetime_interval,
    time_dilation,
)


class TestRelativityPhysics(unittest.TestCase):

    def test_lorentz_factor_at_rest(self):
        self.assertAlmostEqual(lorentz_factor(0.0), 1.0)

    def test_time_dilation_matches_gamma(self):
        proper_time = 1.0
        v = 0.6 * C_LIGHT
        gamma = lorentz_factor(v)
        self.assertAlmostEqual(time_dilation(proper_time, v), gamma)

    def test_rest_energy_mass_equivalence(self):
        mass = 1.0
        expected = mass * C_LIGHT ** 2
        self.assertAlmostEqual(rest_energy(mass), expected)

    def test_relativistic_energy_greater_than_rest(self):
        mass = 1.0
        v = 0.5 * C_LIGHT
        self.assertGreater(relativistic_energy(mass, v), rest_energy(mass))

    def test_gravitational_force_inverse_square(self):
        m1 = 5.0
        m2 = 10.0
        r = 2.0
        expected = G_CONST * m1 * m2 / r ** 2
        self.assertAlmostEqual(gravitational_force(m1, m2, r), expected)

    def test_spacetime_interval_timelike(self):
        self.assertTrue(is_timelike_interval(1.0, 100.0, 0.0, 0.0))

    def test_einstein_field_equation_string(self):
        self.assertIn("G_{μν}", einstein_field_equation())

    def test_documentation_mentions_relativity_formulas(self):
        readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))
        with open(readme_path, "r", encoding="utf-8") as handle:
            contents = handle.read()

        self.assertIn("Lorentz factor", contents)
        self.assertIn("E = m c^2", contents)
        self.assertIn("F = G m1 m2 / r^2", contents)
        self.assertIn("c^2 dt^2 - dx^2 - dy^2 - dz^2", contents)
        self.assertIn("G_{μν}", contents)
