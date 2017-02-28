import urllib
import json
import time

weatherurl = "http://api.openweathermap.org/data/2.5/weather?"
forecasturl = "http://api.openweathermap.org/data/2.5/forecast?"

APPID = open('accountdata.txt', 'r').read().strip()

places = {
            'Berlin': '2950159', 'Ueckermunde': '2820471', 'London': '2643743', 
            'Helsinki': '658225', 'Reykjavik': '3413829', 'Melbourne': '2158177', 'Moscow': '524901'
    }


def getweather(now = True):
    temperatures = {}
    dt = str(int(time.time()))
    for k,v in places.iteritems():
        if now:
            url = weatherurl + urllib.urlencode({'id': v, 'APPID': APPID})
        else:
            url = forecasturl + urllib.urlencode({'id': v, 'APPID': APPID})

        uh = urllib.urlopen(url)
        data = uh.read()
        d = json.loads(data)
        
        if now:
            temperatures[k] = [d['main']['temp_min'], d['main']['temp_max'], d['main']['temp']]
        else:
            if k not in temperatures:
                temperatures[k] = {}
            for forecast in d['list']:
                temperatures[k][forecast['dt']] = [forecast['main']['temp_min'], forecast['main']['temp_max'], forecast['main']['temp']]
    
    jsdata = json.dumps(temperatures, indent = 4)
    if now:
        if type(jsdata) == str:
            open('current/currentweather-'+dt+'.json', 'w+').write(jsdata)
    else:
        if type(jsdata) == str:
            open('future/futureweather-'+dt+'.json', 'w+').write(jsdata)

tdelta = 2340
currenttime = int(time.time())
firstwait = 10*(355 - ((currenttime - tdelta)/10 % 360))
print "sleeping", firstwait, "seconds"
print "sleeping until", time.ctime(currenttime+firstwait)
time.sleep(firstwait)
while True:
    if (currenttime - tdelta)/10 % 360 == 0:
        print "fetching weather", time.ctime(currenttime)
        getweather()
        if (currenttime - tdelta)/10 % 1080 == 0:
            print "fetching forecast"        
            getweather(False)
        time.sleep(3550)
    time.sleep(4)
    print 'fetching...'
    currenttime = int(time.time())




