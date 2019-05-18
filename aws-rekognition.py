import csv
import boto3
import os.path

## Seleciona a imagem a ser analizada ##
while True:
    photo = input('Digite o nome da imagem: ')

    if os.path.isfile(photo):
        break

    print(f'Imagem {photo} não encontrada, favor digite uma imagem existente.')
#############################################

## Leitura da credencial cadastrada no AWS ##
with open('credentials.csv', 'r') as data:
    next(data)
    reader = csv.reader(data)

    for read in reader:
        access_key_id = read[2]
        secret_access_key = read[3]
#############################################

## Metodo para ir ao webService e efetuar a detecção dos objetos da imagem ##
def detect_labels(region, secret_access_key, access_key_id, photo, max_labels, min_confidence):
    source_bytes_photo = open(photo, 'rb') #Abre a imagem.

    #Configurações de conexão a AWS.
    rekognition = boto3.client('rekognition', 
                                region,
                                aws_secret_access_key=secret_access_key,
                                aws_access_key_id=access_key_id)

    #Comunicação a AWS passando a cadeida de bytes da imagem, 
    # o numero de retorno dos objetos reconhecidos e o nivel de acerto.
    response = rekognition.detect_labels(
        Image={
            'Bytes':bytearray(source_bytes_photo.read())
        },
        MaxLabels=max_labels,
        MinConfidence=min_confidence
    )

    return response['Labels']
#############################################

region = 'us-east-2' #Região conforme escolhido na criação da conta.
max_labels = 10 #Numero de retorno dos objetos reconhecidos.
min_confidence = 90 #nivel de acerto.

#Exibe a detecção
print(f'Analise da imagem {photo} iniciada, aguarde...')
for label in detect_labels(region, secret_access_key, access_key_id, photo, max_labels, min_confidence):
    print('{Name} - {Confidence}%'.format(**label))
print(f'Analise da imagem {photo} concluida')