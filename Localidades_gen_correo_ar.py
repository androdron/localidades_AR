#!/usr/bin/python3
from requests import Request, Session
import unicodedata
import re
import pandas as pd
import csv
import os

print('Este script genera un csv con las localidades de las provincias de Argentina a partir del\
formulario presente en la pagina de correo argentino en la parte de "consulta de codigo postal".\
El metodo para la extraccion de los mismos puede cambiar en el caso de que el portal de correo argentino\
sufra cambios. Este metodo fue desarrollado en Agosto de 2018 por Andrey Musatov \
(Ministerio de Produccion de La Nacion)')

cwd = str(os.getcwd())
pwd = str(cwd+'/localidades_cp_maestro.csv')
if os.path.isfile(pwd) == True:
    os.system('rm %s'%(pwd))
prov_cod_correo = {"Ciudad Autonoma de Buenos Aires":"C","Buenos Aires":"B",
                  "Catamarca":"K","Chaco":"H","Chubut":"U","Cordoba":"X",
                  "Corrientes":"W","Entre Rios":"E","Formosa":"P","Jujuy":"Y",
                  "La Pampa":"L","La Rioja":"F","Mendoza":"M","Misiones":"N",
                   "Neuquen":"Q","Rio Negro":"R","Salta":"A","San Juan":"J",
                   "San Luis":"D","Santa Cruz":"Z","Santa Fe":"S",
                   "Santiago del Estero":"G","Tierra del Fuego":"V","Tucuman":"T"}

pattern = r'"id":"\d*","nombre":".*?","cp":"\d*"'

with open('localidades_cp.csv','a') as f:
    for key in prov_cod_correo:
        s = Session()
        headres = {'Host': 'www.correoargentino.com.ar',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-GB,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.correoargentino.com.ar/formularios/cpa',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '60',
            'Cookie': 'has_js=1',
            'Connection': 'keep-alive',
            'DNT': '1'}
        url = 'https://www.correoargentino.com.ar/sites/all/modules/custom/ca_forms/api/wsFacade.php'
        req = Request('POST', url, headers=headres)#, data=data)
        prepped = req.prepare()
        prepped.body = 'action=localidades&localidad=none&calle=&altura=&provincia=%s'%(prov_cod_correo[key])
        resp = s.send(prepped)
        text = str(resp.content).replace('\\\\u00d1','Ñ')
        for val in re.findall(pattern,text):
            print(key.join('""')+","+val,file=f)

def multi_replace(df,cols,char,rep_char):
    for col in cols:
        df[col] = [e.replace(char,rep_char,1) for e in df[col].astype('str')]
df = pd.read_csv('localidades_cp.csv',header=None,names=['provincia','id','localidad','cp'])
multi_replace(df,['cp'],'cp:"','')
multi_replace(df,['id'],'id:"','')
multi_replace(df,['localidad'],'nombre:"','')
multi_replace(df,['cp','localidad','id'],'"','')

dtmast = {'provincia':['Buenos Aires', 'Catamarca', 'Chaco', 'Chubut', 'Cordoba', 'Corrientes', 'Entre Rios', 'Formosa', 'Jujuy', 'La Pampa', 'La Rioja', 'Mendoza', 'Misiones', 'Neuquen',\
                  'Rio Negro', 'Salta', 'San Juan', 'San Luis', 'Santa Cruz', 'Santa Fe', 'Santiago del Estero', 'Tierra del Fuego', 'Tucuman', 'Ciudad Autonoma de Buenos Aires'],\
          'id_prov_mstr':['06', '10', '22', '26', '14', '18', '30', '34', '38', '42', '46', '50', '54', '58', '62', '66', '70', '74', '78', '82', '86', '94', '90', '02']}
dfprov = pd.DataFrame.from_dict(dtmast, orient='columns')
dfprov['id_prov_mstr'] = dfprov['id_prov_mstr'].astype('object')
local_con_id = pd.merge(df,dfprov,on='provincia')
df_caba = pd.read_csv('tabla_ciudad_bsas.csv',dtype={'id_provincia':'object'}).rename\
(columns={'cod':'cp','cod_description':'localidad','id_provincia':'id_prov_mstr','provincia_descripcion':'provincia'})
df_final = pd.concat([local_con_id,df_caba],sort=False).sort_values(by=['id_prov_mstr'])
df_final.loc[df_final['id_prov_mstr'] == '02', 'localidad'] = 'Ciudad Autonoma de Buenos Aires'
df_final.loc[df_final['id_prov_mstr'] == '02', 'id'] = '5001'
df_final.to_csv(pwd,index=False,quotechar='"',quoting=csv.QUOTE_ALL)
os.system('rm %s/localidades_cp.csv'%(cwd))
print('Se ha generado el csv')
