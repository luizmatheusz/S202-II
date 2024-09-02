import threading
import time
import random
from pymongo import MongoClient

# Configuração do banco de dados
connector = MongoClient("mongodb://localhost:27017")
database = connector['bancoiot']
collection = database.sensores

# Criação de sensores
sensores = [
    {'nomeSensor': 'Sensor 1', 'valorSensor': 0, 'sensorAlarmado': False},
    {'nomeSensor': 'Sensor 2', 'valorSensor': 0, 'sensorAlarmado': False},
    {'nomeSensor': 'Sensor 3', 'valorSensor': 0, 'sensorAlarmado': False},
]

# Adiciona os sensores ao banco de dados
for sensor in sensores:
    if collection.find_one({'nomeSensor': sensor['nomeSensor']}):
        print(sensor['nomeSensor'], ' já existe no banco de dados.')
        
    else:
        collection.insert_one(sensor)
        print(sensor['nomeSensor'], 'foi adicionado ao banco de dados.')

# Função que mede a temperatura ou informa o status
def medir_temperatura(nome, intervalo):
    while True:
        sensorAlarmado = collection.find_one({'nomeSensor': nome, 'sensorAlarmado': True})
        
        if sensorAlarmado:
            print(f'Atenção! Temperatura muito alta! Verificar {nome}!')
            
        else:
            temperatura = random.randint(30, 40)
            collection.update_one({'nomeSensor': nome}, {'$set': {'valorSensor': temperatura}})
            
            if temperatura > 38:
                collection.update_one({'nomeSensor': nome}, {'$set': {'sensorAlarmado': True}})
            
            print(nome, ': ', temperatura, ' Cº')
        
        time.sleep(intervalo)
        
# Instancia os sensores e inicia as threads
s1 = threading.Thread(target=medir_temperatura, args=('Sensor 1', 3))
s2 = threading.Thread(target=medir_temperatura, args=('Sensor 2', 3))
s3 = threading.Thread(target=medir_temperatura, args=('Sensor 3', 3))
s1.start()
s2.start()
s3.start()