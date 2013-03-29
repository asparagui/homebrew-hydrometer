#!/usr/bin/env python3

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import sys, string
import re

from subprocess import Popen, PIPE

import subprocess
import argparse

def request_url(url):
    req = Request(url)
    
    try:
        response = urlopen(req)
        
    except HTTPError as error:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', error.code)
    
    except URLError as error:
        print('We failed to reach the server.')
        print('Reason: ', error.reason)
            
    else:            
        data = response.read()
        return data


def sourceforge_parse(line):
        
    pattern = re.compile('(?<=net/)(?P<name>[a-zA-Z0-9\-]+)/')
    
    match = pattern.search(line)
    
    if match:
        if match.group('name')=='project' or match.group('name')=='projects' or match.group('name')=='sourceforge':
            pattern2 = re.compile('(?<=net/)'+match.group('name')+'/(?P<name>[a-zA-Z0-9\-]+)/')
            match = pattern2.search(line)
            if match:
                #print (match.group('name'))
                sourceforge_read(match.group('name'))
        else:
            #print (match.group('name'))
            sourceforge_read(match.group('name'))


def sourceforge_read(name):
    url = 'http://sourceforge.net/projects/' + name + '/files/'
    #print (url)

    data = request_url(url)
   
    if data:
        soup = BeautifulSoup(data)
            
        for dl in soup.find_all("div", class_="download-bar"):
            a = dl.contents[1]
                    
            print (line)
            print ('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t',a.contents[1].contents[1])
            print ('\n\n')


                  
def googlecode_parse(line):
     
     pattern = re.compile('(?<=//)(?P<name>[a-zA-Z0-9\-]+)')
    
     match = pattern.search(line)
    
     if match:
         url = 'http://code.google.com/p/' + match.group('name') + '/downloads/list'
        
         data = request_url(url)
   
         if data:
             soup = BeautifulSoup(data)
                
             print ('\n\n\n\n')
             print (line)
             print ('\n\n')
             
             for dl in soup.find_all("tr",class_='ifOpened'):
                 print (dl)



def gnumirror_parse(line):
    pattern = re.compile('(?<=net/)(?P<name>[a-zA-Z0-9\-]+)/')

    match = re.search('(?<=org/)\w+', line)
    
    if match:
        
        url = 'http://ftp.gnu.org/gnu/' + match.group(0) + '/?C=M;O=D'
        
        data = request_url(url)
            
        if data:
            soup = BeautifulSoup(data)
                
            print ('\n\n\n\n')
            print (line)
            print ('\n\n')
            
            for dl in soup.find_all("a"):
                print (dl)



def github_parse(line):

    pattern = re.compile('(?<=github.com/)(?P<username>[a-zA-Z0-9\-]+)/(?P<projectname>[a-zA-Z0-9\-]+)/')
    
    match = pattern.search(line)
    
    if match:
        if match.group('username')=='downloads':
            pattern2 = re.compile('(?<=github.com/)downloads/(?P<username>[a-zA-Z0-9\-]+)/(?P<projectname>[a-zA-Z0-9\-]+)/')
            match = pattern2.search(line)

    if match:
        github_read(match.group('username'), match.group('projectname'))

    
def github_read(username, projectname):
    url = 'http://github.com/' + username + '/' + projectname + '/tags'

    data = request_url(url)
        
    if data:
        soup = BeautifulSoup(data)
            
        for dl in soup.find_all("table", class_="tag-list"):
            print ('\n\n\n\n\n\n')
            print (line)
            
            for tr in dl.find_all("tr"):
                for a in tr.find_all("a"):    
                    print (a)




def package_list(source):    

    process = subprocess.Popen("grep url /usr/local/Library/Formula/*.rb | grep " + source,
                                 shell=True,
                                 stdout=subprocess.PIPE )
    stdout_data = str( process.communicate()[0], encoding='utf8' )
        
    package_list = stdout_data.split('\n')

    return package_list
    
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Please specify which source of homebrew packages you wish to parse.')
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument("-s", "--sourceforge", action="store_true")
    group.add_argument("-c", "--googlecode", action="store_true")
    group.add_argument("-g", "--gnuftp", action="store_true")
    group.add_argument("-b", "--github", action="store_true")

    args = parser.parse_args()
        
    print ('Building a list of files to process, this may take some time...')    

    if args.sourceforge:
        
        packages = package_list('sourceforge')
    
        for line in packages:
            sourceforge_parse(line)
        
    elif args.googlecode:
    
        packages = package_list('googlecode')
    
        for line in packages:
            googlecode_parse(line)

    elif args.gnuftp:
    
        packages = package_list('ftpmirror')
        
        for line in packages:
            gnumirror_parse(line)

    elif args.github:
    
        packages = package_list('github')
        
        for line in packages:
            github_parse(line)

    else:
        print ('No package source specified, halting.  (try --help)')
    
    
    