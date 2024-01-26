"""
Terminal animation
"""

from os import get_terminal_size

# helper functions   
def animation():
    column, lines = get_terminal_size()
    print('-' * column)