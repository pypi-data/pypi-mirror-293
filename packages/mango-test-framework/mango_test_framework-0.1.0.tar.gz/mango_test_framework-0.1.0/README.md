# Mango Test
A simple testing framework in python.

HOW TO USE:
Firstly enter the command in your terminal: pip install mango_test_framework
after that go to your python code and type: from mango_test_framework import mangostart, mangoend, summary
This imports the package.
Then you need to wrap the code you want to test inside mangostart() and mangoend()

This is an example:
mangostart()
code = """
x = 1
y = 1
assert x + y == 2
"""
mangoend(code)

*Note that you need to add the variable you have the code you want to test as an argument inside mangoend()*

ENJOY!