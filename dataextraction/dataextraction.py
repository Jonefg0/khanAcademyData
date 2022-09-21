from selenium import webdriver
import pandas as pd
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv, find_dotenv
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
from datetime import date, datetime


load_dotenv(find_dotenv())
USER = os.environ.get('KHAN_EMAIL')
PSW = os.environ.get('KHAN_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get("DB_NAME")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_TABLE = os.environ.get("DB_TABLE")
DB_STUDENT_TABLE = os.environ.get("DB_STUDENT_TABLE")
COURSES = os.environ.get('COURSES')
username = os.environ.get('BROWSERSTACK_USERNAME')
accessKey = os.environ.get('BROWSERSTACK_ACCESS_KEY')

def verification(lista):
    sum = 0
    for i in lista:
        for j in i:
            if j != '0':
                sum = sum+1
    if (sum > 0):
        return True
    return False


def countNonzeros(lista):
    sum = 0
    for i in range(0, len(lista)):
        if lista[i] != '0':
            sum = sum+1
    return sum


def create_connection():
    return (pymysql.connect(
        host=DB_HOST, port=int(DB_PORT), user=DB_USER,
        passwd=DB_PASSWORD, db=DB_NAME)
    )


def sendStudentData(df):
    for i in range(0, len(df)):
        con = create_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO `"+DB_STUDENT_TABLE+"` (codigo_escuela, codigo_curso, fecha_script, fecha_inicio, fecha_fin, numero_semana, nombre_estudiante, total_minutos, habilidades_mejoradas, habilidades_sin_avance ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (df['escuela'][i], df['curso'][i], df['fecha_script'][i], df['fecha_inicio'][i], df['fecha_fin'][i], df['numero_semana'][i], df['ESTUDIANTE'][i], df['TOTAL DE MINUTOS DE APRENDIZAJE'][i], df['HABILIDADES MEJORADAS'][i], df['HABILIDADES SIN AVANCE'][i]))
        con.commit()
        con.close()

def sendData(df):
    for i in range(0, len(df)):
        con = create_connection()
        cur = con.cursor()
        cur.execute("INSERT INTO `"+DB_TABLE+"` (codigo_escuela,numero_estudiantes,fecha_script,fecha_inicio,fecha_fin,numero_semana,suma_minutos,skills_mejoradas,suma_skill_sin_avance,maximo_ejercicios,maximo_skills) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (df['codigo_escuela'][i], df['numero_estudiantes'][i], df['fecha_script'][i], df['fecha_inicio'][i], df['fecha_fin'][i], df['numero_semana'][i], df['suma_minutos'][i], df['skills_mejoradas'][i], df['suma_skill_sin_avance'][i], df['maximo_ejercicios'][i], df['maximo_skills'][i]))
        con.commit()
        con.close()


def date_to_string(date: datetime):
    m = {
        '1': 'enero',
        '2': 'febrero',
        '3': 'marzo',
        '4': 'abril',
        '5': 'mayo',
        '6': 'junio',
        '7': 'julio',
        '8': 'agosto',
        '9': 'septiembre',
        '10': 'octubre',
        '11': 'noviembre',
        '12': 'diciembre',
    }
    month = date.month
    str_month = m[str(month)]
    string_date = str_month + ' ' + str(date.day) + ', ' + str(date.year)
    return string_date


def string_to_date(string_date: str):
    m = {
        'enero': '1',
        'febrero': '2',
        'marzo': '3',
        'abril': '4',
        'mayo': '5',
        'junio': '6',
        'julio': '7',
        'agosto': '8',
        'septiembre': '9',
        'octubre': '10',
        'noviembre': '11',
        'diciembre': '12',
    }
    split_date = string_date.split(' ')

    day = int(str(split_date[1])[0:-1])
    month = int(m[split_date[0]])
    year = int(split_date[2])

    return date(year, month, day)


def update_verfification(last_date, actual_date: datetime, initial_month):
    dates_w = []  # wednesday in year
    dates_m = []  # mondays in year
    actual_month = actual_date.month
    months = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
              "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30,
            31, 30, 31]  # duración de los meses
    year = actual_date.year
    first_time = True
    # 0: enero, 1:febrero, 2: marzo, 3: abril, 4: mayo,....
    actual_month = actual_date.month

    for j in range((actual_month - initial_month)):  # partir desde mes de inicio
        real_month = j + initial_month
        if first_time:  # primer viernes del mes de inicio
            i = 11
            first_time = False
        else:
            i = 7 - (days[real_month - 1] - (i))  # primer viernes del mes
        while (i <= days[real_month]):
            if (real_month == (actual_month-1)):
                if i >= actual_date.day:
                    break
            # parte desde mes de inicio
            dates_w.append(months[j+initial_month] +
                           " "+str(i)+", " + str(year))
            i = i+7
            #print("i quedó en:", i)
        i = i-7
    first_time = True
    for k in range((actual_month - initial_month)):
        real_month = k + initial_month
        if first_time:  # primer lunes del año
            i = 7
            first_time = False
        else:
            i = 7 - (days[real_month - 1] - (i))  # primer lunes del mes
        while (i <= days[real_month]):
            if (real_month == (actual_month-1)):
                if i > actual_date.day:
                    break
            # parte desde mes de inicio
            dates_m.append(months[k+initial_month] +
                           " "+str(i)+", " + str(year))
            i = i+7
            #print("i quedó en:", i)
        i = i-7
    dates_m = dates_m[:-1]
    if (str(type(last_date)) == "<class 'datetime.date'>"):
        diff = actual_date-last_date
        if (diff.days < 7):  # just last week data
            return [dates_m[-1:], dates_w[-1:]]
        else:
            week_count = 7
            count = 0
            while (week_count <= diff.days):
                week_count += 7
                count += 1
            return [dates_m[-count:], dates_w[-count:]]
    else:
        return [dates_m, dates_w]


def last_week_number():
    con = create_connection()
    cur = con.cursor()
    cur.execute("SELECT MAX(numero_semana) FROM "+DB_TABLE+"")
    con.commit()
    con.close()
    aux = cur.fetchone()

    if (aux[0] == None):
        return 0
    else:
        return int(aux[0])

def last_week_date():
    con = create_connection()
    cur = con.cursor()
    cur.execute("SELECT max(fecha_fin) FROM "+DB_TABLE+"")
    con.commit()
    con.close()
    aux = cur.fetchone()

    if (aux[0] == None):
        return ""
    else:
        return (aux[0])


def browserStack_driver():
    desired_cap = {
        "os": "Windows",
        "os_version": "10",
        "browser": "Chrome",
        "browser_version": "latest",
        'bstack:options': {
            "resolution": "1920x1080",

        },
    }

    return webdriver.Remote(command_executor='https://'+username+':'+accessKey+'@hub-cloud.browserstack.com/wd/hub', desired_capabilities=desired_cap)


def local_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    # options.add_argument('--headless')

    #driver = webdriver.Chrome(driver_path, chrome_options=options)

    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


def run_script():

    driver = local_driver()
    driver.maximize_window()
    lwn = last_week_number()

    cursos = COURSES.split(',')
    table = []
    # stand_by :
    fecha = datetime.today()
    first_row = True
    item = 0
    fechas_l, fechas_v = update_verfification(last_week_date(), date.today(), 2)
    columnas = ['codigo_escuela', 'numero_estudiantes', 'fecha_script', 'fecha_inicio', 'fecha_fin', 'numero_semana',
                'suma_minutos', 'skills_mejoradas', 'suma_skill_sin_avance', 'maximo_ejercicios', 'maximo_skills']
    df = pd.DataFrame(columns=columnas)

    for i in cursos:
        df_actual = pd.DataFrame(columns=columnas)
        driver.get("https://www.khanacademy.org/teacher/class/" +
                   i+"/overview/activity")
        time.sleep(2)
        if (first_row):
            driver.find_element(
                By.XPATH, '//*[@id="uid-login-form-0-wb-id-identifier-field"]').send_keys(USER)
            driver.find_element(
                By.XPATH, '//*[@id="uid-labeled-text-field-1-wb-id-field"]').send_keys(PSW)
            driver.find_element(
                By.XPATH, '//*[@id="app-shell-root"]/div/main/div[2]/div/div[3]/section[2]/div/div/form/button').click()

        time.sleep(3)
        # wdw(driver,10).until(EC.element_to_be_clickable(By.XPATH,'//*[@id="class-shell"]/div/div[1]/div[1]/div[1]/div/h4'))
        # driver.find_element(By.XPATH,'')
        print("INICIANDO SCRAPING")
        codigo_escuela = wdw(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="class-shell"]/div/div[1]/div[1]/div[1]/div/h4'))).text
        escuela_y_curso = codigo_escuela.split(':')[0]
        escuela_curso_array = escuela_y_curso.split('-')
        escuela = escuela_curso_array[0]
        curso = escuela_curso_array[1]+escuela_curso_array[2]

        #escuela = driver.find_element(By.XPATH,'//*[@id="class-shell"]/div/div[1]/div[1]/div[1]/div/h4').text
        time.sleep(5)
        for k in range(0, len(fechas_v)):
            if (first_row):
                item = 5
            else:
                item = 6
            driver.find_element(
                By.XPATH, '//*[@id="class-shell"]/div/div[2]/div[3]/div[2]/div[1]/div/div/button').click()
            driver.find_element(
                By.XPATH, '/html/body/div[2]/div/div/div[' + str(item)+']').click()
            fecha_inicio = string_to_date(fechas_l[k])
            fecha_fin = string_to_date(fechas_v[k])
            wdw(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="start-date-field"]')))
            time.sleep(2)
            for l in range(0, 30):  # borrar espacios start-date-field
                try:
                    driver.find_element(
                        By.XPATH, '//*[@id="start-date-field"]').send_keys(Keys.BACKSPACE)
                except:
                    print("error")

            driver.find_element(
                By.XPATH, '//*[@id="start-date-field"]').send_keys(str(fechas_l[k]))

            wdw(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="end-date-field"]')))
            for l in range(0, 30):  # borrar espacios start-date-field
                driver.find_element(
                    By.XPATH, '//*[@id="end-date-field"]').send_keys(Keys.BACKSPACE)

            driver.find_element(
                By.XPATH, '//*[@id="end-date-field"]').send_keys(str(fechas_v[k]))

            # cargar fechas
            wdw(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div/div/div/div/div[2]/div/div/span[3]'))).click()
            wdw(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div/div/div/div/div[3]/button'))).click()

            tipo = wdw(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="class-shell"]/div/div[2]/div[3]/div[2]/div[1]/div/div/button/span'))).text
            table = wdw(driver, 2).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="class-shell"]/div/div[2]/div[3]/div[2]/div[3]/div/div/div/div'))).text
            tab = table.split("\n")
            columnas = [tab[0], tab[1], tab[2], tab[3]]
            columnas_df = ['escuela', 'curso', 'fecha_script', 'fecha_inicio',
                           'fecha_fin', 'numero_semana', tab[0], tab[1], tab[2], tab[3]]
            df_estudiantes = pd.DataFrame(columns=columnas_df)
            df4 = pd.DataFrame(columns=columnas)
            output = [tab[i:i + 4] for i in range(4, len(tab), 4)]
            output_aux = output
            first_row = False
            if verification(output):
                for j in range(0, len(output)):
                    df4.loc[j] = output[j]
                    output_aux[j].insert(0, escuela)
                    output_aux[j].insert(1, curso)
                    output_aux[j].insert(2, fecha)
                    output_aux[j].insert(3, fecha_inicio)
                    output_aux[j].insert(4, fecha_fin)
                    output_aux[j].insert(5, k+lwn+1)
                for j in range(0, len(output_aux)):
                    df_estudiantes.loc[j] = output_aux[j]
                sendStudentData(df_estudiantes)
                sumaMinutos = df4['TOTAL DE MINUTOS DE APRENDIZAJE'].astype(
                    int).sum()
                maxEjercicio = df4['TOTAL DE MINUTOS DE APRENDIZAJE'].max()
                maxSkills = df4['HABILIDADES MEJORADAS'].max()
                sumaSkills = df4['HABILIDADES MEJORADAS'].astype(int).sum()
                sumaWOProgress = df4['HABILIDADES SIN AVANCE'].astype(
                    int).sum()
            else:
                sumaMinutos = 0
                sumaSkills = 0
                sumaWOProgress = 0
            df = df.append({'codigo_escuela': escuela_y_curso, 'numero_estudiantes': countNonzeros(df4['TOTAL DE MINUTOS DE APRENDIZAJE']), 'fecha_script': fecha, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'numero_semana': k +
                           lwn + 1, 'suma_minutos': sumaMinutos, 'skills_mejoradas': sumaSkills, 'suma_skill_sin_avance': sumaWOProgress, 'maximo_ejercicios': maxEjercicio, 'maximo_skills': maxSkills}, ignore_index=True)
            df_actual = df_actual.append({'codigo_escuela': escuela_y_curso, 'numero_estudiantes': countNonzeros(df4['TOTAL DE MINUTOS DE APRENDIZAJE']), 'fecha_script': fecha, 'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin, 'numero_semana': k + lwn +
                                          + 1, 'suma_minutos': sumaMinutos, 'skills_mejoradas': sumaSkills, 'suma_skill_sin_avance': sumaWOProgress, 'maximo_ejercicios': maxEjercicio, 'maximo_skills': maxSkills}, ignore_index=True)
        sendData(df_actual)
        print("se terminó de enviar:", codigo_escuela)
    df.to_excel('datos/output_'+str(date.today())+'.xlsx')

    print("Script terminado, tenga buen día")
    driver.close()