#!/usr/bin/python3
import os
from unittest import TestLoader, result
from unittest.mock import patch
import console
from console import HBNBCommand
import pep8
import io
import inspect
import unittest
from models import storage
from models.user import User
import sys
"""
 Unitest for console
"""


class TestHBNBCommand(unittest.TestCase):
    """
    class for testing HBNBCommand class' methods
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class method for the doc tests
        """
        cls.cmd_func = inspect.getmembers(HBNBCommand, inspect.isfunction)
        cls.HBNB = HBNBCommand()
        cls.id_holder = 0
        cls.test_command = ""

        try:
            os.rename("file.json", "temp.json")
        except Exception:
            print("file not found!")
            return

    @classmethod
    def tearDownClass(cls):
        """
        Tear down class method runnings
        """
        os.rename("temp.json", "file.json")
        del cls.HBNB

    def test_pep8_conformance_HBNBCommand(self):
        """
        Test that console.py file conform to PEP8
        """
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_HBNBCommand(self):
        """
        Test that test_console.py file conform to PEP8
        """
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """
        Tests if module docstring documentation exist
        """
        self.assertTrue(len(console.__doc__) >= 1)

    def test_class_docstring(self):
        """
        Tests if class docstring documentation exist
        """
        self.assertTrue(len(self.HBNB.__doc__) >= 1)

    def test_func_docstring(self):
        """
        Test each function in console class for documentation
        """
        for func in self.cmd_func:
            if type(func[1].__name__) == "function":
                self.assertTrue(len(func[1].__doc__) >= 1)

    def test_empty_line(self):
        """
        Tests for when an empty line is passed
        """
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.HBNB.onecmd("\n")
            self.assertEqual("", f.getvalue())

    def test_EOF_command(self):
        """
        Tests for what an EOF cmd is passed
        """
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.assertTrue(self.HBNB.onecmd("EOF"))

    def test_quit(self):
        """
        Test for when quit command is passed
        """
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.HBNB.onecmd("quit")
            self.assertEqual("", f.getvalue())

    def test_create(self):
        """
        Test creating a new class instance
        """
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "create User"
            self.HBNB.onecmd(self.test_command)
            self.id_holder = f.getvalue().strip('\n')
            self.assertEqual(36, len(self.id_holder))
        return(self.id_holder)

    def test_count(self):
        """
        Test the count method for number of objects of a
        particular model type  in file storage
        """
        self.id_holder = self.test_create()
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "count User"
            self.HBNB.onecmd(self.test_command)
            result = f.getvalue().rstrip('\n')
            self.assertEqual('3', result)
            return True

    def test_show(self):
        """
        Test the show method to show the string representation of
        a particular instance
        """
        self.id_holder = self.test_create()
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "show User {}".format(self.id_holder)
            self.HBNB.onecmd(self.test_command)
            partial_response = "[User] ({}) "\
                .format(self.id_holder)
            full_response = f.getvalue().rstrip('\n')
            self.assertIn(partial_response, full_response)

        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "show User {}3".format(self.id_holder)
            self.HBNB.onecmd(self.test_command)
            response = "** no instance found **"
            full_response = f.getvalue().rstrip('\n')
            self.assertEqual("** no instance found **", full_response)

    def test_destroy(self):
        """
        Test that an existing instance of a class
        is destroyed
        """
        self.id_holder = self.test_create()
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "destroy User {}".format(self.id_holder)
            self.HBNB.onecmd(self.test_command)
            response = f.getvalue().rstrip('\n')
            self.assertEqual("", response)

        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "destroy User {}5".format(self.id_holder)
            self.HBNB.onecmd(self.test_command)
            response = f.getvalue().rstrip('\n')
            self.assertEqual("** no instance found **", response)

    def test_all(self):
        """
        Test that the the all method prints a list of
        all instances belonging to a particular class
        if class exists.
        """
        result = 0
        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "all User"
            self.HBNB.onecmd(self.test_command)
            response = eval(f.getvalue().rstrip('\n'))
            result = response
            self.assertTrue(len(response) > 0)

        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "all BaseModel"
            self.HBNB.onecmd(self.test_command)
            response = eval(f.getvalue().rstrip('\n'))
            self.assertTrue(len(response) == 0)

        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "all Base"
            self.HBNB.onecmd(self.test_command)
            response = f.getvalue().rstrip('\n')
            self.assertEqual("** class doesn't exist **", response)

    def test_update(self):
        """
        Test that updating an instance with a key and a value
        works as expected
        """
        self.id_holder = self.test_create()
        instances_dict = storage.all()
        for key in instances_dict:
            split_key = key.split(".")
            if split_key[0] == "User" and split_key[1] == self.id_holder:
                full_key = key

        instance = User(**instances_dict[full_key].to_dict())

        with patch('sys.stdout', new=io.StringIO()) as f:
            self.test_command = "update User {} name Mary"\
                .format(self.id_holder)
            self.HBNB.onecmd(self.test_command)
            instances_dict = storage.all()
        print(instances_dict.to_dict)
        print(instances_dict[full_key])
        instance = User(**instances_dict[full_key].to_dict())
        instance_json = instance.to_dict()
        print("after", instance_json)


if __name__ == "__main__":
    unittest.main()
