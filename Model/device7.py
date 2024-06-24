from dataclasses import dataclass

from Model.device import Device
import flet as ft


@dataclass
class Device7(Device):
    uid: str
    itemId: int
    name: str
    position: (float, float)
    device_status: bool
    object_status: bool
    battery: float
    total_km: float
    blocco: bool
    selected_type: str

    def __str__(self):
        return super().__str__() + (f"Batteria: {self.format_attribute_str(self.battery)} V\n"
                                    f"Km totali: {self.format_attribute_str(self.total_km)} km\n"
                                    f"Sensore di blocco: {self.format_attribute_str(self.defineStatus(self.blocco))}")

    def displayData(self):
        rows = super().displayData()
        rows.extend(
            [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Batteria", weight=ft.FontWeight.W_400)),
                        ft.DataCell(ft.Text(str(self.battery) + "V")if self.battery is not None else ft.Text("Sensore non trovato!", color='red'))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Km totali", weight=ft.FontWeight.W_400)),
                        ft.DataCell(ft.Text(str(self.total_km) + "Km")if self.total_km > 0 else ft.Text("Sensore non trovato!", color='red'))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Sensore di blocco", weight=ft.FontWeight.W_400)),
                        ft.DataCell(ft.Text(self.defineStatus(self.blocco))if self.blocco is not None else ft.Text("Sensore non trovato!", color='red'))
                    ]
                )
            ]
        )
        return rows
