import flet as ft
from Model.model import Model
from UI.view import View
from UI.controller import Controller


def main(page: ft.Page):
    #  secondo documentazione flet il modo per far funzionare il metodo launch_url è usarlo nel main 
    #  quindi ho dovuto necessariamente scrivere qui il metodo per effettuare le chiamate e poi chiamarlo nel model
    def telefono(numero):
        # Costruisce l'URL con il numero di telefono precompilato
        tel_url = f'tel:{numero}'
        # Apre l'URL nel browser
        page.launch_url(tel_url)

    #  Inizializzazione delle classi necessarie 
    my_model = Model(telefono)  # assegno il metodo telefono 
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    #  Caricamento pagina di partenza (Login)
    my_view.load_login_interface()


ft.app(target=main, assets_dir='assets', upload_dir="uploads")  # assets è la cartella che contiene le immagini 
# del progetto, upload quella che conterrà le immagini caricate dall'utente per la scansione del qr code
