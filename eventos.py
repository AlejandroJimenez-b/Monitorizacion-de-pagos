from datetime import date, timedelta

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