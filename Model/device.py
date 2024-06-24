from dataclasses import dataclass
import flet as ft

#  la classe device è la superclasse da cui derivano tutte le altre classi device più specifiche
# contiene le informazioni e i metodi comuni a tutti i dispositivi, le altre sottoclassi sono invece più specifiche


@dataclass
class Device:
    uid: str
    itemId: int
    name: str
    position: (float, float)
    device_status: bool
    object_status: bool
    selected_type: str

    def defineStatus(self, boolean):
        """Trasforma un boolean in stringa, utile per l'output di testo dei campi bool"""
        if boolean == 1:
            return "On"
        elif boolean == 0:
            return "Off"
        else:
            return None

    def __str__(self):
        return (f"Dati dispositivo:\n"
                f"IMEI: {self.format_attribute_str(self.uid)}\n"
                f"Nome: {self.format_attribute_str(self.name)}\n"
                f"Status: {self.format_attribute_str(self.defineStatus(self.device_status))}\n"
                f"Posizione: {self.format_attribute_str(self.position)}\n"
                f"Accensione: {self.format_attribute_str(self.defineStatus(self.object_status))}\n")

    def displayData(self):
        """Costruisce una lista di righe contenenti oggetti ft.DataRow da inserire nella DataTable della
        pagina dei risultati della ricerca"""
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("IMEI", weight=ft.FontWeight.W_400)),
                    ft.DataCell(ft.Text(self.uid) if self.uid is not None else ft.Text("Sensore non trovato!", color='red'))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("nome", weight=ft.FontWeight.W_400)),
                    ft.DataCell(ft.Text(self.name) if self.name is not None else ft.Text("Sensore non trovato!", color='red'))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Status dispositivo", weight=ft.FontWeight.W_400)),
                    ft.DataCell(ft.Text(self.defineStatus(self.device_status)) if self.device_status is not None else ft.Text("Sensore non trovato!", color='red'))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Posizione", weight=ft.FontWeight.W_400)),
                    ft.DataCell(ft.Text(self.position) if self.position is not None else ft.Text("Sensore non trovato!", color='red'))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Accensione", weight=ft.FontWeight.W_400)),
                    ft.DataCell(ft.Text(self.defineStatus(self.object_status)) if self.object_status is not None else ft.Text("Sensore non trovato!", color='red'))
                ]
            )
        ]
        return rows

    def format_attribute_str(self, value):
        """Trasforma un valore None o -1 in stringa, utile per l'output di testo dei sensori non trovati"""
        if value is None:
            return f'Sensore non trovato!'
        elif value == -1:
            return f'Sensore non trovato!'
        else:
            return f'{value}'
