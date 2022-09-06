from datetime import date, datetime


ultima_fecha = date(2022,8,26)
fecha_hoy = date.today()
print ("fecha:", date.today())
dif = (fecha_hoy - ultima_fecha).days
print("diferencia entre fechas:", dif)

date_string = "21 June, 2018"
print("date_string =", date_string)



def date_to_string(date:datetime):
    m = {
        '1':'enero',
        '2':'febrero',
        '3':'marzo',
        '4':'abril',
        '5':'mayo',
        '6':'junio',
        '7':'julio',
        '8':'agosto',
        '9':'septiembre',
        '10':'octubre',
        '11':'noviembre',
        '12':'diciembre',
    }
    month = date.month
    str_month = m[str(month)]
    string_date = str_month + ' ' + str(date.day) + ', ' + str(date.year)
    return string_date

def string_to_date(string_date:str):
    m = {
        'enero':'1',
        'febrero':'2',
        'marzo':'3',
        'abril':'4',
        'mayo':'5',
        'junio':'6',
        'julio':'7',
        'agosto':'8',
        'septiembre':'9',
        'octubre':'10',
        'noviembre':'11',
        'diciembre':'12',
    }
    split_date = string_date.split(' ')
    print("split_date", split_date)
    day = int(str(split_date[1])[0:-1])
    month = int(m[split_date[0]])
    year = int(split_date[2])

    return date(year,month,day)

    
def update_verfification(last_date, actual_date:datetime):
    print("last_date type: ", type(last_date))
    if (str(type(last_date)) ==  "<class 'datetime.date'>"):
        dates = [date_to_string(last_date), date_to_string(actual_date)]
    else:
        #arreglo desde inicio de cursos, se restan 2 meses para no contar enero y febrero
        actual_month = actual_date.month 
        months = ["enero","febrero","marzo","abril","mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre"]
        days = [31,28,31,30,31,30,31,31,30,31,30,31]
        year = actual_date.year
        dates = []
        first_time = True
        initial_month = 2 #0: enero, 1:febrero, 2: marzo, 3: abril, 4: mayo,....
        actual_month = actual_date.month 

        for j in range((actual_month - initial_month)):#partir desde mes de inicio
            real_month = j + initial_month
            if first_time: #primer viernes del mes de inicio
                i = 4
                first_time = False
            else :
                i = 7 - (days[real_month - 1] - (i)) #primer viernes del mes
                #print("el siguiente mes parte en i",i)
            while (i <=days[real_month]):
                if (real_month == (actual_month-1)):
                    if i >=  actual_date.day:
                        break
                dates.append(months[j+initial_month]+" "+str(i)+", "+ str(year))#parte desde mes de inicio
                i=i+7
                #print("i quedó en:", i)
            i=i-7
    return dates




print(string_to_date("agosto 8, 2022"))



#date_object = datetime.strptime(date_string, "%d %B, %Y")
#print("date_object =", date_object)

#ultima_fecha_string = ultima_fecha.strftime("%d %B, %Y")
#print("ultima_fecha_string =",ultima_fecha_string)