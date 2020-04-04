import re

class Game(object):

    def __init__(self, * name):
        self.name = name
    
    def strip_tags(self, html):
        regex = re.compile(r'<[^>]+>')
        return regex.sub('', html)
