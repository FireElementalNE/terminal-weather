'''
Get the weather on your terminal!

This project was ported from a shell scipt forum post found here:

https://bbs.archlinux.org/viewtopic.php?id=37381

It also uses some code from the Python Cookbook
'''

import sys,json,re
from urllib import urlopen

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

myArr = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]

#following from Python cookbook, #475186

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

#2 simple conversion functions
def convertK2C2FToString(temp):
    return str(int((((temp-273.15)*9)/5)+32))

def float2int2string(arg):
    return str(int(arg))

def printInfo(city,country,cond,temp,tmax,tmin,windS,windD,arr):
    printout("Location: ",arr[0])
    sys.stdout.write(city + ', ' + country + ' ')
    printout("Condition: ",arr[1])
    sys.stdout.write(cond + ' ')
    printout("Temp: ",arr[2])
    sys.stdout.write(temp + 'F ')
    printout("Max Temp: ",arr[3])
    sys.stdout.write(tmax + 'F ')
    printout("Min Temp: ",arr[4])
    sys.stdout.write(tmin + 'F ')
    printout("Wind: ",arr[5])
    sys.stdout.write(windS + 'mph ' + windD + '\n') 

def getInfo(city,country='#'): #get data
    try:
        if country != '#': #Contruct proper url depending on args
            url = 'http://api.openweathermap.org/data/2.5/weather?q=%s,%s' % (city,country)
        else:
            url = 'http://api.openweathermap.org/data/2.5/weather?q=%s' % (city)
        content = json.loads(urlopen(url).read()) #Fetch and load JSON data
        description = content['weather'][0]['description'] #get result accorfing to weather API
        max_temp = content['main']['temp_max']
        min_temp = content['main']['temp_min']
        temp = content['main']['temp']
        city0 = content['name']
        country0 = content['sys']['country']
        windSpeed = content['wind']['speed']
        windDeg = content['wind']['deg']
        printInfo(city0,country0, description, convertK2C2FToString(temp), convertK2C2FToString(max_temp), convertK2C2FToString(min_temp), float2int2string(windSpeed), getDirection(windDeg), myArr)
    except (ValueError, KeyError):
        print 'If you are seeing this something went wrong, check your spelling!'

try:
    flag = 0
    myRegex = '^(\d\d\d\d+)$' #city ID?
    city = sys.argv[1]
    m = re.search(myRegex,city)
    country = ''
    if m == None: #if not continue as normal
        country = sys.argv[2]
        flag = 1
except (IndexError, AttributeError):
    print 'usage: python ' + sys.argv[0] + ' <city> <country> '
    print 'usage: python ' + sys.argv[0] + ' <city ID> '
    sys.exit(0)
if flag == 1:
    getInfo(city,country)
else:
    getInfo(city)
