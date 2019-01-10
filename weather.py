'''
Get the weather on your terminal!

This project was ported from a shell scipt forum post found here:

https://bbs.archlinux.org/viewtopic.php?id=37381

It also uses some code from the Python Cookbook
'''

import sys, traceback
import json
import re
import os
import pprint
import argparse
import urllib.request
from apikey import APPID

#following from Python cookbook, #475186

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
myArr = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]

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

def get_direction(wd): #convert from deg to compass direction used javascript @ http://www.csgnetwork.com/degrees2direct.html as a skeliton
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
		

def print_verbose(ver,s):
	if ver:
		print(s)

#2 simple conversion functions
def convertK2C2FToString(temp):
	return str(int((((temp-273.15)*9)/5)+32))

def convertK2CToString(temp):
	return str(int(((temp-273.15))))

def float2Int2String(arg):
	return str(int(arg))

def mph2kph(arg):
	return str(int(1.609344 * arg))

def print_info(city,country,cond,temp,tmax,tmin,windS,windD,arr,unit1,unit2):
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

def get_info(verbose, city, country, unit):
	try:
		if country != None: #Contruct proper url depending on args
			url = 'http://api.openweathermap.org/data/2.5/weather?q={},{}&APPID={}'.format(city,country, APPID);
		else:
			url = 'http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}'.format(city, APPID);
		print_verbose(verbose,'Sending/Receiving Request...'); print()
		content = json.loads(urllib.request.urlopen(url).read().decode("utf-8")) #Fetch and load JSON data
		print_verbose(verbose,'done.\n')
		print_verbose(verbose,'printing JSON result:')
		if verbose:
			pprint.pprint(content)
		description = content['weather'][0]['description'] #get result accorfing to weather API
		max_temp = content['main']['temp_max']
		min_temp = content['main']['temp_min']
		temp = content['main']['temp']
		city_json = content['name']
		country_json = content['sys']['country']
		wind_speed = content['wind']['speed']
		wind_deg = content['wind']['deg']
		print_verbose(verbose,'Printing Data:')
		if unit.lower() == 'i':
			temp = convertK2C2FToString(temp)
			max_temp = convertK2C2FToString(max_temp)
			min_temp = convertK2C2FToString(min_temp)
			temp_unit = 'F'
			speed_unit = 'mph'
		elif unit.lower() == 'm':
			temp = convertK2CToString(temp)
			max_temp = convertK2CToString(max_temp)
			min_temp = convertK2CToString(min_temp)
			wind_speed = mph2kph(wind_speed)
			temp_unit = 'C'
			speed_unit = 'kph'
		wind_dir = get_direction(wind_deg)
		print_info(city_json, country_json, description, temp, max_temp, min_temp, str(wind_speed), wind_dir, myArr, temp_unit, speed_unit)
	except(ValueError, KeyError):
		print('If you are seeing this something went wrong, check your spelling!')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Get the weather.')
	parser.add_argument('-C','--country', help='the counrty',required=True, type=str)
	parser.add_argument('-c','--city', help='The city',required=True, type=str)
	parser.add_argument('-u','--unit', choices=['i', 'm',], help='allowed sorting types',required=True)
	parser.add_argument('-v','--verbose', action='store_true', help='verbose output',required=False)
	args = parser.parse_args()
	get_info(args.verbose, args.city, args.country, args.unit)
