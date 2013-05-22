'''
Get the weather on your terminal!

This project was ported from a shell scipt forum post found here:

https://bbs.archlinux.org/viewtopic.php?id=37381

It also uses some code from the Python Cookbook
'''

#http://api.openweathermap.org/data/2.5/weather?q=boston,us
import sys,re,json
from urllib import urlopen

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
#choose color here
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
def convertK2C2F(temp):
    return (((temp-273.15)*9)/5)+32

def printInfo(city,country,cond,temp,tmax,tmin,arrnum,arr):
    printout("Location: ",arr[arrnum])
    sys.stdout.write(city + ', ' + country + ' ')
    printout("Condition: ",arr[arrnum])
    sys.stdout.write(cond + ' ')
    printout("Temp: ",arr[arrnum])
    sys.stdout.write(temp + 'F ')
    printout("Max Temp: ",arr[arrnum])
    sys.stdout.write(tmax + 'F ')
    printout("Min Temp: ",arr[arrnum])
    sys.stdout.write(tmin + 'F\n')

def getInfo(city,country,i=4):
    try:
        url = 'http://api.openweathermap.org/data/2.5/weather?q=%s,%s' % (city,country)
        content = json.loads(urlopen(url).read())
        description = content['weather'][0]['description']
        max_temp = content['main']['temp_max']
        min_temp = content['main']['temp_min']
        temp = content['main']['temp']
        city0 = content['name']
        country0 = content['sys']['country']
        printInfo(city0,country0,description,str(int(convertK2C2F(temp))),str(int(convertK2C2F(max_temp))),str(int(convertK2C2F(min_temp))),i,myArr)
    except (ValueError, KeyError):
        print 'If you are seeing this something went wrong, check your spelling!'
    

try:
    if sys.argv[1] != 'all':
        city = sys.argv[1]
        country = sys.argv[2]
except IndexError:
    print 'usage: python ' + sys.argv[0] + ' <city> <country> '
    sys.exit(0)
getInfo(city,country)
