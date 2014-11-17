#coding=utf-8

import sys,os,urllib,urllib2
import web
import sqlite3

reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('../config')
import scholarCiteConfig as config

# 将未收录的图书cite值标为-1

# testEnd = False

def update(filepath):
    isbn = os.path.basename(filepath).split('.')[0]
    data = urllib.urlencode({
        'isbn' : isbn,
        'num' : -1
    })

    req = urllib2.Request(config.site_host + "/submit/set_cite",data)
    res = urllib2.urlopen(req)

    # print res.read()

def checkIfUnrecorded(filepath):
    keyWords = "did not match any articles published in"
    html = open(filepath).read()

    if html.find(keyWords)>-1:
        update(filepath)
        # global testEnd 
        # testEnd = True


def runFromFolder(path = config.html_path):
    # global testEnd 

    print "Go to folder: %s"%path
    fileList = os.listdir(path)
    for filename in fileList:
        # if testEnd : return

        filepath = path + filename
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1]==".html":
            checkIfUnrecorded(filepath)
            sys.stdout.write('.')
            sys.stdout.flush()
        elif os.path.isdir(filepath):
            runFromFolder(filepath + "/")
        else:
            print filepath



runFromFolder()










