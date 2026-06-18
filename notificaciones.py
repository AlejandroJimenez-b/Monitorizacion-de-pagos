import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from logger import Logger

load_dotenv()


class Notificaciones:

    logger = Logger().configurar_logging()

    def __init__(self):
        self.remitente = os.getenv("GMAIL_USER")
        self.password = os.getenv("GMAIL_PASSWORD")
        self.servidor = "smtp.gmail.com"
        self.puerto = 587

    def enviar_email(self, destinatario: str, asunto: str, cuerpo: str):

        if not self.remitente or not self.password:
            self.logger.error("Credenciales de email no configuradas")
            return

        if not isinstance(destinatario, str) or "@" not in destinatario:
            self.logger.error("Destinatario inválido")
            return

        try:
            mensaje = MIMEText(cuerpo, "plain")
            mensaje["Subject"] = asunto
            mensaje["From"] = self.remitente
            mensaje["To"] = destinatario

            with smtplib.SMTP(self.servidor, self.puerto) as conexion:
                conexion.starttls()
                conexion.login(self.remitente, self.password)
                conexion.sendmail(
                    self.remitente,
                    destinatario,
                    mensaje.as_string()
                )

                self.logger.info(f"Email enviado a {destinatario}")

        except smtplib.SMTPAuthenticationError:
            self.logger.error("Error: credenciales SMTP incorrectas")
        except smtplib.SMTPException as e:
            self.logger.error(f"Error SMTP: {e}")

    def notificar_cuota_vencida(self, destinatario: str, num_cuota: int, dias_retraso: int, recargo: float):

        if num_cuota is None:
            self.logger.error("num_cuota inválida en notificación")
            return

        asunto = f"Aviso: Cuota {num_cuota} vencida"

        cuerpo = (
            f"Estimado cliente,\n\n"
            f"La cuota {num_cuota} fue pagada con {dias_retraso} días de retraso.\n"
            f"Recargo aplicado: {recargo} €.\n\n"
            f"Atentamente,\nSu banco."
        )

        self.enviar_email(destinatario, asunto, cuerpo)