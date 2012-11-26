#!/usr/local/bin/python3

from bs4 import BeautifulSoup

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

import sys, string
import re

from subprocess import Popen, PIPE

import subprocess
import argparse

def sourceforge_parse(line):
    
    m = re.search('(?<=net/)\w+', line)

    if m:
        
        name = ''
        
        if m.group(0)=='project' or m.group(0)=="projects":
            m = re.search('(?<='+m.group(0)+'/)\w+', line)
            if m:
                name = m.group(0)
                #print (m.group(0), line)
        else:
            name = m.group(0)
            #print (m.group(0), line)
            
        if name:
            
            url = 'http://sourceforge.net/projects/' + name + '/files/'
        
            print (url)
            

            req = Request(url)
            try:
                response = urlopen(req)
            except HTTPError as e:
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            except URLError as e:
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            
            else:            
                data = response.read()
            
                if data:
                    soup = BeautifulSoup(data)
            
                    for dl in soup.find_all("div", class_="download-bar"):
                        a = dl.contents[1]
                    
                        print (line)
                        print ('                        ',a.contents[1].contents[1])
                        print ('\n\n')
                        
                        
                        
                        
def googlecode_parse(line):

     m = re.search('(?<=//)\w+', line)
    
     if m:

         url = 'http://code.google.com/p/' + m.group(0) + '/downloads/list'
        
         req = Request(url)
         try:
             response = urlopen(req)
         except HTTPError as e:
             print('The server couldn\'t fulfill the request.')
             print('Error code: ', e.code)
         except URLError as e:
             print('We failed to reach a server.')
             print('Reason: ', e.reason)
            
         else:            
             data = response.read()
            
             if data:
                 soup = BeautifulSoup(data)
                
                 print ('\n\n\n\n')
                 print (line)
                
                 for dl in soup.find_all("tr",class_='ifOpened'):
                    
                     print (dl)



def gnumirror_parse(line):

    m = re.search('(?<=org/)\w+', line)
    
    if m:

        url = 'http://ftpmirror.gnu.org/' + m.group(0) + '/?C=M;O=D'
        
        req = Request(url)
        try:
            response = urlopen(req)
        except HTTPError as e:
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
            
        else:            
            data = response.read()
            
            if data:
                soup = BeautifulSoup(data)
                
                print ('\n\n\n\n')
                print (line)
                
                for dl in soup.find_all("a"):
                    
                    print (dl)





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Please specify which source of homebrew packages you wish to parse.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--sourceforge", action="store_true")
    group.add_argument("-c", "--googlecode", action="store_true")
    group.add_argument("-g", "--gnuftp", action="store_true")

    args = parser.parse_args()
        
    if args.sourceforge:
        print ('Building a list of files to process, this may take some time...')    
        process = subprocess.Popen("grep url /usr/local/Library/Formula/*.rb | grep sourceforge",
                                     shell=True,
                                     stdout=subprocess.PIPE )
        stdout_data = str( process.communicate()[0], encoding='utf8' )
        
        package_list = stdout_data.split('\n')
    
        for line in package_list:
            sourceforge_parse(line)
        
    elif args.googlecode:
        print ('Building a list of files to process, this may take some time...')    
        process = subprocess.Popen("grep url /usr/local/Library/Formula/*.rb | grep googlecode",
                                     shell=True,
                                     stdout=subprocess.PIPE )
        stdout_data = str( process.communicate()[0], encoding='utf8' )
        
        package_list = stdout_data.split('\n')
    
        for line in package_list:
            googlecode_parse(line)

    elif args.gnuftp:
        print ('Building a list of files to process, this may take some time...')    
        process = subprocess.Popen("grep url /usr/local/Library/Formula/*.rb | grep ftpmirror",
                                     shell=True,
                                     stdout=subprocess.PIPE )
        stdout_data = str( process.communicate()[0], encoding='utf8' )
        
        package_list = stdout_data.split('\n')
    
        for line in package_list:
            gnumirror_parse(line)



    else:
        print ('No package source specified, halting.  (try --help)')
    
    
    