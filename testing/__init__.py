import unittest
from libs import Example, Slide
import sys
from cStringIO import StringIO
from contextlib import contextmanager

__author__ = 'markcial'


@contextmanager
def capture_out(command, *args, **kwargs):
  out, sys.stdout = sys.stdout, StringIO()
  command(*args, **kwargs)
  sys.stdout.seek(0)
  yield sys.stdout.read()
  sys.stdout = out

@contextmanager
def capture_err(command, *args, **kwargs):
  out, sys.stderr = sys.stderr, StringIO()
  command(*args, **kwargs)
  sys.stderr.seek(0)
  yield sys.stderr.read()
  sys.stderr = out

class TestExamples(unittest.TestCase):

    def test_create_new_empty(self):
        example = Example()
        self.assertEqual('', str(example))

    def test_create_new_with_text(self):
        example = Example('print "foo"')
        self.assertEqual('print "foo"', str(example))

    def test_run_example(self):
        example = Example('print "foo"')
        with capture_out(example.execute) as output:
            self.assertEquals("foo\n", output)

    def test_run_multiline_example(self):
        example = Example("a = 12\nprint a")
        with capture_out(example.execute) as output:
            self.assertEquals("12\n", output)


class TestSlides(unittest.TestCase):

    def test_create_new_empty_slide(self):
        slide = Slide()
        self.assertEqual("", str(slide))

    def test_create_slide_with_wrong_type(self):
        self.assertRaises(TypeError, Slide, [1])

    def test_create_new_slide_with_short_example(self):
        slide = Slide("""
Sample slide with a simple print
================================
>>> print 'hi!'
        """)
        with capture_out(slide.example.execute) as output:
            self.assertEquals("hi!\n", output)

    def test_create_new_slide_with_long_example(self):
        slide = Slide("""
Sample slide with variable assign and print
================================
>>> v = 'hi!'
>>> print v
        """)
        with capture_out(slide.example.execute) as output:
            self.assertEquals("hi!\n", output)

    def test_create_new_slide_with_complex_example(self):
        slide = Slide("""
Sample slide with class creation, instantiation  and print
================================
>>> class Demo:
...     def salute(self):
...         print 'hi from inside demo!'
...
>>> demo = Demo()
>>> demo.salute()
        """)
        with capture_out(slide.example.execute) as output:
            self.assertEquals("hi from inside demo!\n", output)

    def test_slide_with_wrong_example(self):
        slide = Slide("""
Sample slide with wrong example
===============================
>>> class Demo:
>>> a = Demo()
""")
        with capture_err(slide.example.execute) as output:
            self.assertEqual("""  File "<string>", line 2
    a = Demo()
    ^
IndentationError: expected an indented block
""", output)



if __name__ == '__main__':
    unittest.main()