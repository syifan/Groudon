from scipy import stats

def getPathLossExp(km,db):
    gradient = 0.0
    gradient,intercept,r_value,p_value,std_err=stats.linregress(km,db)
    return gradient


def read_data(file):
    MAT = []
    fp = open(file,"r")
    while True:
        line = fp.readline()
        data = line.split('\n')[0]
        if not line:break
        MAT.append(float(data))
    #print MAT
    return MAT

#print getPathLossExp([5.05,6.75,3.21,2.66],[1.65,26.5,-5.93,7.96])

#KM = read_data("KM")
#
#!!!!!!!!!!!! YOU HAVE TO DO THIS@!!!!!!!!!!!
#BPL =  read_data("BPL")[3:]
#################################
#print KM
#print BPL
#print len(KM),len(BPL)
#print getPathLossExp(KM,BPL)
