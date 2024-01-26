"""
Terminal animation
"""

from os import get_terminal_size
__all__ = [
    'animation'
]
# helper functions   
def animation():
    column, lines = get_terminal_size()
    print('-' * column)