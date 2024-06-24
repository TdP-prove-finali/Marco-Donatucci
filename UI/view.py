import flet as ft

#  il file view.py contiene tutte le specifiche riguardanti lo stile della GUI 


class View(ft.UserControl):

    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self.filePicker = None
        self.btn_esc = None
        self.btn_no_lettore = None
        self.btn_lettore = None
        self.txt_cliente = None
        self.btn_termina = None
        self.txt_final = None
        self.callBar = None
        self.table = None
        self.btn_fine = None
        self.btn_nome = None
        self.btn_sblocco = None
        self.btn_tacho = None
        self.btn_blocco = None
        self.btn_call = None
        self.btn_search = None
        self.txt_imei = None
        self.ddType = None
        self.btn_login = None
        self.txt_password = None
        self.txt_username = None
        self.appBar = None
        self.pr = ft.ProgressRing(width=40, height=40, stroke_width=4, bgcolor='red',
                                  color='white')
        self._page = page
        self._page.title = "Topfly applicazione installatori"
        self._title = ft.Text("Applicazione Installatori", color="red", size=24)
        self._page.horizontal_alignment = 'CENTER'
        self._page.vertical_alignment = 'CENTER'
        self._page.scroll = ft.ScrollMode.HIDDEN
        self._page.theme_mode = ft.ThemeMode.SYSTEM
        self.logo = ft.Image(
            src="/images/T_check_per_splash-removebg.png",
            width=200,
            height=100,
            fit=ft.ImageFit.CONTAIN,
        )
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self.txt_result = None
        self.txt_container = None
        self.username = None

    def load_login_interface(self):
        """Interfaccia di login (pagina iniziale)"""
        #  logo
        # self._page.auto_scroll=True
        self._page.controls.append(ft.Container(padding=ft.padding.only(top=60), content=self.logo))
        # title
        self._page.controls.append(ft.Container(ft.Text("Login", color='red', font_family='Helvetica',
                                                        weight=ft.FontWeight.BOLD,
                                                        theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                                                padding=20))
        # row1: login
        self.txt_username = ft.TextField(
            label="username",
            width=300,
            focused_border_color='red'
        )
        self._page.controls.append(ft.Container(self.txt_username, padding=10))
        self.txt_password = ft.TextField(
            label="password",
            width=300,
            focused_border_color='red',
            password=True,
            can_reveal_password=True
        )
        self._page.controls.append(ft.Container(self.txt_password, padding=10))
        self.btn_login = ft.ElevatedButton(text="Login", on_click=self.controller.handle_login,
                                           bgcolor='red', color='white', width=200)
        self._page.controls.append(ft.Container(self.btn_login, padding=20))
        #  progressRing
        self._page.controls.append(ft.Container(self.pr, padding=20))
        self.pr.visible = False
        #  output
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        row = ft.Row([self.txt_result], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row)
        self._page.update()

    def load_search_interface(self):
        """Interfaccia di ricerca tramite IMEI e caricamento immagini con QR code"""
        # AppBar
        self.appBar = ft.AppBar(title=ft.Text('Ricerca dispositivo', color='white', font_family='Helvetica',
                                              weight=ft.FontWeight.BOLD, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                bgcolor='red')
        self._page.controls.append(self.appBar)
        #  row: ricerca imei
        self.ddType = ft.Dropdown(label="Tipo di dispositivo", width=300, focused_border_color='red')
        self.controller.fillDdType()
        self._page.controls.append(ft.Container(self.ddType, padding=20))
        self.icon_qr_search = ft.IconButton(icon=ft.icons.CAMERA_ALT_ROUNDED, icon_color='red',
                                 on_click=self.controller.display_qr_dialog)
        self.txt_imei = ft.TextField(
            label="IMEI",
            width=300,
            focused_border_color='red',
            suffix=self.icon_qr_search
        )
        self._page.controls.append(ft.Container(self.txt_imei, padding=ft.padding.only(bottom=20)))
        self.btn_search = ft.ElevatedButton(text="Cerca", on_click=self.controller.handle_search,
                                            bgcolor='red', color='white', width=200,
                                            icon=ft.icons.SEARCH_ROUNDED, icon_color='white')
        self._page.controls.append(ft.Container(self.btn_search, padding=ft.padding.only(bottom=20)))
        #  progressRing

        self._page.controls.append(ft.Container(self.pr, padding=20))
        self.pr.visible = False
        #  output
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        row = ft.Row([self.txt_result], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row)
        #  Fine collaudo
        self.btn_call = ft.FloatingActionButton(text="Contatta il tecnico", icon=ft.icons.CALL_ROUNDED,
                                                on_click=self.controller.handle_call, bgcolor='red')
        self._page.controls.append(self.btn_call)
        #  File picker per il caricamento delle immagini dalla galleria
        self.filePicker = ft.FilePicker(on_result=self.controller.handle_search_qr)
        self._page.overlay.append(self.filePicker)
        self._page.update()

    def load_results_interface(self):
        """Interfaccia dei risultati della ricerca e dei comandi possibili sul tipo di dispositivo"""
        self.appBar = ft.AppBar(leading=ft.IconButton(icon=ft.icons.ARROW_BACK_ROUNDED,
                                                      icon_color='white',
                                                      on_click=self.controller.back),
                                title=ft.Text('Risultati della ricerca', color='white', font_family='Helvetica',
                                              weight=ft.FontWeight.BOLD, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                bgcolor='red',
                                actions=[ft.IconButton(icon=ft.icons.REFRESH_ROUNDED,
                                                       icon_color='white',
                                                       on_click=self.controller.refresh)])
        self._page.controls.append(self.appBar)
        #  btn blocca motore e tacho
        self.btn_blocco = ft.ElevatedButton(text="Blocca motore", disabled=True, on_click=self.controller.handle_blocco,
                                            bgcolor='red', color='white', width=200)
        self.btn_lettore = ft.ElevatedButton(text="Abilita lettore", disabled=True,
                                             on_click=self.controller.handle_lettore,
                                             bgcolor='red', color='white', width=200)
        self.btn_no_lettore = ft.ElevatedButton(text="Disabilita lettore", disabled=True,
                                                on_click=self.controller.handle_no_lettore,
                                                bgcolor='red', color='white', width=200)
        self.btn_tacho = ft.ElevatedButton(text="Tacho check", disabled=True, on_click=self.controller.handle_tacho,
                                           bgcolor='red', color='white', width=200)
        self.btn_sblocco = ft.ElevatedButton(text="Sblocca motore", disabled=True,
                                             on_click=self.controller.handle_sblocco,
                                             bgcolor='red', color='white', width=200)
        self.btn_nome = ft.ElevatedButton(text="Cambia nome", on_click=self.controller.handle_nome,
                                          bgcolor='red', color='white', width=200)
        self.btn_fine = ft.ElevatedButton(text="Termina collaudo", icon=ft.icons.DONE_ROUNDED,
                                          on_click=self.controller.handle_termina_float, bgcolor='red', color='white',
                                          width=200)
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Parametri")),
                ft.DataColumn(ft.Text("Valori"))
            ])
        container = ft.Container(padding=ft.padding.only(bottom=60), content=self.table)
        self._page.controls.append(container)
        self._page.controls.append(ft.Divider(color='red'))
        self._page.controls.append(ft.Text("Comandi", color='red', font_family='Helvetica',
                                           weight=ft.FontWeight.BOLD, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM))
        self._page.controls.append(ft.Container(self.btn_blocco, padding=10))
        self._page.controls.append(ft.Container(self.btn_sblocco, padding=10))
        self._page.controls.append(ft.Container(self.btn_lettore, padding=10))
        self._page.controls.append(ft.Container(self.btn_no_lettore, padding=10))
        self._page.controls.append(ft.Container(self.btn_tacho, padding=10))
        self._page.controls.append(ft.Container(padding=10, content=self.btn_nome))
        self._page.controls.append(ft.Container(padding=ft.padding.only(top=10, bottom=20), content=self.btn_fine))
        #  output
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        row = ft.Row([self.txt_result], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row)
        self._page.controls.append(ft.Container(self.pr, padding=ft.padding.only(top=10, bottom=40)))
        self.pr.visible = False
        self.callBar = ft.BottomAppBar(bgcolor='red',
                                       content=ft.Row(controls=[ft.Text("Hai bisogno di aiuto?\nContatta il tecnico!",
                                                                        color='white',
                                                                        font_family='Helvetica',
                                                                        weight=ft.FontWeight.BOLD,
                                                                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                                                                ft.IconButton(icon=ft.icons.CALL_ROUNDED,
                                                                              icon_color='white',
                                                                              on_click=self.controller.handle_call)
                                                                ], alignment=ft.MainAxisAlignment.CENTER))
        self._page.controls.append(self.callBar)
        self._page.update()

    def load_final_interface(self):
        """Interfaccia per il termine del collaudo (pagina finale)"""
        self.appBar = ft.AppBar(leading=ft.IconButton(icon=ft.icons.ARROW_BACK_ROUNDED,
                                                      icon_color='white',
                                                      on_click=self.controller.back),
                                title=ft.Text('Termina collaudo', color='white', font_family='Helvetica',
                                              weight=ft.FontWeight.BOLD, theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
                                bgcolor='red'
                                )
        self._page.controls.append(self.appBar)

        self.txt_final = ft.TextField(label="Note", height=200, multiline=True, min_lines=5, max_lines=5)
        self._page.controls.append(ft.Container(self.txt_final, padding=20))
        self.btn_termina = ft.ElevatedButton(text="Termina collaudo", icon=ft.icons.DONE_ROUNDED,
                                             on_click=self.controller.handle_termina, bgcolor='red', color='white',
                                             width=200)
        self.btn_call = ft.FloatingActionButton(text="Contatta il tecnico", icon=ft.icons.CALL_ROUNDED,
                                                on_click=self.controller.handle_call, bgcolor='red')
        self.txt_cliente = ft.TextField(
            label="Nome Cliente",
            width=300,
            focused_border_color='red'
        )
        self._page.controls.append(ft.Container(self.txt_cliente, padding=20))
        self._page.controls.append(ft.Container(self.btn_termina, padding=ft.padding.only(bottom=20)))
        self._page.controls.append(self.btn_call)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message), adaptive=True)
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def create_model_alert_collaudo(self):
        dlg = ft.AlertDialog(title=ft.Text("Conferma termine collaudo"),
                             content=ft.Text("Sei sicuro di voler confermare il termine del collaudo?"),
                             actions=[
                                 ft.TextButton("Sì", on_click=self.controller.handle_yes_collaudo),
                                 ft.TextButton("No", on_click=self.controller.handle_no_collaudo),
                             ],
                             actions_alignment=ft.MainAxisAlignment.END, adaptive=True)
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()
        
#  MODEL ALERT PERSONALIZZATI:

    def create_model_alert_nome(self):
        dlg = ft.AlertDialog(title=ft.Text("Cambia nome"),
                             content=ft.Text("Inserisci il nuovo nome del dispositivo:"),
                             actions=[
                                 ft.TextField(label="Nuovo nome"),
                                 ft.TextButton("Invia", on_click=self.controller.handle_send_name),
                             ],
                             actions_alignment=ft.MainAxisAlignment.END, adaptive=True)
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def create_model_alert_call(self):
        dlg = ft.AlertDialog(title=ft.Text("Contatta il tecnico"),
                             content=ft.Text("Seleziona un tecnico da contattare"),
                             actions=[
                                 ft.TextButton("Marco", on_click=self.controller.handle_call_Marco),
                                 ft.TextButton("Marisa", on_click=self.controller.handle_call_Marisa),
                             ],
                             actions_alignment=ft.MainAxisAlignment.END, adaptive=True)
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()
    
    def create_model_alert_qr(self):
        dlg = ft.AlertDialog(title=ft.Text("Carica un immagine con codice QR"),
                             content=ft.Text("Scatta una foto al codice QR e caricala per leggere i dati in automatico!"),
                             actions=[
                                 ft.TextButton("Seleziona",
                                               on_click= lambda _: self.filePicker.pick_files(allow_multiple=False, 
                                                                                            file_type=ft.FilePickerFileType.IMAGE)),
                                 ft.TextButton("Annulla", on_click=self.controller.handle_no_collaudo),
                             ],
                             actions_alignment=ft.MainAxisAlignment.END, adaptive=True)
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

