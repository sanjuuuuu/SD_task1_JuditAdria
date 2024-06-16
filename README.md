# SD_Task1_JuditAdrià

## Requisits

Per a poder executar l'aplicació es necessari tenir instalat això:

- Python 3.6 o superior
- `grpcio` i `grpcio-tools`
- `redis`
- `pika`
- Un servidor Redis en execució
- Un servidor RabbitMQ en execució:
- sudo docker rm rabbitmq 
- sudo docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

Podeu instal·lar les dependències necessàries mitjançant pip3 dintre del entorn virtual:

```sh
pip3 install grpcio grpcio-tools redis pika
```

## Arxius del Projecte

- `chat.proto`: Definició del servei gRPC.
- `chat_pb2.py` i `chat_pb2_grpc.py`: Fitxers generats a partir de `chat.proto`.
- `server.py`: Implementació del servidor gRPC, que inclou la lògica del servidor de noms i el message broker.
- `client.py`: Implementació del client gRPC per interactuar amb el servidor i altres clients.

## Generació dels Fitxers gRPC

Abans de poder executar el servidor i el client, heu de generar els fitxers gRPC a partir de la definició del servei `chat.proto`. Executeu la següent comanda:

```sh
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
```

## Executar el Servidor

Per executar el servidor, obriu un terminal, entreu al entorn virtual i executeu:

```sh
python3 server.py
```

El servidor començarà a escoltar a la port `50051`.

## Executar el Client

Per executar el client, obriu un altre terminal, torneu a entrar al entorn virtual i executeu:

```sh
python3 client.py
```

Se us demanarà el vostre nom d'usuari, es important escollir 1 dels 4 noms d'usuari disponibles. Després, apareixerà el menú per escollir les opcions:

1. Connectar-se a un xat privat
2. Subscriure’s a un xat grupal
3. Descobrir a un xat actiu
4. Accedir al canal d'insults

### Opcions del Client

#### 1. Connectar-se a un Xat Privat

Introduïu l'ID del xat al qual voleu connectar-vos. Si l'usuari està disponible, es connectarà i podreu començar a enviar missatges privats.

#### 2. Subscriure’s a un Xat Grupal

Introduïu l'ID del grup al qual voleu subscriure-vos. Un cop subscrits, podreu enviar i rebre missatges grupals.

#### 3. Descobrir Xats Actius

El client enviarà una sol·licitud per descobrir a un altre client que estigui disponible

#### 4. Accedir al Canal d'Insults

El client es connectarà a una cua de RabbitMQ per enviar i rebre insults. Els insults es distribueixen de manera que cada missatge arribi a un client diferent.

