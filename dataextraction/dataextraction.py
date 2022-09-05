from selenium import webdriver
import pandas as pd
import time
import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.common.by import By
from selenium.webdriver.support  import expected_conditions as EC
from dotenv import load_dotenv
import os
from webdriver_manager.chrome import ChromeDriverManager
import pymysql
def verification(lista):
    sum = 0
    for i in lista:
        for j in i:
            if j!='0':
                sum= sum+1
    if (sum > 0):
        return True
    return False

def countNonzeros(lista):
    sum = 0
    for i in range (0,len(lista)):
        if lista[i] != '0':
            sum = sum+1
    return sum


def create_conecction():
    return (pymysql.connect(
        host="146.83.216.229", port=8080, user="root",
        passwd="YcQOiyxi2I", db="wordpress")
    )

def local_con():
    return (pymysql.connect(
        host="localhost", port=3306, user="root",
        passwd="", db="logros")
    )

def update_verfification():
    date = datetime.now()



def sendData():
    df = pd.read_excel (r'output_01092022.xlsx')

    for i in range(0,len(df)):
        con = local_con()
        cur = con.cursor()
        cur.execute ("INSERT INTO `logros` (codigo_escuela,numero_estudiantes,fecha_script,fecha_inicio,fecha_fin,numero_semana,suma_minutos,skills_mejoradas,suma_skill_sin_avance,maximo_ejercicios,maximo_skills) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(df['codigo_escuela'][i],df['numero_estudiantes'][i],df['fecha_script'][i],df['fecha_script'][i],df['fecha_script'][i],df['numero_semana'][i],df['suma_minutos'][i],df['skills_mejoradas'][i],df['suma_skill_sin_avance'][i],df['maximo_ejercicios'][i],df['maximo_skills'][i]))
        con.commit()
        con.close()
    

usr = os.getenv('KHAN_EMAIL')
psw = os.getenv('KHAN_PASSWORD')


#def extractdata():
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')


#driver = webdriver.Chrome(driver_path, chrome_options=options)

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
#driver.get("https://www.khanacademy.org/teacher/class/SNFD6RAV/overview/activity")
#time.sleep(4)


cursos = ["PUFMSN2Y","B8R2QYTZ","SK8AVS6T","SNFD6RAV","HGCVH5GU","M5NC6Q59","8RN7Y26W","4BDG3KYZ","PE4HKFPJ","FUDFPMJP","PR8XE9NN","KZFDPGFC","9A52ZEQY","WVHHCPNT","Z5GBVS8T","EUX423PU","VFQDGQ7C"]
#cursos = ["PUFMSN2Y"]
table = []
#stand_by : 
fecha = datetime.datetime.now()
first_row = True
item = 0
meses = ['agosto','septiembre']#el ultimo es el mes actual
dias = [31,3]#el ultimo valor es la fecha actual, útltimas semanas hasta hoy
año = '2022'#el último es el valor del año actual
fechas = []
for j in range(len(meses)):
    i = 1
    while (i <=dias[j]):
        fechas.append(meses[j]+" "+str(i)+", "+año)
        i=i+7

fechas = fechas[4:6]
columnas = ['codigo_escuela','numero_estudiantes','fecha_script','intervalo','numero_semana','suma_minutos','skills_mejoradas','suma_skill_sin_avance','maximo_ejercicios','maximo_skills']
df = pd.DataFrame(columns=columnas)




for i in cursos:
    driver.get("https://www.khanacademy.org/teacher/class/"+i+"/overview/activity")
    if (first_row):
        driver.find_element(By.XPATH,'//*[@id="uid-login-form-0-wb-id-identifier-field"]').send_keys("")
        driver.find_element(By.XPATH,'//*[@id="uid-labeled-text-field-1-wb-id-field"]').send_keys("")
        driver.find_element(By.XPATH,'//*[@id="app-shell-root"]/div/main/div[2]/div/div[3]/section[2]/div/div/form/button').click()


    time.sleep(2)
    #wdw(driver,10).until(EC.element_to_be_clickable(By.XPATH,'//*[@id="class-shell"]/div/div[1]/div[1]/div[1]/div/h4'))
    #driver.find_element(By.XPATH,'')

    escuela = wdw(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="class-shell"]/div/div[1]/div[1]/div[1]/div/h4'))).text

    #escuela = driver.find_element(By.XPATH,'//*[@id="class-shell"]/div/div[1]/div[1]/div[1]/div/h4').text
    print("escuela:",escuela)

    for k in range(0,len(fechas)-1):
        if(first_row):
            item = 5
        else:
            item = 6
        driver.find_element(By.XPATH,'//*[@id="class-shell"]/div/div[2]/div[3]/div[2]/div[1]/div/div/button').click()
        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div['+ str(item)+']').click()

        wdw(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="start-date-field"]')))
        for l in range (0,30):#borrar espacios start-date-field
            driver.find_element(By.XPATH,'//*[@id="start-date-field"]').send_keys(Keys.BACKSPACE)
            
        driver.find_element(By.XPATH,'//*[@id="start-date-field"]').send_keys(str(fechas[k]))

        wdw(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="end-date-field"]')))
        for l in range (0,30):#borrar espacios start-date-field
            driver.find_element(By.XPATH,'//*[@id="end-date-field"]').send_keys(Keys.BACKSPACE)
            
        driver.find_element(By.XPATH,'//*[@id="end-date-field"]').send_keys(str(fechas[k+1]))


        #cargar fechas
        wdw(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div/div/div/div[2]/div/div/span[3]'))).click()
        wdw(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div/div/div/div/div[3]/button'))).click()

        tipo = wdw(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="class-shell"]/div/div[2]/div[3]/div[2]/div[1]/div/div/button/span'))).text
        table =  wdw(driver,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="class-shell"]/div/div[2]/div[3]/div[2]/div[3]/div/div/div/div'))).text
        tab = table.split("\n")
        columnas = [tab[0],tab[1],tab[2],tab[3]]
        df4 = pd.DataFrame(columns = columnas)
        output=[tab[i:i + 4] for i in range(4, len(tab), 4)]

        first_row = False
        if verification(output) :
            for j in range (0,len(output)):
                df4.loc[j] = output[j]
            sumaMinutos = df4['TOTAL DE MINUTOS DE APRENDIZAJE'].astype(int).sum()
            maxEjercicio = df4['TOTAL DE MINUTOS DE APRENDIZAJE'].max()
            maxSkills = df4['HABILIDADES MEJORADAS'].max()
            sumaSkills = df4['HABILIDADES MEJORADAS'].astype(int).sum()
            sumaWOProgress = df4['HABILIDADES SIN AVANCE'].astype(int).sum()
            time.sleep(2)
        else:
            sumaMinutos = 0
            sumaSkills = 0
            sumaWOProgress=0
        df=df.append({'codigo_escuela' : escuela , 'numero_estudiantes': countNonzeros(df4['TOTAL DE MINUTOS DE APRENDIZAJE']) ,'fecha_script' : fecha,'intervalo' : tipo,'numero_semana':k+23, 'suma_minutos': sumaMinutos,'skills_mejoradas':sumaSkills,'suma_skill_sin_avance':sumaWOProgress,'maximo_ejercicios':maxEjercicio,'maximo_skills':maxSkills} , ignore_index=True)


df.to_excel("datos/output_01092022.xlsx")
sendData()
time.sleep(10)