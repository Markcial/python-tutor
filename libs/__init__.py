# -.- encoding: utf8 -.-

import re
from abc import ABCMeta
from itertools import repeat
from code import InteractiveConsole


class Navigable(object):
    """
    Navigable object through a collection of items
    """

    __metaclass__ = ABCMeta

    def __init__(self, collection=None):
        self.collection = collection or []
        self.pointer = 0

    @property
    def current(self):
        return self.collection[self.pointer] if len(self.collection) > self.pointer else None

    @property
    def next(self):
        if self.pointer < len(self.collection):
            self.pointer += 1
        return self.current

    @property
    def prev(self):
        if self.pointer > 0:
            self.pointer -= 1
        return self.current


class Completable(Navigable):
    """
    Object that checks for completions through different chapters
    """
    __metaclass__ = ABCMeta

    def __init__(self, collection=None):
        collection = collection or []
        super(Completable, self).__init__(collection)
        self.themes = {a: b for a,b in zip(range(0,len(collection)), repeat(False))}

    def mark_completed(self, which):
        self.themes[which] = True

    def has_completed(self, which):
        return self.themes[which]


class Example(str, InteractiveConsole):
    """
    Embedded examples inside the Slide objects
    """
    def __init__(self, sample=None):
        if sample and not isinstance(sample, basestring):
            raise TypeError('Only null or basestring types allowed as parameter, %s received instead' % type(sample))
        self.sample = sample or ''
        InteractiveConsole.__init__(self)

    """
    function call that interactively executes the code sample
    """
    def execute(self):
        self.runcode(self.sample)

    def __str__(self):
        return self.sample


class Slide(str):
    """
    Slide objects collected inside the chapters objects
    """
    def __init__(self, content=None):
        if content and not isinstance(content, basestring):
            raise TypeError('Only null or basestring types allowed as parameter, %s received instead' % type(content))
        super(Slide, self).__init__(content)
        self.matcher = re.compile(r'^[>\.]{3} (.*)$', re.M)
        self.example = Example("\n".join(self.matcher.findall(self)))

    @property
    def has_example(self):
        return self.example is not None


class Tutor(InteractiveConsole, Completable):
    """
    """

    keywords = [
        'help', 'next', 'prev', 'current', 'example'
    ]

    banner = """
Interactive tutor for python teaching
"""

    usage = """
Write one of the following keywords (current, next, previous, examples)
    """

    def __init__(self, slides):
        map(self.validate, slides)
        InteractiveConsole.__init__(self)
        super(Completable, self).__init__(slides)
        
    def interact(self, banner=None):
        banner = self.banner
        super(Tutor, self).interact(banner)

    def run_current(self):
        print self.current

    def run_next(self):
        print self.next

    def run_prev(self):
        print self.prev

    def run_example(self):
        if self.current.has_example:
            print self.current.example.execute()

    def push(self, line):
        if line in self.keywords:
            cmd = getattr(self, 'run_%s'%line)
            cmd()
        else:
            super(Tutor, self).push(line)

    def raw_input(self, prompt=""):
        example = 'try the sum operator with: [3+4]: '
        
        return super(Tutor, self).raw_input(example)

    @staticmethod
    def validate(slide):
        if not isinstance(slide, Slide):
            raise TypeError('Object received was not of the type Slide, type %s received' % type(slide))
