from datetime import date, timedelta
from eventos import CalendarioLaboral
from logger import Logger


class Prestamo:

    logger = Logger().configurar_logging()
    INTERVALO_DIAS = 30

    def __init__(self, fecha_inicio: date, num_cuotas: int):

        if not isinstance(fecha_inicio, date):
            self.logger.error("fecha_inicio inválida")
            fecha_inicio = date.today()

        if not isinstance(num_cuotas, int) or num_cuotas <= 0:
            self.logger.error("num_cuotas inválido")
            num_cuotas = 1

        self.fecha_inicio = CalendarioLaboral.siguiente_dia_laborable(fecha_inicio)
        self.num_cuotas = num_cuotas

    def calcular_siguiente_valida(self, fecha_anterior: date) -> date:
        return CalendarioLaboral.siguiente_dia_laborable(
            fecha_anterior + timedelta(days=self.INTERVALO_DIAS)
        )

    def calcular_cuotas(self):

        self.logger.info(
            f"Generando {self.num_cuotas} cuotas cada {self.INTERVALO_DIAS} días"
        )

        fecha_actual = self.fecha_inicio
        consecutivas_desplazadas = 0
        calculo_cuotas = []

        for cuota in range(1, self.num_cuotas + 1):

            if not isinstance(fecha_actual, date):
                self.logger.error("Fecha inválida en cálculo de cuotas")
                continue

            fecha_ideal = (
                fecha_actual + timedelta(days=self.INTERVALO_DIAS)
                if cuota > 1 else fecha_actual
            )

            dias_desplazados = (
                (fecha_actual - fecha_ideal).days if cuota > 1 else 0
            )

            if dias_desplazados > 0:
                consecutivas_desplazadas += 1
            else:
                consecutivas_desplazadas = 0

            self.logger.info(f"Cuota {cuota}: {fecha_actual}")
            
            if consecutivas_desplazadas >= 3:
                self.logger.warning(f"Atención: {consecutivas_desplazadas} cuotas consecutivas fueron desplazadas.")

            calculo_cuotas.append({
                "cuota": cuota,
                "fecha_prevista": fecha_actual
            })

            if cuota < self.num_cuotas:
                fecha_actual = self.calcular_siguiente_valida(fecha_actual)

        return calculo_cuotas


class AnalizadorPagos:

    logger = Logger().configurar_logging()

    TARIFAS = {
        "interes_normal": 0.07,
        "interes_demora": 0.09,
        "interes_legal": 0.040625
    }

    def __init__(self, cuotas_planificadas: list, pagos_realizados: list):

        self.cuotas_planificadas = cuotas_planificadas or []
        self.pagos_realizados = pagos_realizados or []

    def analizar(self):

        resultados_de_cuota = []

        if not isinstance(self.cuotas_planificadas, list):
            self.logger.error("cuotas_planificadas inválidas")
            return []

        if not isinstance(self.pagos_realizados, list):
            self.logger.error("pagos_realizados inválidos")
            return []

        for i in range(len(self.cuotas_planificadas)):

            plan = self.cuotas_planificadas[i]

            pago = (
                self.pagos_realizados[i]
                if i < len(self.pagos_realizados)
                else None
            )

            resultado = {
                "cuota": plan.get("cuota"),
                "nombre": plan.get("nombre")
            }

            if not isinstance(pago, dict):
                self.logger.warning(
                    f"Cuota {plan.get('nombre', plan['cuota'])}: IMPAGADA"
                )

                resultado["estado"] = "IMPAGADA"

                resultados_de_cuota.append(resultado)
                continue

            importe_pagado = pago.get("importe_pagado", 0)

            if not pago.get("pagada") or importe_pagado == 0:

                self.logger.warning(
                    f"Cuota {plan.get('nombre', plan['cuota'])}: IMPAGADA"
                )

                resultado["estado"] = "IMPAGADA"

            else:

                fecha_pago = pago.get("fecha_pago")

                if not isinstance(fecha_pago, date):
                    self.logger.warning("fecha_pago inválida")
                    continue

                dias_retraso = max(
                    0,
                    (fecha_pago - plan["fecha_prevista"]).days
                )

                importe_requerido = plan.get("importe_requerido", 0)
                faltante = max(0, importe_requerido - importe_pagado)
                esta_incompleta = faltante > 0

                if dias_retraso == 0 and not esta_incompleta:

                    self.logger.info(
                        f"Cuota {plan.get('nombre', plan['cuota'])}: pagada a tiempo"
                    )

                    resultado["estado"] = "PAGADA"
                    resultado["dias_de_retraso"] = 0

                else:

                    if dias_retraso > 0 and esta_incompleta:
                        resultado["estado"] = "PAGADA CON RETRASO INCOMPLETA"
                    elif dias_retraso > 0:
                        resultado["estado"] = "PAGADA CON RETRASO"
                    else:
                        resultado["estado"] = "PAGADA INCOMPLETA"
                    resultado["dias_de_retraso"] = dias_retraso

                    if esta_incompleta:
                        self.logger.warning(
                            f"Cuota {plan.get('nombre', plan['cuota'])}: "
                            f"INCOMPLETA. {faltante} € POR ABONAR"
                        )

                        resultado["incompleta"] = True
                        resultado["faltante"] = faltante

                    if dias_retraso > 0:
                        interes = round(
                            dias_retraso
                            * importe_pagado
                            * (self.TARIFAS["interes_demora"] / 365),
                            2
                        )

                        self.logger.warning(
                            f"Cuota {plan.get('nombre', plan['cuota'])}: "
                            f"pagada con {dias_retraso} días de retraso. "
                            f"Recargo: {interes} €"
                        )

                        resultado["recargo"] = interes

            resultados_de_cuota.append(resultado)

        return resultados_de_cuota
