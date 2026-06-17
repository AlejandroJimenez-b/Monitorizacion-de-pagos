from datetime import date, timedelta
from logger import Logger

# Clase calendario (para los festivos)
class CalendarioLaboral:
    
    FESTIVOS_2026 = {
        date(2026, 1, 1),
        date(2026, 1, 6),
        date(2026, 4, 2),
        date(2026, 4, 3),
        date(2026, 5, 1),
        date(2026, 8, 15),
        date(2026, 10, 12),
        date(2026, 11, 1),
        date(2026, 12, 6),
        date(2026, 12, 8),
        date(2026, 12, 25),
    }

    @staticmethod
    def es_dia_festivo(fecha: date) -> bool:
        if fecha.weekday() >= 5:
            return True
        return fecha in CalendarioLaboral.FESTIVOS_2026

    @staticmethod
    def es_dia_no_laborable(fecha: date) -> bool:
        return CalendarioLaboral.es_dia_festivo(fecha)

    @staticmethod
    def siguiente_dia_laborable(fecha: date) -> date:
        while CalendarioLaboral.es_dia_no_laborable(fecha):
            fecha += timedelta(days=1)
        return fecha
    

# Clase planificadora de eventos recurrentes
class PlanificadorEventos:

    logger = Logger().configurar_logging()

    def __init__(self, fecha_inicio: date, intervalo_dias: int, num_eventos: int):
        self.fecha_inicio = CalendarioLaboral.siguiente_dia_laborable(fecha_inicio)
        self.intervalo_dias = intervalo_dias
        self.num_eventos = num_eventos

    def calcular_siguiente_valida(self, fecha_anterior: date) -> date:
        fecha = fecha_anterior + timedelta(days=self.intervalo_dias)
        return CalendarioLaboral.siguiente_dia_laborable(fecha)

    def planificar(self):
        self.logger.info(f"--- Planificación de {self.num_eventos} eventos recurrentes (Intervalo: {self.intervalo_dias} días) ---")
        fecha_actual = self.fecha_inicio
        for evento in range(1, self.num_eventos + 1):
            self.logger.info(f"Evento {evento}: {fecha_actual}")
            if evento < self.num_eventos:
                fecha_actual = self.calcular_siguiente_valida(fecha_actual)