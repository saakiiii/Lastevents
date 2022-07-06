import datetime


def calculateHour(posttime, postdate):
        print(posttime)
        print(postdate)
        now = datetime.datetime.now()
        currenttime = now.strftime("%H:%M")
        currentdate = now.strftime("%d-%m-%Y")
        currenttime = currenttime.split(':')
        currentdate = currentdate.split('-')
        currenthour = int(currenttime[0])
        currentday = int(currentdate[0])
        currentmonth = int(currentdate[1])
        currentyear = int(currentdate[-1])
        currentminute = int(currenttime[1])
        posttime = posttime.split(":")
        postdate = postdate.split("-")
        postday = int(postdate[0])
        postmonth = int(postdate[1])
        postyear = int(postdate[-1])
        posthour = int(posttime[0])
        postminute = int(posttime[1])
        monthWith31days = [1, 3, 5, 7, 8, 10, 12]
        monthWith30days = [4, 6, 9, 11]
        monthWith28or29days = [2]
        val = None
        if currentyear == postyear:
            if currentmonth == postmonth:
                if (currentday - postday) == 1:
                    timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=1)
                    timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=0)
                    val = timehour  - timehour1           
                if (currentday - postday) == 0:
                    timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=0)
                    timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=0)
                    val = timehour - timehour1            
            else:
                if (currentmonth - postmonth) == 1:  
                    if postmonth in monthWith31days:
                        if currentday - postday == -30:
                            # val = currenthour - posthour
                            timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=1)
                            timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=0)
                            val = timehour  - timehour1            
                            if val == 0:
                                val = 24 - (currenthour + posthour)

                            if val < 0:
                                val = -(val)
                    elif postmonth in monthWith30days:
                        if currentday - postday == -29:
                            # val = currenthour - posthour
                            print(currenthour)
                            print(posthour)
                            # val = (currenthour + posthour) - ((24 - posthour) + (24 - currenthour) - 1)
                            timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=0)
                            timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=1)
                            val = timehour  - timehour1       

                    elif postmonth in monthWith28or29days:
                        if currentday - postday == -28 or currentday - postday == -27:
                            # val = currenthour - posthour
                            timehour = datetime.timedelta(hours=currenthour, minutes=currentminute, seconds=0, days=0)
                            timehour1 = datetime.timedelta(hours=posthour, minutes=postminute, seconds=0, days=1)
                            val = timehour  - timehour1           
        
        if val == None:
            return None
        if len(str(val)) > 8:
            print("jh")
            pass
        else:
           time_split = str(val).split(":") 
           if time_split[0] == '0':
               print(time_split[1]+'min ago')
               return time_split[1] + 'min ago'  
           else: 
            print(time_split[0]+"h ago")
            return time_split[0] + "h ago"
    
# calculateHour(posttime="11:12", postdate="02-07-2022")

import re

str = "hello<>world."
val = re.sub(r'[@_!#$%^&*()<>?/\|}{~:]', "", str)
print(str[0:-1])
print(val)