# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 11:32:20 2019

@author: Mouni
"""

import wikipedia

def get_wiki_text(text):
    
    wikipedia.set_lang("en")
    wiki_text = wikipedia.summary(text, sentences=9)
    
    return wiki_text

