import unittest
import os
import sys
import py_compile
from unittest.mock import patch
import io

from pvactools.lib.valid_alleles import ValidAlleles
from tests.utils import *

class ValidAllelesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #locate the bin and test_data directories
        cls.valid_alleles_path = os.path.join(pvactools_directory(), "pvactools", "lib", "valid_alleles.py")

    def module_compiles(self):
        self.assertTrue(py_compile.compile(self.valid_alleles_path))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_alleles_with_algorithm(self, mock_stdout):
        self.assertFalse(ValidAlleles(
            "NetMHCpan",
            "human",
            None
        ).print_valid_alleles())
        self.assertNotIn("DPA", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_alleles_with_species(self, mock_stdout):
        self.assertFalse(ValidAlleles(
            None,
            "mouse",
            None
        ).print_valid_alleles())
        self.assertNotIn("HLA", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_alleles_with_algorithm_and_species(self, mock_stdout):
        self.assertFalse(ValidAlleles(
            "NetMHC",
            "mouse",
            None
        ).print_valid_alleles())
        self.assertIn("H-2-Db", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_alleles_with_length(self, mock_stdout):
        self.assertFalse(ValidAlleles(
            None,
            "human",
            8
        ).print_valid_alleles())
        self.assertIn("HLA", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_alleles_with_algorithm_and_length(self, mock_stdout):
        self.assertFalse(ValidAlleles(
            "NetMHCpan",
            "human",
            8
        ).print_valid_alleles())
        self.assertIn("HLA", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_alleles_with_species_and_length(self, mock_stdout):
        self.assertFalse(ValidAlleles(
            None,
            "mouse",
            8
        ).print_valid_alleles())
        self.assertIn("H-2-Db", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_valid_alleles_with_algorithm_and_species_and_length(self, mock_stdout):
        self.assertFalse(ValidAlleles(
            "NetMHC",
            "mouse",
            8
        ).print_valid_alleles())
        self.assertIn("H-2-Db", mock_stdout.getvalue())
