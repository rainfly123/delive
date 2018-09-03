#!/usr/bin/env python
#-*- coding:utf-8 -*- 
import os
import sys
import time as ltime
import datetime
import daemon
import mysql
import commands
import json

if __name__ == "__main__":
    daemon.daemonize("/tmp/delive.pid")
    mydata = []
    basedir = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(basedir, 'config')
    data = json.load(open(filename))
    for channel in data["all"]:
        gid = channel['Gid']
        times = channel['Times']
        one = {"gid":gid, "time":[]}
        for time in times:
            start = datetime.datetime.strptime(time['StartTime'], "%Y-%m-%d %H:%M")
            end = datetime.datetime.strptime(time['EndTime'], "%Y-%m-%d %H:%M")
            one["time"].append({"startime":start, "endtime":end})
            mydata.append(one)

    while True:
        now = datetime.datetime.now()
        print now
        for c in mydata:
            gid = c['gid']
            times = c['time']
            for x in times:
                x = x['startime']
                if now.date() ==  x.date() and now.hour == x.hour and now.minute == x.minute:
                    print "start",gid,x
                    mysql.NoLive(gid)
            for x in times:
                x = x['endtime']
                if now.date() ==  x.date() and now.hour == x.hour and now.minute == x.minute:
                    print "end",gid,x
                    mysql.Live(gid)
        
        ltime.sleep(10)

