import unittest
import json
from flask import Flask
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
    
    ### TESTS PARA CASOS DE EXITO

    # Verifica si la solicitud para obtener los contactos se realiza correctamente
    def test_contactos(self):
        response = self.client.get('/billetera/contactos?minumero=21345')
        self.assertEqual(response.status_code, 200)
    

    # Verifica si la solicitud para realizar el pago se da de forma correcta
    def test_pagar(self):
        response = self.client.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=100')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Pago realizado")
    

    # Verifica si se obtiene el historial correctamente
    def test_historial(self):
        response = self.client.get('/billetera/historial?minumero=123')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        
    
    ### TESTS PARA ERRORES
    
    # Verifica si al ingresar una cuenta que no existe, el servidor arroja un codigo 404
    def test_contactos_cuenta_desconocida(self):
        response = self.client.get('/billetera/contactos?minumero=999')
        self.assertEqual(response.status_code, 404)


    # Verifica si al intentar realizar el pago desde una cuenta no existente se obtiene un error 404 y se retorna el mensaje "Número no encontrado"
    def test_pagar_desde_cuenta_desconocida(self):
        response = self.client.get('/billetera/pagar?minumero=999&numerodestino=123&valor=100')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_data(as_text=True), "Número no encontrado")


    # Verifica si al intentar obtener el historial de una cuenta no existente se obtiene un error 404
    def test_historial_cuenta_desconocida(self):
        response = self.client.get('/billetera/historial?minumero=999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
