# -*- coding: utf-8 -*-
"""
Web scrapping tools.
Created on Sun Nov  6 17:04:34 2016

@author: Ivan Georgiev
"""
import tempfile
import hashlib
import os.path as path
import urllib.request as request
from bs4 import BeautifulSoup, Comment

# ==================================================================
cache_dir = tempfile.gettempdir() + '/iglib-urlread'

# ==================================================================
def get_hash_for(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest() + str(len(url))

# ==================================================================
def get_cache_filename_for(url):
    if not os.path.isdir(cache_dir):
        os.makedirs(cache_dir)
    return "{}/{}.html".format(cache_dir, get_hash_for(url))

# ==================================================================
def open_cache_for(url, force=False):
    """Opens local cache file for a given url."""
    cache_filename = get_cache_filename_for(url)
    
    if (force or not path.isfile(cache_filename)) :
        with request.urlopen(url) as src:
            content = src.read()
        with open(cache_filename, 'wb') as cf:
            cf.write(content)
    
    return open(cache_filename, 'rb')
    
# ==================================================================
def read_from(url, force=False):
    """Read url from cache or remote."""
    with open_url(url, force) as localfile:
        return localfile.read()
        

# ==================================================================
def bs_remove_comments(soup):
    """Remove comments from Beautiful Soup 4's soup"""
    for c in soup.find_all(text=lambda x: isinstance(x,Comment)):
        c.replace_with('')
    return soup
    
    
    
# ==================================================================
def bs_remove_tag(soup, tag):
    """Remove tag (including contents) from Beautiful Soup's soup.

       soup
           Beautiful Soup's soup object.
           
       tag
           Tag name or collection of tag names.
    
       Example:
       
       Following example extracts the text from a web page.
       
       ```python
       import urllib
       
       # Create a soup object
       soup = BeautifulSoup(urllib.request.urlopen('http://wikipedia.org'))
       
       # Remove comments
       bs_remove_comments(soup)
       
       # Remove following tags.
       bs_remove_tag(soup,['head','script','style'])
       
       # Extract text from all tags that has left.
       soup.get_text()
       ```
        
    """
    if isinstance(tag, str):
        for el in soup.find_all(tag):
            el.replace_with('')
    else:
        for t in tag:
            bs_remove_tag(soup, t)
    return soup
