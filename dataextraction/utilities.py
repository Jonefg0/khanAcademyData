from datetime import date, datetime
import locale


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


def update_verfification(last_date, actual_date:datetime):
    if (type(last_date) == datetime):
        if (actual_date > last_date):
            delta = actual_date - last_date
    else:
        #arreglo desde inicio de cursos, se restan 2 meses para no contar enero y febrero
        months = ["enero","febrero","marzo","abril","mayo","junio","julio","septiembre","octubre","noviembre","diciembre"]
        days = [31,28,31,30,31,30,31,31,30,31,30,31]
        year = actual_date.year
        dates = []
        for j in range(len(months)-2):
            i = 1
            while (i <days[j]):
                dates.append(months[j+2]+" "+str(i)+", "+ str(year))
                i=i+7





#date_object = datetime.strptime(date_string, "%d %B, %Y")
#print("date_object =", date_object)

#ultima_fecha_string = ultima_fecha.strftime("%d %B, %Y")
#print("ultima_fecha_string =",ultima_fecha_string)