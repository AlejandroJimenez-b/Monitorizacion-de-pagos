from eventos import PlanificadorEventos
from banco import Prestamo, AnalizadorPagos
from notificaciones import Notificaciones
from logger import Logger
from datetime import date


class Main:

    logger = Logger().configurar_logging()

    def __init__(self):
        self.notificaciones = Notificaciones()

    def ejecutar(self, fecha_inicio, num_cuotas, importe_cuota, cuota_requerida, pagos_realizados, email_cliente):

        # Validaciones básicas de entrada
        if not isinstance(fecha_inicio, date):
            self.logger.error("fecha_inicio debe ser datetime.date")
            return

        if not isinstance(num_cuotas, int) or num_cuotas <= 0:
            self.logger.error("num_cuotas debe ser un entero > 0")
            return

        if not isinstance(pagos_realizados, list):
            self.logger.error("pagos_realizados debe ser una lista")
            return

        if not isinstance(email_cliente, str) or "@" not in email_cliente:
            self.logger.error("email_cliente inválido")
            return

        # 1. Crear préstamo
        prestamo = Prestamo(fecha_inicio, num_cuotas)
        cuotas_planificadas = prestamo.calcular_cuotas()

        if not cuotas_planificadas:
            self.logger.error("No se pudieron generar cuotas")
            return

        # 2. Analizar pagos
        analizador = AnalizadorPagos(
            cuotas_planificadas,
            pagos_realizados,
            importe_cuota,
            cuota_requerida
        )

        resultados = analizador.analizar()

        if not resultados:
            self.logger.error("No se generaron resultados de análisis")
            return

        # 3. Notificaciones
        for resultado in resultados:
            if resultado.get("estado") != "PAGADA":

                self.notificaciones.notificar_cuota_vencida(
                    email_cliente,
                    resultado.get("cuota"),
                    resultado.get("dias_de_retraso", 0),
                    resultado.get("recargo", 0)
                )


if __name__ == "__main__":

    main = Main()

    pagos_realizados = [
        {"fecha_pago": date(2026, 1, 15), "pagada": True},
        # {"fecha_pago": date(2026, 2, 2), "pagada": True},
    ]

    main.ejecutar(
        fecha_inicio=date(2026, 1, 1),
        num_cuotas=1,
        importe_cuota=500,
        cuota_requerida=500,
        pagos_realizados=pagos_realizados,
        email_cliente="alextresel22@gmail.com"
    )