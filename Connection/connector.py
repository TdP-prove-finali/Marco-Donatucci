import smtplib
import webbrowser
from urllib.parse import urlparse, parse_qs
from wialon import Wialon, WialonError  # libreria per la connessione alla piattaforma dell'azienda, presa da github
import re
import requests


#  il file connector.py contiene tutti i metodi che si occupano di stabilire connessioni http e fare richieste ai server
# gli url di richiesta, i parametri e le flag sono stati impostati secondo documentazione ufficiale dei server


class Connection:
    def __init__(self):
        self.token = None
        self.wialon_api = None

    def getConnection(self, imei):
        """Stabilisce una connessione al server ed effettua la ricerca del dispositivo"""
        try:
            self.wialon_api = Wialon()
            result = self.wialon_api.token_login(  # il login tramite token è necessario per ottenere il session id
                token=self.token)
            self.wialon_api.sid = result['eid']  # ottiene il session id che servirà ad autenticare qualsiasi richiesta

            search_spec = {
                'itemsType': 'avl_unit',
                'propName': 'sys_unique_id',
                'propValueMask': imei,  # codice di identificazione univoco del dispositivo
                'sortType': 'sys_name'
            }

            search_result = self.wialon_api.search_items(spec=search_spec)
            if len(search_result['items']) == 0:
                return None
            item_data = search_result['items'][0]
            #  ATTIVAZIONE UNITA!
            if item_data['act'] == 0:
                activation = self.wialon_api.active_unit(item_data['id'])
                # le unità disattivate vengono automaticamente
                # attivate durante la ricerca (su richiesta dell'azienda)
                item_data['act'] = activation['active']
            self.wialon_api.core_logout()
            return item_data  # ottengo un dizionario con tutti i valori dei sensori dell'unità cercata
        except WialonError as e:
            print(e)

    def setToken(self, new_url):
        """Estrae il token dall'url di reindirizzamento e lo assegna all'attributo token"""
        parsed_url = urlparse(new_url)
        query_params = parse_qs(parsed_url.query)
        access_token = query_params.get('access_token', [None])[0]
        self.token = access_token
        #  il token verrà utilizzato per ottenere il session id per qualisasi richiesta al server

    def getTokenRequest(self, username, password):
        """Permette di effettuare il login tramite username e password"""
        url = 'https://hst-api.wialon.com/oauth/authorize.html?lang=en'
        data = {
            'response_type': 'token',
            'wialon_sdk_url': 'https://hst-api.wialon.com',
            'success_uri': '',
            'login_uri': 'https://tracking.topflyiot.com/login.html',
            'client_id': 'wialon',
            'redirect_uri': 'https://tracking.topflyiot.com/login.html',
            'access_type': '-1',
            'activation_time': '0',
            'duration': '0',
            'flags': '7',
            'login': username,
            'passw': password
        }
        headers = {
            'origin': 'https://tracking.topflyiot.com',
            'content-type': 'application/x-www-form-urlencoded',
            'refer': 'https://tracking.topflyiot.com/'
        }
        response = requests.post(url, data=data, headers=headers)  # richiesta http post
        if response.status_code == 200:
            get_url = response.request.url
            # se la richiesta è andata a buon fine la risposta contiene un url di reindirizzamento con dentro un campo
            # token, il metodo setToken estrae il token e lo assegna al valore self
            self.setToken(get_url)
        else:
            return None

    def executeCommand(self, command, param, itemId):
        """Metodo di esecuzione di comandi sull'unità"""
        params = {
            "itemId": itemId,  # id dell'unità
            "commandName": command,  # nome del comando (tutti i nomi sono stati forniti dall'azienda)
            "linkType": "tcp",
            "param": param,  # parametri aggiuntivi (anche forniti dall'azienda)
            "timeout": 10,
            "flags": 0
        }
        try:
            result = self.wialon_api.token_login(
                token=self.token)  # procedura di autenticazione
            self.wialon_api.sid = result['eid']
            command_result = self.wialon_api.execute_cmd(params=params)  # metodo di esecuzione dei comandi dell'api
            if len(command_result) == 0:
                return True  # esecuzione comando andato a buon fine
            else:
                return None  # esecuzione comando fallita
        except WialonError as e:
            print(e)

    def update_name(self, itemId, name):
        """Metodo che permette di cambiare il nome di un unità"""
        try:
            result = self.wialon_api.token_login(
                token=self.token)  # procedura di autenticazione
            self.wialon_api.sid = result['eid']
            command_result = self.wialon_api.update_name(itemId, name)   # metodo per il cambio del nome dell'api
            if command_result['nm'] == name:
                return True
            else:
                return False
        except WialonError as e:
            print(e)

    def send_email(self, message):
        """Metodo per inoltrare una mail al termine del collaudo"""
        subject = "Conferma collaudo dispositivo"
        encoded_subject = f"Subject: {subject}\n\n"

        # Concatena il soggetto e il messaggio decodificato
        full_message = encoded_subject + message

        # Codifica il messaggio completo in UTF-8
        encoded_message = full_message.encode('utf-8')
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login('marco.donatucci02@gmail.com', 'akwm zcgl lkep ffvh')
        server.sendmail('marco.donatucci02@gmail.com', 'marco.donatucci02@gmail.com', encoded_message)
        # l'e-mail serve all'azienda per tenere traccia dei collaudi che avvengono, la mail viene quindi mandata da 
        # un indirizzo email a se stesso
        server.quit()



