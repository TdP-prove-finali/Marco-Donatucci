from dataclasses import dataclass

from Model.device import Device
import flet as ft


@dataclass
class Device10(Device):
    uid: str
    itemId: int
    name: str
    position: (float, float)
    device_status: bool
    object_status: bool
    battery: float
    rpm: float
    fuel_percentage: float
    total_km: float
    water_temp: float
    blocco: bool
    selected_type: str

    def __str__(self):
        return super().__str__() + (f"Batteria: {self.format_attribute_str(self.battery)} V\n"
                                    f"Giri motore: {self.format_attribute_str(self.rpm)} rpm\n"
                                    f"Percentuale carburante: {self.format_attribute_str(self.fuel_percentage)}%\n"
                                    f"Km totali: {self.format_attribute_str(self.total_km)} km\n"
                                    f"Temperatura acqua motore: {self.format_attribute_str(self.water_temp)} °C\n"
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
                        ft.DataCell(ft.Text("Giri motore", weight=ft.FontWeight.W_400)),
                        ft.DataCell(ft.Text(str(self.rpm) + "rpm")if self.rpm is not None else ft.Text("Sensore non trovato!", color='red'))
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Percentuale carburante", weight=ft.FontWeight.W_400)),
                        ft.DataCell(ft.Text(str(self.fuel_percentage) + "%")if self.fuel_percentage is not None else ft.Text("Sensore non trovato!", color='red'))
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
                        ft.DataCell(ft.Text("Temperatura acqua motore", weight=ft.FontWeight.W_400)),
                        ft.DataCell(ft.Text(str(self.water_temp) + "°C")if self.water_temp > 0 else ft.Text("Sensore non trovato!", color='red'))
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
