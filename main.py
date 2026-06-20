from eventos import PlanificadorEventos
from banco import Prestamo, AnalizadorPagos
from notificaciones import Notificaciones
from logger import Logger
from datetime import date


class Main:

    logger = Logger().configurar_logging()

    def __init__(self):
        self.notificaciones = Notificaciones()

    def ejecutar(self, fecha_inicio, cuotas, pagos_realizados, email_cliente):

        # Validaciones básicas de entrada
        if not isinstance(fecha_inicio, date):
            self.logger.error("fecha_inicio debe ser datetime.date")
            return

        if not isinstance(cuotas, list) or len(cuotas) == 0:
            self.logger.error("cuotas debe ser una lista no vacía")
            return

        if not isinstance(pagos_realizados, list):
            self.logger.error("pagos_realizados debe ser una lista")
            return

        if not isinstance(email_cliente, str) or "@" not in email_cliente:
            self.logger.error("email_cliente inválido")
            return

        # 1. Crear préstamo
        prestamo = Prestamo(
            fecha_inicio,
            len(cuotas)
        )

        cuotas_planificadas = prestamo.calcular_cuotas()

        for plan, cuota in zip(cuotas_planificadas, cuotas):

            plan["nombre"] = cuota["nombre"]
            plan["importe_requerido"] = cuota["importe"]

        # 2. Analizar pagos
        analizador = AnalizadorPagos(
            cuotas_planificadas,
            pagos_realizados
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
                    resultado.get("nombre"),
                    resultado.get("dias_de_retraso", 0),
                    resultado.get("recargo", 0)
                )


if __name__ == "__main__":

    main = Main()


    # Cuotas a ejecutar
    cuotas = [
        {"nombre": "Agua", "importe": 30},
        {"nombre": "Luz", "importe": 40},
        {"nombre": "Netflix", "importe": 12},
        {"nombre": "Internet", "importe": 20},
        
    ]

    pagos_realizados = [
        {
            "fecha_pago": date(2026, 1, 15),
            "pagada": True,
            "importe_pagado": 30
        },
        {
            "fecha_pago": date(2026, 2, 2),
            "pagada": True,
            "importe_pagado": 40
        },
        {
            "fecha_pago": date(2026, 3, 15),
            "pagada": True,
            "importe_pagado": 10
        },
        {
            "fecha_pago": date(2026, 2, 2),
            "pagada": True,
            "importe_pagado": 20
        },
    ]

    main.ejecutar(
        fecha_inicio=date(2026, 1, 1),
        cuotas=cuotas,
        pagos_realizados=pagos_realizados,
        email_cliente="alextresel22@gmail.com"
    )
