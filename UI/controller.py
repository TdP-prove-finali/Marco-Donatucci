import pathlib
import time
import flet as ft


#  il file controller.py gestisce le interazioni tra gli oggetti della view 
#  e funge da interfaccia tra input dell'utente e la classe model


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDdType(self):
        """Metodo per il fill del Dropdown menu contenente i tipi di dispositivi"""
        self._view.ddType.options.append(ft.dropdown.Option(key='1', text="Topflytech T8806+R"))
        self._view.ddType.options.append(ft.dropdown.Option(key='2', text="Topflytech T8803"))
        self._view.ddType.options.append(ft.dropdown.Option(key='3', text="Topflytech T8803+"))
        self._view.ddType.options.append(ft.dropdown.Option(key='4', text="Topflytech T8803+E"))
        self._view.ddType.options.append(ft.dropdown.Option(key='5', text="Topflytech TLW2-12BL"))
        self._view.ddType.options.append(ft.dropdown.Option(key='6', text="Topflytech PioneerX100"))
        self._view.ddType.options.append(ft.dropdown.Option(key='7', text="Teltonika FMB920"))
        self._view.ddType.options.append(ft.dropdown.Option(key='8', text="Teltonika FMB140"))
        self._view.ddType.options.append(ft.dropdown.Option(key='9', text="Teltonika FMB640"))
        self._view.ddType.options.append(ft.dropdown.Option(key='10', text="Teltonika FMC150"))
        self._view.ddType.options.append(ft.dropdown.Option(key='11', text="Teltonika FMC640"))
        self._view.ddType.options.append(ft.dropdown.Option(key='12', text="Queclink GV58CEU"))
        self._view.ddType.options.append(ft.dropdown.Option(key='13', text="Queclink GV355CEU"))
        self._view.ddType.options.append(ft.dropdown.Option(key='14', text="Queclink GV350CEU"))

    def handle_search(self, e):
        """Metodo per la ricerca di un dispositivo tramite IMEI"""
        #  il metodo viene chiamato al click del bottone 'cerca'
        self._view.txt_result.clean()
        #  appare il progress ring
        self._view.pr.visible = True
        self._view.update_page()
        imei = self._view.txt_imei.value
        #  controlli di validità dell'imei inserito
        imei = str(imei).replace(" ", "")
        if not imei.isdigit():
            self._view.create_alert("IMEI errato! Riprova")
            self._view.txt_imei.value = ''
            self._view.pr.visible = False
            self._view.update_page()
            return
        if self._model.connection is None:
            self._view.create_alert("Accedi con username e password")
            self._view.txt_imei.value = ''
            self._view.pr.visible = False
            self._view.update_page()
            return
        if self._view.ddType.value is None or self._view.ddType.value == '':
            self._view.create_alert("Seleziona il tipo di dispositivo")
            self._view.txt_imei.value = ''
            self._view.pr.visible = False
            self._view.update_page()
            return
        #  viene settato il device sul model e vengono cercati tutti i dati
        search_start_time = time.time()
        self._model.setDevice(imei, self._view.ddType.value)
    
        #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
        tempo_di_attesa = 10
        start_time = time.time()
        while self._model.device is None:
            if time.time() - start_time >= tempo_di_attesa:
                break
            else:
                pass
        search_end_time = time.time()
        print(f"Algoritmo di ricerca: {search_end_time-search_start_time}")
        #  controlli sull'output 
        if self._model.device is None:
            self._view.txt_result.controls.append(
                ft.Text("Dispositivo non trovato! controlla l'IMEI e il tipo di dispositivo e riprova", color='red'))
            self._view.pr.visible = False
            self._view.update_page()
            return
        #  il progress ring sparisce e viene caricata l'interfaccia dei risultati
        drop = self._view.ddType.value
        self._view.pr.visible = False
        self._view._page.controls.clear()
        self._view.load_results_interface()
        self._view.update_page()
        blocco = ['1', '2', '3', '4', '5', '7', '8', '12', '14']
        tacho = ['9', '11', '13']
        lettore = ['8', '12', '14']
        #  vengono abilitati solo i bottoni dei comandi possibili sul tipo di dispositivo cercato
        if blocco.__contains__(drop):
            self._view.btn_blocco.disabled = False
            self._view.btn_sblocco.disabled = False
        if tacho.__contains__(drop):
            self._view.btn_tacho.disabled = False
        if lettore.__contains__(drop):
            self._view.btn_lettore.disabled = False
            self._view.btn_no_lettore.disabled = False
        for row in self._model.device.displayData():
            self._view.table.rows.append(row)
        # self._view.txt_result.controls.append(ft.Text(self._model.device.__str__()))
        self._view.update_page()

    def handle_login(self, e):
        """Metodo per effettuare il login con username e password"""
        #  il metodo viene chiamato al click del bottone 'login'
        #  appare il progress ring
        self._view.pr.visible = True
        self._view.txt_result.controls.clear()
        self._view.update_page()
        #  controlli sulla connessione e sui valori inseriti nei textfields
        if self._model.connection is None:
            self._model.setConnection()
        if self._view.txt_username.value is None or self._view.txt_username.value == '':
            self._view.create_alert("Inserisci username e password!")
            self._view.pr.visible = False
            self._view.update_page()
            return
        if self._view.txt_password.value is None or self._view.txt_password.value == '':
            self._view.create_alert("Inserisci username e password!")
            self._view.pr.visible = False
            self._view.update_page()
            return
        username = self._view.txt_username.value.replace(" ", "")
        password = self._view.txt_password.value.replace(" ", "")
        #  viene settato il token della connessione 
        login_start_time = time.time()
        self._model.setToken(username, password)
        #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
        tempo_di_attesa = 10
        start_time = time.time()
        while self._model.connection.token is None:
            if time.time() - start_time >= tempo_di_attesa:
                break
            else:
                pass
        login_end_time = time.time()
        print(f"Algoritmo di autenticazione: {login_end_time-login_start_time}")
        if self._model.connection.token is None:
            self._view.txt_result.controls.append(
                ft.Text("Accesso non riuscito! controlla username e password e riprova", color='red'))
            self._view.pr.visible = False
            self._view.update_page()
            return
        #  sparisce il progress ring e viene caricata l'interfaccia di ricerca
        self._view.pr.visible = False
        self._view.username = self._view.txt_username.value
        self._view.txt_username.value = ''
        self._view.txt_password.value = ''
        self._view._page.controls.clear()
        self._view.load_search_interface()
        self._view.update_page()

    def back(self, e):
        """Metodo per tornare alla pagina di ricerca (pagina principalmente utilizzata nell'app)"""
        self._view._page.controls.clear()
        self._view.load_search_interface()
        self._view.update_page()

    def refresh(self, e):
        """Metodo per ricaricare i dati nella pagina dei risultati"""
        drop = self._view.ddType.value
        self._view._page.controls.clear()
        self._view.update_page()
        self._model.setDevice(self._model.device.uid, self._model.device.selected_type)
        self._view.load_results_interface()
        self._view.update_page()
        blocco = ['1', '2', '3', '4', '5', '7', '8', '12', '14']
        tacho = ['9', '11', '13']
        lettore = ['8', '12', '14']
        if blocco.__contains__(drop):
            self._view.btn_blocco.disabled = False
            self._view.btn_sblocco.disabled = False
        if tacho.__contains__(drop):
            self._view.btn_tacho.disabled = False
        if lettore.__contains__(drop):
            self._view.btn_lettore.disabled = False
            self._view.btn_no_lettore.disabled = False
        for row in self._model.device.displayData():
            self._view.table.rows.append(row)
        # self._view.txt_result.controls.append(ft.Text(self._model.device.__str__()))
        self._view.update_page()

    def handle_blocco(self, e):
        """Metodo per inoltrare il comando di blocco motore"""
        #  il metodo viene eseguito al click del bottone 'blocca motore'
        self._view.txt_result.clean()
        #  appare il progress ring
        self._view.pr.visible = True
        self._view.update_page()
        #  viene chiamato il metodo del model
        var = self._model.doBlocco()
        #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
        tempo_di_attesa = 10
        start_time = time.time()
        while not var:
            if time.time() - start_time >= tempo_di_attesa:
                break
            else:
                pass
        #  controlli sull'output e return del risultato
        if var:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text(f"Risposta comando: {var}", color='green'))
            self._view.update_page()
            return
        else:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text("Blocco non riuscito! Riprova!", color='red'))
            self._view.update_page()
            return

    def handle_tacho(self, e):
        """Metodo per inoltrare il comando di Tacho check"""
        #  il metodo viene eseguito al click del bottone 'tacho check'
        self._view.txt_result.clean()
        # appare il progress ring
        self._view.pr.visible = True
        self._view.update_page()
        #  viene chiamato il metodo del model
        tacho_start_time = time.time()
        var = self._model.doTacho()
        #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
        tempo_di_attesa = 10
        start_time = time.time()
        while not var:
            if time.time() - start_time >= tempo_di_attesa:
                break
            else:
                pass
        tacho_end_time = time.time()
        print(f"Algoritmo comando tacho: {tacho_end_time-tacho_start_time}")
        #  controlli sull'output e return del risultato
        if var:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text(f"Risposta comando: {var}"))
            self._view.update_page()
            return
        else:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text("Invio comando non riuscito! Riprova!", color='red'))
            self._view.update_page()
            return

    def handle_sblocco(self, e):
        """Metodo per inoltrare il comando di sblocco motore"""
        #  il metodo viene eseguito al click del bottone 'Sblocca motore'
        self._view.txt_result.clean()
        #  appare il progress ring
        self._view.pr.visible = True
        self._view.update_page()
        #  viene chiamato il metodo del model
        var = self._model.doSblocco()
        #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
        tempo_di_attesa = 10
        start_time = time.time()
        while not var:
            if time.time() - start_time >= tempo_di_attesa:
                break
            else:
                pass
        #  controlli sull'output e return del risultato
        if var:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text(f"Risposta comando: {var}", color='green'))
            self._view.update_page()
            return
        else:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text("Sblocco non riuscito! Riprova!", color='red'))
            self._view.update_page()
            return

    def handle_nome(self, e):
        #  crea il model alert per il cambio del nome 
        self._view.create_model_alert_nome()
        self._view.update_page()

    def handle_termina_float(self, e):
        #  carica l'interfaccia finale al click del bottone 'termina collaudo'
        self._view._page.controls.clear()
        self._view.load_final_interface()
        self._view.update_page()

    def handle_termina(self, e):
        #  viene eseguito al click del bottone 'termina' nella pagina finale, apre il model alert per terminare
        if self._view.txt_cliente.value is None or self._view.txt_cliente.value == '':
            self._view.create_alert("Inserisci il nome del cliente per continuare!")
            self._view.update_page()
            return
        self._view.create_model_alert_collaudo()
        self._view.update_page()

    def handle_yes_collaudo(self, e):
        #  viene eseguito al click del bottone 'si' nel model alert della pagina finale
        self._view._page.dialog.open = False
        self._view.update_page()
        self._view._page.controls.clear()
        if self._model.device is None:
            self._view.create_alert("Nessun dispositivo collaudato, cerca il dispositivo!")
            self._view.load_search_interface()
            self._view.update_page()
            return
        try:
            #  inoltra la mail con i dati del collaudo all'azienda
            mail_start_time = time.time()
            self._model.doEmail(self._view.username, self._view.txt_final.value, self._view.txt_cliente.value)
        except:
            self._view.create_alert("Problemi riscontrati nel termine collaudo, contatta il tecnico!")
            self._view.load_search_interface()
            self._view.update_page()
            return
        #  output e caricamento interfaccia di ricerca
        mail_end_time = time.time()
        print(f"Algoritmo email: {mail_end_time-mail_start_time}")
        self._view.create_alert("Collaudo terminato")
        self._model.device = None
        self._view.load_search_interface()
        self._view.update_page()

    def handle_no_collaudo(self, e):
        #  viene eseguito al click del bottone 'no' nel model alert del termine del collaudo
        self._view._page.dialog.open = False
        self._view.update_page()

    def handle_send_name(self, e):
        #  viene eseguito al click del bottone 'invia' nel model alert per il cambio del nome
        self._view._page.dialog.open = False
        self._view.update_page()
        nome = self._view._page.dialog.actions[0].value
        #  chiama il metodo del model per cambiare il nome
        name_start_time = time.time()
        result = self._model.doName(nome)
        #  output
        name_end_time = time.time()
        print(f"Algoritmo cambio nome: {name_end_time-name_start_time}")
        if result:
            self._view.create_alert("Nome dispositivo cambiato")
        else:
            self._view.create_alert("Cambio nome non andato a buon fine, riprova!")
        self._view.update_page()

    def handle_lettore(self, e):
        """Metodo per inoltro del comando lettore on"""
        #  viene eseguito al click del bottone 'abilita lettore'
        self._view.txt_result.clean()
        self._view.pr.visible = True
        self._view.update_page()
        #  esegue il metodo del model
        var = self._model.doLettoreOn()
        #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
        tempo_di_attesa = 10
        start_time = time.time()
        while not var:
            if time.time() - start_time >= tempo_di_attesa:
                break
            else:
                pass
        #  controlli sull'output e return del risultato
        if var or self._view.ddType == '12':
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text(f"Risposta comando: {var}", color='green'))
            self._view.update_page()
            return
        else:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text("Comando non riuscito! Riprova!", color='red'))
            self._view.update_page()
            return

    def handle_no_lettore(self, e):
        """Metodo per l'inoltro del comando lettore off"""
        #  viene eseguito al click del bottone 'disabilita lettore'
        self._view.txt_result.clean()
        self._view.pr.visible = True
        self._view.update_page()
        #  esegue il metodo del model
        var = self._model.doLettoreOff()
        #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
        tempo_di_attesa = 10
        start_time = time.time()
        while not var:
            if time.time() - start_time >= tempo_di_attesa:
                break
            else:
                pass
        #  controlli sull'output e return del risultato
        if var or self._view.ddType == '12':
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text(f"Risposta comando: {var}", color='green'))
            self._view.update_page()
            return
        else:
            self._view.pr.visible = False
            self._view.txt_result.controls.append(ft.Text("Comando non riuscito! Riprova!", color='red'))
            self._view.update_page()
            return

    def handle_call(self, e):
        #  apre il model alert per la scelta del tecnico da chiamare (tra Marco e Marisa) al click del bottone 
        #  per chiamare il tecnico
        self._view.create_model_alert_call()

    def handle_call_Marco(self, e):
        #  esegue il metodo per effettuare la telefonata
        self._model.doCall('+390000000000')

    def handle_call_Marisa(self, e):
        #  esegue il metodo per effettuare la telefonata
        self._model.doCall('+390000000000')

    def display_qr_dialog(self, e):
        #  al click del bottone con l'icona della fotocamera nel campo di ricerca apre il model alert per selezionare 
        #  i file dalla galleria con il file picker
        self._view.create_model_alert_qr()
        self._view.update_page()

    def handle_search_qr(self, e: ft.FilePickerResultEvent):
        """Metodo per eseguire una ricerca tramite scansione di un QR code da FilePicker"""
        self._view._page.dialog.open = False
        #  disabilito i comandi di ricerca per non creare altri thread di ricerca 
        self._view.btn_search.disabled = True
        self._view.icon_qr_search.disabled = True
        self._view.txt_result.controls.clear()
        self._view.pr.visible = True
        self._view.update_page()
        #  controlli sul filepicker
        if self._view.filePicker.result is not None and self._view.filePicker.result.files is not None:
            var = self._view.filePicker.result.files
            #  esegue il metodo del model
            qr_start_time = time.time()
            imei = self._model.read_qr_code(str(var[0].path))
            #  timer di attesa massima in caso il device rimanga None per problemi di input o connessione
            tempo_di_attesa = 10
            start_time = time.time()
            while not imei:
                if time.time() - start_time >= tempo_di_attesa:
                    break
                else:
                    pass
            qr_end_time = time.time()
            print(f"Algoritmo ricerca con codice qr: {qr_end_time-qr_start_time}")
            #  controlli sull'output e return dei risultati
            if imei:
                self._view.pr.visible = False
                self._view.txt_imei.value = imei
                self._view.btn_search.disabled = False
                self._view.icon_qr_search.disabled = False
                self._view.update_page()
                return
            else:
                self._view.pr.visible = False
                self._view.txt_result.controls.append(ft.Text("Codice QR non trovato! Riprova", color='red'))
                self._view.btn_search.disabled = False
                self._view.icon_qr_search.disabled = False
                self._view.update_page()
                return
        #  riabilitazione delle funzioni di ricerca
        self._view.btn_search.disabled = False
        self._view.pr.visible = False
        self._view.icon_qr_search.disabled = False
        self._view.update_page()
        
