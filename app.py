from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


class Operacion:
    def __init__(self, numero_destino, valor):
        self.numero_destino = numero_destino
        self.fecha = datetime.now()
        self.valor = valor


class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operaciones = []

    def historial(self):
        return self.operaciones

    def pagar(self, destino, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            operacion = Operacion(destino, valor)
            self.operaciones.append(operacion)
            for cuenta in BD:
                if cuenta.numero == destino:
                    cuenta.saldo += valor
                    break
            
            return "Pago realizado"
        else:
            return "Saldo insuficiente"


# Inicializamos la base de datos en memoria
BD = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]


@app.route('/billetera/contactos', methods=['GET'])
def contactos():
    minumero = request.args.get('minumero')
    for cuenta in BD:
        if cuenta.numero == minumero:
            contactos_info = []
            for contacto in cuenta.contactos:
                for c in BD:
                    if c.numero == contacto:
                        contactos_info.append(f"{contacto}: {c.nombre}")
            return '<br>'.join(contactos_info), 200
            #return jsonify(cuenta.contactos)
    return "Número no encontrado", 404


@app.route('/billetera/pagar', methods=['GET'])
def pagar():
    minumero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = int(request.args.get('valor'))
    for cuenta in BD:
        if cuenta.numero == minumero:
            return cuenta.pagar(numerodestino, valor), 200
    return "Número no encontrado", 404


@app.route('/billetera/historial', methods=['GET'])
def historial():
    minumero = request.args.get('minumero')
    for cuenta in BD:
        if cuenta.numero == minumero:
            return jsonify(["Saldo de " + str(cuenta.nombre) + ": " + str(cuenta.saldo)])
    return "Número no encontrado", 404




if __name__ == '__main__':
    app.run(debug=True, port=8080)
