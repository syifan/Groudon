# -*- coding: utf8 -*-
import subprocess
import os
import sys
import time
from time import sleep
import MySQLdb
import random
import shutil
from conn import connMysql
from caldistance import CalDis
from getPathLossExp import read_data
from getPathLossExp import getPathLossExp
from loadc import getConductivity
from trim import trim
from txt2image import txt2image
from txt2html import plaintext2html
import getHeight
from getHeight import getPathInfo
from getHeight import formatPathInfo
from getHeight import getHTT
from getHeight import getHRR
from millinton import cal_milliton

MIN_POINT = 2
TRACE_FILE_NAME = "simple.tr"


def get_job():
    conn = connMysql()
    cur = conn.cursor()
    sql = "SELECT * FROM `main` WHERE `status`=0 LIMIT 0,30"
    cur.execute(sql)
    dataset = cur.fetchall()
    cur.close()
    conn.close()
    return dataset

def split_job(dataset):
    jobs={}
    for data in dataset:
        jobs.setdefault(data[1],[]).append(data)
    for job in jobs:
        yield list(jobs.get(job,()))

def split_parameters(dataset):
    simulation_paras = []
    
    dataset = dataset.split("END,")
    for data in dataset:
        parameters_set =  data.split(",")
        simulation_paras.append(parameters_set)
    return simulation_paras



def do_simulation(job):
    # for DEBUG
    try:
        running_id = job[0][1]
        parameters = job[0][2]
    except Exception,e:
        print "ERROR- Point Num ERROR OR Lack LAT LNG"
        mark_as_complete(job[0])
        return 1

    para_set = split_parameters(parameters)
    clean_pre_data(running_id)
    for data in para_set:
        lat1 = data[0].split("(")[1].strip()
        lng1 = data[1].split(")")[0].strip()
        lat2 = data[2].split("(")[1].strip()
        lng2 = data[3].split(")")[0].strip()
        if (data[4] == "PARA"):
# If it has parameters
# then
            freq = float(data[5])
            pol = data[6]
            if (pol == "Vertical"):
                pol = 0
            else:
                pol = 1
            height = float(data[7])
            height_r = float(data[8])
            bandwidth = float(data[9])
# Now its time to run simulation
            result_set = run_GRWAVE(running_id,lat1,lng1,lat2,lng2,freq,pol,height,height_r,bandwidth)
            run_NS(running_id,result_set)
# Upload the result
            upload_FINAL_RESULT(running_id)
    mark_as_complete(running_id)
    return 0
        #print freq,pol,height,height_r,bandwidth

def run_GRWAVE(running_id,lat1,lng1,lat2,lng2,freq,pol,height,height_r,bandwidth):
    #save_res(show_res("out"),job[0])

# calculate the distance between two points
    try:
        dis = CalDis(lat1,lng1,lat2,lng2)
    except Exception,e:
        print "error cal dis"
        mark_as_complete(running_id)
    try:
        con1 = getConductivity(lat1,lng1)
    except Exception,e:
        print "error cal con1"
        mark_as_complete(running_id)

    try:
        geo_height = getPathInfo(lat1,lng1,lat2,lng2)
        if geo_height == None:
            raise Exception,e
        elif geo_height < 0:
            geo_height = 0
    except Exception,e:
        print e
        print "cannot grab geo_info"
        mark_as_complete(running_id)
    try:
        geo_height2 = formatPathInfo(geo_height)
        if geo_height2 < 0:
            geo_height2 = 0
    except Exception,e:
        mark_as_complete(running_id)
        print "geo height grab error"
        print geo_height
        return 1
    try:
        #hei1_mean = getHeight_mean(lat1,lng1,lat2,lng2)
        if getHTT(geo_height2) < 0:
            HTT = height
        else:
            HTT = getHTT(geo_height2) + height
        if getHRR(geo_height2) < 0:
            HRR = height_r
        else:
            HRR = getHRR(geo_height2) + height_r
        #HTT = getHTT(geo_height2) + height
        #HRR = getHRR(geo_height2) + height_r
        print "HTT,HRR:",HTT,HRR
    except Exception,e:
        print "error calculate HTT HRR"
        mark_as_complete(running_id)
        return 1
    try:
        res =\
        cal_milliton(geo_height2,int(freq),int(pol),dis,HTT,HRR,height,height_r)
        if res is not None:
            save_Et(res,running_id)
#@ NOW FIX THIS
    except Exception,e:
        print e
        mark_as_complete(running_id)
        return 1
    
    try:
        fp = open("inp","w")
    except Exception,e:
        print "error open"
    command1 = "HTT {} \n\
               HRR {} \n\
               IPOLRN {}\n\
               FREQ {} \n\
               SIGMA {} \n\
               EPSLON 30 \n\
               dmin 1\n\
               dmax {}\n\
               dstep 5\n\
               GO\
               ".format(str(HTT),str(HRR),pol,freq,con1,dis)
    fp.write(command1)
    fp.close()
    fp = open("inp2","w")
    command = "HTT {} \n\
               HRR {} \n\
               IPOLRN {}\n\
               FREQ {} \n\
               SIGMA {} \n\
               EPSLON 30 \n\
               dmin 1\n\
               dmax 1000\n\
               dstep 5\n\
               GO\
               ".format(str(HTT),str(HRR),pol,freq,con1)
    fp.write(command)
    fp.close()
#    except Exception,E:
#        print command1
#        print "Error writing inp inp2"
        #return 1
    # running grwave the result will save in out
    rungrwave=os.getcwd()+"/gr <inp >out"
    rungrwave_for_ns2=os.getcwd()+"/gr <inp2 >out2"
    runget_result="sh "+os.getcwd()+"/get_res.sh"
    run_get_KM = "perl get_KM.pl out2 > KM"
    run_get_BPL = "perl get_BasicPathLoss.pl out2 > BPL"
    try:
        process1 = subprocess.Popen(rungrwave,shell=True)
        process1.wait()
    except Exception,E:
        print "Error process 1"
        mark_as_complete(running_id)
        return 1
    try:
        process2 = subprocess.Popen(rungrwave_for_ns2,shell=True)
        process2.wait()
    except Exception,e:
        print "Error process 2"
        mark_as_complete(running_id)
        return 1
    try:
        process3 = subprocess.Popen(run_get_KM,shell=True)
        process3.wait()
    except Exception,E:
        print "Error process 3"
        mark_as_complete(running_id)
        return 1
    try:
        process4 = subprocess.Popen(run_get_BPL,shell=True)
        process4.wait()
    except Exception,E:
        print "Error process 4"
        mark_as_complete(running_id)
        return 1
    try:
        DAT_KM = read_data("KM")
        DAT_BPL = read_data("BPL")[3:]
    except Exception,E:
        print "Error process read data"
        mark_as_complete(running_id)
        return 1
    try:
        PathLossExp = getPathLossExp(DAT_KM,DAT_BPL)
    except Exception,e:
        print "Error get pathlossexp"
        mark_as_complete(running_id)
        return 1
    result_set = []
    result_set.append(bandwidth)
    result_set.append(freq)
    result_set.append(dis)
    return result_set

def run_NS(running_id,result_set):
    bandwidth = result_set[0]
    freq = result_set[1]
    dis = result_set[2]

    try:
        bandwidth_ns = " " + str(bandwidth)+"bps"+ " "
        freq_ns = " "+str(freq)+"e6"+" "
        dis_ns = " "+str(dis*1000)+" "
        run_ns2 = os.getcwd()+"/ns dsr.tcl "
        run_ns2 = run_ns2+str(0.1)+bandwidth_ns+freq_ns+dis_ns
        print run_ns2
        process = subprocess.Popen(run_ns2,shell=True)
        process.wait()
    except Exception,e:
        print "run_ns2 error"
        mark_as_complete(running_id)
    try:
        run_ana_throughput = "perl mea.pl "+TRACE_FILE_NAME
        process_out =\
        subprocess.Popen(run_ana_throughput,stdout=subprocess.PIPE,shell=True).communicate()
    except Exception,e:
        print "run_ana_throughput error"
    print process_out[0]
    print len(process_out[0].split(","))
    save_res(process_out[0],"throughput",running_id)
    try:
        run_ana_del = "perl del.pl "+TRACE_FILE_NAME
        process_out =\
        subprocess.Popen(run_ana_del,stdout=subprocess.PIPE,shell=True).communicate()
    except Exception,e:
        print "run_ana_del error"
        mark_as_complete(running_id)
    print process_out[0]
    print len(process_out[0].split(","))
    save_res(process_out[0],"delay",running_id)

    return 0


def upload_FINAL_RESULT(running_id):
    try:
        random_num = upload_res()
    except Exception,e:
        mark_as_complete(running_id)
        print "upload res error"
        return 1
    try:
        save_res(random_num,"res",running_id)
    except Exception,e:
        mark_as_complete(running_id)
        print "save res error"
        return 1
    #K = subprocess.Popen(runget_result,shell=True,stdout=subprocess.PIPE)
    #req0 = mark_as_complete(running_id)
    #save_res(show_res("out"),job[0])
    #print show_res("out")

def show_res(file):
    fout = open(file,"r")
    return fout.read()

def save_res(data,name,running_id):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `"+name+"` = \""+data+"\" where running_id= " +str(running_id)
    print sql
    cur.execute(sql)
    conn.commit()
    cur.close
    conn.close()

#
def save_Et(Et,running_id):
    conn = connMysql()
    cur = conn.cursor()
    get_old_Et = "Select `Et` from `gr`.`main` where running_id = "+\
            str(running_id)
    cur.execute(get_old_Et)
    pre_res = cur.fetchone()[0]
    if pre_res:
        new_data = pre_res+","+str(Et)
    else:
        new_data = str(Et)
    print new_data

    sql = "UPDATE `gr`.`main` SET `Et` = \""+new_data+"\" where running_id="+\
            str(running_id)
    print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def upload_res():
    random_num = str(random.randrange(0,10001,2))
    print rundom_num
    try:
        shutil.copy2(os.getcwd()+"/out","/home/quake0day/www/Torterra/res/"+random_num)
        shutil.copy2(os.getcwd()+"/simple.tr","/home/quake0day/www/Torterra/tr/"+random_num)
    except Exception,e:
        print "upload error"
    return random_num

def save_res_plot(res,running_id):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `throughput` =\""+res+"\" where running_id=\
    "+str(running_id)
    print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return 0

def mark_as_complete(running_id):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `status` = 1 where running_id= " +str(running_id)
   # print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return 0

def clean_pre_data(running_id):
    conn = connMysql()
    cur = conn.cursor()
    sql = "UPDATE `gr`.`main` SET `Et` = null where running_id= " +str(running_id)
   # print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return 0

if __name__ == '__main__':
    #main
    while 1:
        sleep(1)
        try:
            job = split_job(get_job())
        except Exception,e:
            pass
        try:
            task = job.next()
            do_simulation(task)

            sleep(1)
        except Exception,e:
            pass
