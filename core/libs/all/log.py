#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
from logging import handlers


'''
levels: 'NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
CRITICAL    50
ERROR       40
WARNING     30
INFO        20
DEBUG       10
NOTSET      0
'''

# The color mechanism is taken from Scapy:
# http://www.secdev.org/projects/scapy/
# Thanks to Philippe Biondi for his awesome tool and design.

class Color:
    normal = "\033[0m"
    black = "\033[30m"
    red = "\033[31m"
    green = "\033[32m"
    yellow = "\033[33m"
    blue = "\033[34m"
    purple = "\033[35m"
    cyan = "\033[36m"
    grey = "\033[37m"

    bold = "\033[1m"
    uline = "\033[4m"
    blink = "\033[5m"
    invert = "\033[7m"

class ColorTheme:
    def __repr__(self):
        return "<%s>" % self.__class__.__name__
    def __getattr__(self, attr):
        return lambda x:x

class NoTheme(ColorTheme):
    pass

class AnsiColorTheme(ColorTheme):
    def __getattr__(self, attr):
        if attr.startswith("__"):
            raise AttributeError(attr)
        s = "style_%s" % attr
        if s in self.__class__.__dict__:
            before = getattr(self, s)
            after = self.style_normal
        else:
            before = after = ""

        def do_style(val, fmt=None, before=before, after=after):
            if fmt is None:
                if type(val) is not str:
                    val = str(val)
            else:
                val = fmt % val
            return before+val+after
        return do_style


    style_normal = ""
    style_prompt = "" # '>>>'
    style_punct = ""
    style_id = ""
    style_not_printable = ""
    style_class_name = ""
    style_field_name = ""
    style_field_value = ""
    style_emph_field_name = ""
    style_emph_field_value = ""
    style_watchlist_name = ""
    style_watchlist_type = ""
    style_watchlist_value = ""
    style_fail = ""
    style_success = ""
    style_odd = ""
    style_even = ""
    style_yellow = ""
    style_active = ""
    style_closed = ""
    style_left = ""
    style_right = ""

class BlackAndWhite(AnsiColorTheme):
    pass

class DefaultTheme(AnsiColorTheme):
    style_normal = Color.normal
    style_prompt = Color.blue+Color.bold
    style_punct = Color.normal
    style_id = Color.blue+Color.bold
    style_not_printable = Color.grey
    style_class_name = Color.red+Color.bold
    style_field_name = Color.blue
    style_field_value = Color.purple
    style_emph_field_name = Color.blue+Color.uline+Color.bold
    style_emph_field_value = Color.purple+Color.uline+Color.bold
    style_watchlist_type = Color.blue
    style_watchlist_value = Color.purple
    style_fail = Color.red+Color.bold
    style_success = Color.blue+Color.bold
    style_even = Color.black+Color.bold
    style_odd = Color.black
    style_yellow = Color.yellow
    style_active = Color.black
    style_closed = Color.grey
    style_left = Color.blue+Color.invert
    style_right = Color.red+Color.invert

theme = DefaultTheme()


class Logger:    
    def __init__(self):
        self.file_frmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.stream_frmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        self.logger = logging.getLogger('mylogname')
        self.logger.setLevel(logging.INFO)
        
        # file handler
        #self.fh = logging.FileHandler('mylogname.log')
        
        # stream handler
        #self.ch = logging.StreamHandler()
        
        #self.ch.setFormatter(self.stream_frmt)
        #self.fh.setFormatter(self.file_frmt)
        
        #self.logger.addHandler(self.ch)
        #self.logger.addHandler(self.fh)
        
        
    def debug(self, *args):
        self.logger.debug(
            theme.style_prompt 
            + ''.join(str(i) for i in args) 
            + theme.style_normal)

    def info(self, *args):
        self.logger.info(
            theme.style_yellow 
            + ''.join(str(i) for i in args) 
            + theme.style_normal)

    def exception(self, *args):
        self.logger.exception(
            theme.style_fail 
            + ''.join(str(i) for i in args) 
            + theme.style_normal)

    def warning(self, *args):
        self.logger.warning(
            theme.style_right 
            + ''.join(str(i) for i in args) 
            + theme.style_normal)

log = Logger()
log.info('hello world')
