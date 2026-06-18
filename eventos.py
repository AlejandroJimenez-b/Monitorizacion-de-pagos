from datetime import date, timedelta
from logger import Logger


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

        if not isinstance(fecha, date):
            return False

        return fecha.weekday() >= 5 or fecha in CalendarioLaboral.FESTIVOS_2026

    @staticmethod
    def siguiente_dia_laborable(fecha: date) -> date:

        if not isinstance(fecha, date):
            return None

        while CalendarioLaboral.es_dia_festivo(fecha):
            fecha += timedelta(days=1)

        return fecha


class PlanificadorEventos:

    logger = Logger().configurar_logging()

    def __init__(self, fecha_inicio: date, intervalo_dias: int, num_eventos: int):

        if not isinstance(fecha_inicio, date):
            self.logger.error("fecha_inicio inválida")
            fecha_inicio = date.today()

        if not isinstance(intervalo_dias, int) or intervalo_dias <= 0:
            self.logger.error("intervalo_dias inválido")
            intervalo_dias = 1

        if not isinstance(num_eventos, int) or num_eventos <= 0:
            self.logger.error("num_eventos inválido")
            num_eventos = 1

        self.fecha_inicio = CalendarioLaboral.siguiente_dia_laborable(fecha_inicio)
        self.intervalo_dias = intervalo_dias
        self.num_eventos = num_eventos

    def calcular_siguiente_valida(self, fecha_anterior: date) -> date:
        return CalendarioLaboral.siguiente_dia_laborable(
            fecha_anterior + timedelta(days=self.intervalo_dias)
        )

    def planificar(self):

        self.logger.info(
            f"Planificando {self.num_eventos} eventos cada {self.intervalo_dias} días"
        )

        fecha_actual = self.fecha_inicio

        for evento in range(1, self.num_eventos + 1):

            self.logger.info(f"Evento {evento}: {fecha_actual}")

            if evento < self.num_eventos:
                fecha_actual = self.calcular_siguiente_valida(fecha_actual)