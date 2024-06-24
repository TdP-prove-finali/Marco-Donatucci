from Connection import device_DAO, connector
from PIL import Image
import re
import cv2
import numpy as np


#  il file model.py si occupa dell'elaborazione dei dati e dei comandi, funge anche da interfaccia tra il controller
#  e le connessioni


class Model:
    def __init__(self, telefono):
        self.device = None
        self.connection = None
        self.telefono = telefono

    def setDevice(self, imei, selected_type):
        self.device = device_DAO.getDevice(imei, selected_type, self.connection)
        
    def setConnection(self):
        self.connection = connector.Connection()

    def setToken(self, username, password):
        self.connection.getTokenRequest(username, password)

    def doBlocco(self):
        """Metodo per l'inoltro del comando blocca motore"""
        #  definizione dei parametri (nomi e messaggi forniti dall'azienda)
        msg = {
            '1': 'relay,1#',
            '2': 'relay,1#',
            '3': 'relay,1#',
            '4': 'relay,1#',
            '5': 'relay,1#',
            '7': 'setdigout 1',
            '8': 'setdigout 11',
            '12': 'AT+GTDOS=gv58ceu,0,1,1,1,0,0,0,,1,0,5,,,,FFFF$',
            '14': 'AT+GTDOS=gv350ceu,0,5,1,1,0,0,0,,2,0,0,0,0,,3,0,0,0,0,,4,0,0,0,0,,5,0,0,0,0,,1,0,5,,,,FFFF$'
        }
        name = 'Blocco Motore'
        itemId = self.device.itemId
        var_msg = msg.get(self.device.selected_type)
        #  esecuzione del comando con il metodo della classe connection
        result = self.connection.executeCommand(name, var_msg, itemId)
        return result

    def doTacho(self):
        """Metodo per l'inoltro del comando tacho check"""
        #  definizione dei parametri (nomi e messaggi forniti dall'azienda)
        msg = {
            '9': 'tachocheck',
            '11': 'tachocheck',
            '13': 'AT+GTTTR=gv355ceu,10,,,,,,,,FFFF$',
        }
        name = {
            '9': 'check',
            '11': 'tacho',
            '13': 'tacho check'
        }
        itemId = self.device.itemId
        var_name = name.get(self.device.selected_type)
        var_msg = msg.get(self.device.selected_type)
        #  esecuzione del comando con il metodo della classe connection
        result = self.connection.executeCommand(var_name, var_msg, itemId)
        if result:
            try:
                output = self.connection.getConnection(self.device.uid)['prms']['text']['v']
            except KeyError as e:
                output = True
            return output
        else:
            return False
        

    def doSblocco(self):
        """Metodo per l'inoltro del comando sblocca motore"""
        #  definizione dei parametri (nomi e messaggi forniti dall'azienda)
        msg = {
            '1': 'relay,0#',
            '2': 'relay,0#',
            '3': 'relay,0#',
            '4': 'relay,0#',
            '5': 'relay,0#',
            '7': 'setdigout 0',
            '8': 'setdigout 00',
            '12': 'AT+GTDOS=gv58ceu,0,1,1,0,0,0,0,,1,0,5,,,,FFFF$',
            '14': 'AT+GTDOS=gv350ceu,0,5,1,0,0,0,0,,2,0,0,0,0,,3,0,0,0,0,,4,0,0,0,0,,5,0,0,0,0,,1,0,5,,,,FFFF$'
        }
        name = 'Sblocco Motore'
        itemId = self.device.itemId
        var_msg = msg.get(self.device.selected_type)
        #  esecuzione del comando con il metodo della classe connection
        result = self.connection.executeCommand(name, var_msg, itemId)
        if result:
            try:
                output = self.connection.getConnection(self.device.uid)['prms']['text']['v']
            except KeyError as e:
                try:
                    output = self.connection.getConnection(self.device.uid)['prms']['msg']['v']
                except KeyError as e:
                    output = True
            return output
        else:
            return False

    def doName(self, nome):
        """Metodo per l'inoltro del comando cambia nome"""
        itemId = self.device.itemId
        #  esecuzione del comando con il metodo della classe connection
        result = self.connection.update_name(itemId, nome)
        return result

    def doCall(self, numero):
        """Metodo per effettuare chiamate"""
        self.telefono(numero)  # self.telefono non è un dato ma un metodo definito nel main 

    def defineType(self):
        """Metodo per ottenere il numero del tipo di dispositivo salvato nel model in base al nome"""
        types = {
            '1': 'Topflytech T8806+R',
            '2': 'Topflytech T8803',
            '3': 'Topflytech T8803+',
            '4': 'Topflytech T8803+E',
            '5': 'Topflytech TLW2-12BL',
            '6': 'Topflytech PioneerX100',
            '7': 'Teltonika FMB920',
            '8': 'Teltonika FMB140',
            '9': 'Teltonika FMB640',
            '10': 'Teltonika FMC150',
            '11': 'Teltonika FMC640',
            '12': 'Queclink GV58CEU',
            '13': 'Queclink GV355CEU',
            '14': 'Queclink GV350CEU'
        }
        return types[self.device.selected_type]

    def doEmail(self, username, note, cliente):
        """Metodo per l'inoltro di email"""
        #  Formattazione del messaggio
        message = (f"Nome account: {username}\n"
                   f"Nome cliente: {cliente}\n"
                   f"Tipo dispositivo: {self.defineType()}\n\n"
                   f"{self.device.__str__()}\n\n"
                   f"Note: {note}")
        #  Utilizzo del metodo della classe connection per inoltrare la mail
        self.connection.send_email(message)

    def doLettoreOn(self):
        """Metodo per l'inoltro del comando lettore on"""
        #  definizione dei parametri (nomi e messaggi forniti dall'azienda)
        msg = {
            '8': '  setparam 11700:1',
            '12': 'AT+GTIDA=gv58ceu,2,1,1,,120,7,60,,,,1,0,0,0,,0,,,FFFF$',
            '14': 'AT+GTIDA=gv350ceu,2,1,1,,20,7,20,1,0,1,1,0,0,0,0,0,,,FFFF$'
        }
        name = {
            '8': 'Lettore inserito',
            '12': 'Lettore abilitato',
            '14': 'Lettore abilitato'
        }
        itemId = self.device.itemId
        var_name = name.get(self.device.selected_type)
        var_msg = msg.get(self.device.selected_type)
        #  esecuzione del comando con il metodo della classe connection
        result = self.connection.executeCommand(var_name, var_msg, itemId)
        if result:
            try:
                output = self.connection.getConnection(self.device.uid)['prms']['text']['v']
            except KeyError as e:
                output = True
            return output
        else:
            return False

    def doLettoreOff(self):
        """Metodo per l'inoltro del comando lettore off"""
        #  definizione dei parametri (nomi e messaggi forniti dall'azienda)
        msg = {
            '8': '  setparam 11700:0',
            '12': 'AT+GTIDA=gv58ceu,0,1,1,,120,7,60,,,,1,0,0,0,,0,,,FFFF$',
            '14': 'AT+GTIDA=gv350ceu,0,1,1,,20,7,20,1,0,1,1,0,0,0,0,0,,,FFFF$'
        }
        name = {
            '8': 'Lettore disinserito',
            '12': 'Lettore disabilitato',
            '14': 'Lettore disabilitato'
        }
        itemId = self.device.itemId
        var_name = name.get(self.device.selected_type)
        var_msg = msg.get(self.device.selected_type)
        #  esecuzione del comando con il metodo della classe connection
        result = self.connection.executeCommand(var_name, var_msg, itemId)
        if result:
            try:
                output = self.connection.getConnection(self.device.uid)['prms']['text']['v']
            except KeyError as e:
                output = True
            return output
        else:
            return False

    def read_qr_code(self, path):
        """Metodo per la lettura del qr code a partire da un file immagine"""
        # Apro l'immagine dal percorso usando Pillow
        image = Image.open(path)

        # Converto l'immagine nel formato utilizzato da opencv (BGR) utilizzando un array numpy
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Uso la classe QRCodeDetector per rilevare e decodificare il QR code
        qr_detector = cv2.QRCodeDetector()
        data, points, _ = qr_detector.detectAndDecode(open_cv_image)

        # Se vengono rilevati i punti in cui è presente un codice qr viene restituito l'imei estratto
        if points is not None:
            return self.extract_imei(data)
        else:
            return None

    @staticmethod
    def extract_imei(decoded_results):
        """Metodo per la ricerca del codice identificativo univoco del dispositivo (IMEI) nel testo di output del server"""
        imei_match = re.search(r'IMEI:(\d+)', decoded_results)  # Cerca il campo IMEI 
        if imei_match:
            return imei_match.group(1)  # Restituisce solo il numero IMEI
        return 'IMEI non riconosciuto!'