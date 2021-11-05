import socket
import threading
import sys
import pickle
import os

class Servidor():
    port_ = int(input("Introduce tu puerto: "))

    def __init__(self, host=socket.gethostname(), port=port_):
        self.nicks = []
        self.clientes = []
        self.sock = socket.socket()
        self.sock.bind((str(host), int(port)))
        self.sock.listen(20)
        self.sock.setblocking(False)

        aceptar = threading.Thread(target=self.aceptarC)
        procesar = threading.Thread(target=self.procesarC)

        aceptar.daemon = True
        aceptar.start()

        procesar.daemon = True
        procesar.start()

        while True:
            msg = input('SALIR = Q\n')
            if msg == 'Q':
                print("**** TALOGOOO *****")
                self.sock.close()
                sys.exit()
            elif msg == 'p': # si el usuario escribe por el servidor una p muestra los nicks que hay guardados
                print(self.nicks)
            else:
                pass

    def broadcast(self, msg, cliente):
        for c in self.clientes:
            try:
                if c != cliente:
                    c.send(msg)
            except:
                self.clientes.remove(c)

    def aceptarC(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                print(f"\nConexion aceptada via {conn}\n")
                conn.setblocking(False)
                self.clientes.append(conn)
            except:
                pass

    def procesarC(self):
        print("Procesamiento de mensajes iniciado")
        while True:
            if len(self.clientes) > 0:
                for c in self.clientes:
                    try:
                        data = c.recv(32)
                        if data:
                            self.broadcast(data, c)
                            if ": " not in pickle.loads(data): #hace una comprobacion siempre que recibe cualquier dato para ver si es un nick o un mensaje del cliente
                                self.nicks.append(pickle.loads(data)) #carga los nicks en la lista
                            else:
                                print(pickle.loads(data)) #envia el mensaje y se visualiza desde el servidor
                                f = open("u22056511.txt", "w") #la a es para activar el modo append de escritura en el fichero.
                                f.write(pickle.loads(data) + "\n")# escribe en el fichero correspondiente
                                f.close() #cierra el fichero
                    except:
                        pass

s = Servidor()
