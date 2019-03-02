# -*- coding: utf-8 -*-
"""
Created on Sun Feb 10 16:21:23 2019

@author: Scott
"""
from helper import load_obj, save_obj, init_driver, searchJobs, text_cleaner, get_pause, \
string_from_text
description = text_cleaner(desc_list)
description = [d.decode('unicode_escape') for d in description]