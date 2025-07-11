''' This module introduces the Amplitude class which collects methods for
calculating, adding and displaying. '''

import math
import struct
import sys
from vu_constants import SHORT_NORMALIZE, LINE_CLEAR
from vu_utilityFunctions import Saturate

class Amplitude(object):
    ''' an abstraction for Amplitudes (with an underlying float value)
    that packages a display function and many more '''

    def __init__(self, p_value=0, p_blPrintConsequtively=False):
        self.value = p_value
        self.blPrintConsequtively = p_blPrintConsequtively

    def __add__(self, other):
        return Amplitude(self.value + other.value)

    def __sub__(self, other):
        return Amplitude(self.value - other.value)

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value

    def to_int(self, scale=1):
        ''' convert an amplitude to an integer given a scale such that one can
        choose the precision of the resulting integer '''
        return int(self.value * scale)

    def __int__(self):
        return self.to_int()

    def __str__(self):
        return str(self.value) + " dB"

    @staticmethod
    def from_data(block, gain, *args):
        ''' generate an Amplitude object based on a block of audio input data '''
        count = len(block) // 2
        shorts = struct.unpack("%dh" % count, block)
        sum_squares = sum(s**2 * SHORT_NORMALIZE**2 for s in shorts)
        return Amplitude(Saturate(math.sqrt(sum_squares / count) * gain, -1.0, 1.0), *args)

    def display(self, mark, scale=50):
        ''' display an amplitude and another (marked) maximal Amplitude
        graphically '''
        int_val = self.to_int(scale)
        mark_val = mark.to_int(scale)
        delta = abs(int_val - mark_val)
        emptySpaceAtTheEnd = scale - mark_val

        if(self.blPrintConsequtively):
            print(int_val * '*', (delta-1) * ' ', '|')
        else:
            sTextToBePrinted = f"\r[{str(int_val).zfill(3)}][{int_val * '='}{(delta-1) * '-'}{'X'}{emptySpaceAtTheEnd * '-'}]"
            sys.stdout.write(LINE_CLEAR)
            sys.stdout.write(sTextToBePrinted)
            sys.stdout.flush()
       
        