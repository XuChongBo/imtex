#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from pylab import imshow,show,savefig
import pylab

to_save = True
to_show = False


def output(filename='plot.png'):
    if to_save:
        #save_path = "./data/"
        save_path = "/Users/xcbfreedom/projects/imtex/uploads/"
        f = os.path.join(save_path,filename)
        pylab.savefig(f,bbox_inches='tight')
    if to_show:
        pylab.show()
