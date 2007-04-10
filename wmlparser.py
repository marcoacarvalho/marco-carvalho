#!/bin/env python
# -*- coding: latin-1 -*-

import sys
import urllib
import sgmllib
import re

class wmlParser(sgmllib.SGMLParser):

    istag = False
    text = ''

    def start_p(self, attrs):
         self.istag = True

    def end_p(self):
        self.istag = False

    def handle_data(self, data):
        if self.istag:
            self.text = self.text+data
        else:
            self.text = self.text+data

def main():
    file = open("dsa-1022.wml")
    p = wmlParser()
    p.feed(file.read())
    print p.text
    p.close()

if __name__ == "__main__":
    main()
