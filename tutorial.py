__author__ = 'markcial'

from libs import Slide, Tutor

slides = [
    Slide(
"""Types in python
===============
Everything in python has a type, the philosophy behind python is that everything
in the python codebase is a "first class citizen", everything is able to be
overriden, metaprogrammed, extended or patched."""
    ),
    Slide(
        """Working with types
==================
When you check the type of a number you will get the following output `<type 'int'>`
>>> type(1)"""
    )
]

tutor = Tutor(slides)
tutor.interact()