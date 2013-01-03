'''
#=============================================================================
#     FileName: loadc.py
#         Desc: Calculate land conductivity (search conductivity map)
#       Author: quake0day
#        Email: quake0day@gmail.com
#     HomePage: http://www.darlingtree.com
#      Version: 0.0.1
#   LastChange: 2012-04-05 18:52:34
#      History:
#=============================================================================
'''
import Image
import math

LAT_SW = -47.27
LAT_NE = -34.107
LNG_SW = 166.31
LNG_NE = 179
DEFAULT_RES =5

def getConductivity_c(lat,lng):
    if lat < LAT_SW and lat > LAT_NE and lng < LNG_SW and lng > LNG_NE:
        return -1
    im = Image.open('./data/NewZealand.png')
    pixels = im.load()
    width,height = im.size
    lat_diff = abs(LAT_SW - LAT_NE)
    lng_diff = abs(LNG_SW - LNG_NE)
    lng_one_pix = lng_diff / width
    conductivity_c = pixels[ 
            int(abs(lng -LNG_SW) * width / lng_diff),
            int(abs(lat-LAT_NE) * height / lat_diff)]
    return conductivity_c

def getConductivity_c_mat(data):
    conductivity_c_mat = []
    im = Image.open('./data/NewZealand.png')
    pixels = im.load()
    width,height = im.size
    lat_diff = abs(LAT_SW - LAT_NE)
    lng_diff = abs(LNG_SW - LNG_NE)
    lng_one_pix = lng_diff / width
    for item in data:
        lat = float(item[0])
        lng = float(item[1])
        conductivity_c_mat.append(pixels[ 
                int(abs(lng -LNG_SW) * width / lng_diff),
                int(abs(lat-LAT_NE) * height / lat_diff)])
    return conductivity_c_mat

def convert_mat(conductivity_c_mat):
    res =[]
    for conductivity_c in conductivity_c_mat:
        res.append(convert(conductivity_c))
    return res

def convert(conductivity_c):
    # define default res
    default_res = DEFAULT_RES
    res = default_res
    # search the table
    if conductivity_c == (102,102,102):
        res = 10 * pow(10,-3)
    if conductivity_c == (255,255,0):
        res = 3 * pow(10,-3)
    if conductivity_c == (0,153,0):
        res = 5 * pow(10,-3)
    if conductivity_c == (255,0,255):
        res = 5 * pow(10,-2)
    if conductivity_c == (255,0,0):
        res = 1 * pow(10,-3)
    if conductivity_c == (255,153,0):
        res = 3 * pow(10,-2)
    if conductivity_c == (153,0,51):
        res = 20 * pow(10,-3)
    if conductivity_c == (102,204,255):
        res = 1.6 * pow(10,-3)
    if conductivity_c == (0,51,51):
        res = 1 * pow(10,-3)
    if conductivity_c == (51,0,0):
        res = 0.8 * pow(10,-3)
    if conductivity_c == (0,0,204):
        res = 0.2 * pow(10,-3)
    if conductivity_c == (255,204,204):
        res = 0.1 * pow(10,-3)
    # if getConductivity error then using default res
    if conductivity_c == -1:
        res = default_res
    return res

def getConductivity_mat(data):
    return convert_mat(getConductivity_c_mat(data))

def getConductivity(lat,lng):
    return convert(getConductivity_c(float(lat),float(lng)))



def loadSedmapDat(lat,lng):
# Change lat lng from [-90,90] [-180,180] into [0,180] [0,360]
    lat_C = -(lat - 90 )
    lng_C = lng + 180
#Read file
    file = open("./data/sedmap.dat", "r")
    content = file.read().split("\r")
    file.close()
# Create data as latxlng matrix
    data = [x.strip().split("   ") for x in content]
# Change data to num
    #return eval(data[int(lat_C)][int(lng_C)])
    return 1/float(eval(data[int(lat_C)][int(lng_C)]))

def loadSedmapDat_mat(data):
    conductivity_mat = []
    for item in data:
        lat = item[0]
        lng = item[1]
        conductivity_mat.append(loadSedmapDat(lat,lng))
    return conductivity_mat

print loadSedmapDat(-45,171.23123)

#print getConductivity(-39.54641191968671,174.0234375)
#print getConductivity(-39.50404070558415,174.0673828125)
#print getConductivity(-39.104488809440475,175.05615234375)
#getConductivity(-44.809121700077355,168.607177734375)
#print convert(getConductivity_c(-46.118941506107056,168.37646484375))
#print convert(getConductivity_c(-45.74452698046842,169.95849609375))

