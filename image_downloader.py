# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 11:21:33 2019

@author: Mouni
"""

from google_images_download import google_images_download   #importing the library

def download_image(text):
    
    response = google_images_download.googleimagesdownload()   #class instantiation
    
    arguments = {"keywords":text,"limit":1,"print_urls":True,"output_directory":'static\google_images'}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    
    return paths   #printing absolute paths of the downloaded images

