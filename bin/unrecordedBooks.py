#coding=utf-8

import sys,os,re
import web
import sqlite3

reload(sys)
sys.setdefaultencoding('utf8')

sys.path.append('../config')
import scholarCiteConfig as config

# 将未收录的图书cite值标为-1

def update(filepath):
    print filepath

def checkIfUnrecorded(filepath):
    keyWords = "did not match any articles published in"
    html = open(filepath).read()

    if html.search(keyWords)==-1:
        update(filepath)


def runFromFolder(path = config.html_path):
    fileList = os.listdir(path)
    for filename in fileList:
        filepath = path + filename
        if os.path.isfile(filepath) and os.path.splitext(filepath)[1]==".html":
            checkIfUnrecorded(filepath)
        elif os.path.isdir(filepath):
            print "Go to folder: %s"%filepath
            runFromFolder(filepath + "/")
        else:
            print filepath














