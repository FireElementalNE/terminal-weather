'''
Get the weather on your terminal!

This project was ported from a shell scipt forum post found here:

https://bbs.archlinux.org/viewtopic.php?id=37381

It also uses some code from the Python Cookbook
'''

import sys,json,re,os,pprint
from urllib import urlopen



#following from Python cookbook, #475186
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False


has_colours = has_colours(sys.stdout)
def printout(text, colour=WHITE):
    if has_colours:
        seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
        sys.stdout.write(seq)
    else:
        sys.stdout.write(text)

#END python cookbook

def getDirection(wd): #convert from deg to compass direction used javascript @ http://www.csgnetwork.com/degrees2direct.html as a skeliton
    if wd >= 0 and wd <= 11.25:
        return 'N'
    elif wd > 348.75 and wd <= 360:
        return 'N'
    elif wd > 11.25 and wd <= 33.75:
        return 'NNE'
    elif wd > 33.75 and wd <= 56.25:
        return 'NE'
    elif wd > 56.25 and wd <= 78.75:
        return 'ENE'
    elif wd > 78.75 and wd <= 101.25:
        return  'E'
    elif wd > 101.25 and wd <= 123.75:
        return 'ESE'
    elif wd > 123.75 and wd <= 146.25:
        return 'SE'
    elif wd > 146.25 and wd <= 168.75:
        return 'SSE'
    elif wd > 168.75 and wd <= 191.25:
        return 'S'
    elif wd > 191.25 and wd <= 213.75:
        return 'SSW'
    elif wd > 213.75 and wd <= 236.25:
        return 'SW'
    elif wd > 236.25 and wd <= 258.75:
        return 'WSW'
    elif wd > 258.75 and wd <= 281.25:
        return 'W'
    elif wd > 281.25 and wd <= 303.75:
        return 'WNW'
    elif wd > 303.75 and wd <= 326.25:
        return 'NW'
    elif wd > 326.25 and wd <= 348.75:
        return 'NNW'


def verbose(ver,s,fh):
    if ver:
        os.write(fh,s)
#2 simple conversion functions
def convertK2C2FToString(temp):
    return str(int((((temp-273.15)*9)/5)+32))

def convertK2CToString(temp):
    return str(int(((temp-273.15))))

def float2Int2String(arg):
    return str(int(arg))

def mph2kph(arg):
    return str(int(1.609344 * arg))

def printInfo(city,country,cond,temp,tmax,tmin,windS,windD,arr,unit1,unit2):
    printout("Location: ",arr[0])
    sys.stdout.write(city + ', ' + country + ' ')
    printout("Condition: ",arr[1])
    sys.stdout.write(cond + ' ')
    printout("Temp: ",arr[2])
    sys.stdout.write(temp + unit1 + ' ')
    printout("Max Temp: ",arr[3])
    sys.stdout.write(tmax + unit1 + ' ')
    printout("Min Temp: ",arr[4])
    sys.stdout.write(tmin + unit1 + ' ')
    printout("Wind: ",arr[5])
    sys.stdout.write(windS + unit2 + ' ' + windD + '\n') 

def getInfo(VER,FH,city,country=None,unit=None): #get data
    try:
        if country != None: #Contruct proper url depending on args
            url = 'http://api.openweathermap.org/data/2.5/weather?q=%s,%s' % (city,country)
        else:
            url = 'http://api.openweathermap.org/data/2.5/weather?q=%s' % (city)
        verbose(VER,'Sending/Receiving Request...',FH)
        content = json.loads(urlopen(url).read()) #Fetch and load JSON data
        verbose(VER,'done.\n',FH)
        verbose(VER,'printing JSON result:\n',FH)
        pprint.pprint(content)
        description = content['weather'][0]['description'] #get result accorfing to weather API
        max_temp = content['main']['temp_max']
        min_temp = content['main']['temp_min']
        temp = content['main']['temp']
        city0 = content['name']
        country0 = content['sys']['country']
        windSpeed = content['wind']['speed']
        windDeg = content['wind']['deg']
        verbose(VER,'Printing Data:\n',FH)
        if unit == None:
            unit = 'f'
        if unit.lower() == 'f' or unit.lower() == 'fahrenheit':
            printInfo(city0,country0, description, convertK2C2FToString(temp), convertK2C2FToString(max_temp), convertK2C2FToString(min_temp), float2Int2String(windSpeed), getDirection(windDeg), myArr,'F','mph')
        elif unit.lower() == 'c' or unit.lower() == 'celcius':
            printInfo(city0,country0, description, convertK2CToString(temp), convertK2CToString(max_temp), convertK2CToString(min_temp), mph2kph(windSpeed), getDirection(windDeg), myArr,'C','kph')
        elif unit.lower() == 'k' or unit.lower() == 'kelvin':
            printInfo(city0,country0, description, float2Int2String(temp), float2Int2String(max_temp), float2Int2String(min_temp), mph2kph(windSpeed), getDirection(windDeg), myArr,'K','kph')
    except (ValueError, KeyError):
        print 'If you are seeing this something went wrong, check your spelling!'

VER = True
FH = 1
myArr = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]


try:
    flag = 0
    myRegex = '^(\d\d\d\d+)$' #city ID
    city = sys.argv[1]
    m = re.search(myRegex,city)
    country = ''
    if m == None: #if not continue as normal
        verbose(VER,'Not using City Code...\n',FH)
        country = sys.argv[2]
        flag = 1
    else:
        verbose(VER,'Using City Code...\n',FH)
except (IndexError, AttributeError):
    print 'usage: python ' + sys.argv[0] + ' <city> <country> <OPTIONAL unit: K, F, or C> '
    print 'usage: python ' + sys.argv[0] + ' <city ID> <OPTIONAL unit: K, F, or C> '
    sys.exit(0)
try:
    flag2 = 0
    if flag == 1:
        unit = sys.argv[3]
    else:
        unit = sys.argv[2]
except IndexError:
    flag2 = 1
if flag2 == 0:
    if flag == 1:
        verbose(VER,'Detected unit change...\n',FH)
        getInfo(VER,FH,city,country,unit)
    else:
        verbose(VER,'Detected unit change...\n',FH)
        getInfo(VER,FH,city,None,unit)
else:
    if flag == 1:
        verbose(VER,'No unit change...\n',FH)
        getInfo(VER,FH,city,country,None) 
    else:
        verbose(VER,'No unit change...\n',FH)
        getInfo(VER,FH,city,None,None)
