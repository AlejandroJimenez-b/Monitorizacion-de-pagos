# Flujo del funcionamiento de este archivo: tu script Python → servidor SMTP de Gmail → bandeja del destinatario
# Necesito:
# Credenciales:  tu email y la contraseña de aplicación que vas a generar
# El contenido — asunto, cuerpo del email, destinatario
# La lógica — cuándo disparar el email (cuota impagada, retraso, etc.)

# Librerias que necesito

import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText # Para construir el mensaje (el email)
from logger import Logger
from banco import AnalizadorPagos


load_dotenv()  # lee el archivo .env y carga las variables(con las credenciales)

class Notificaciones:

    logger = Logger().configurar_logging()


    def __init__(self):
        self.remitente = os.getenv("GMAIL_USER")
        self.password  = os.getenv("GMAIL_PASSWORD")
        self.servidor  = "smtp.gmail.com" # es la dirección del servidor de correo de Gmail
        self.puerto    = 587 #  es el puerto que usa Gmail para enviar emails con cifrado TLS (el estándar seguro)

    def enviar_email(self, destinatario: str, asunto: str, cuerpo: str):
        # Construccion del email
        mensaje = MIMEText(cuerpo, "plain")
        mensaje["Subject"] = asunto
        mensaje["From"]    = self.remitente
        mensaje["To"]      = destinatario

        try:
            with smtplib.SMTP(self.servidor, self.puerto) as conexion:
                conexion.starttls()
                conexion.login(self.remitente, self.password)
                conexion.sendmail(self.remitente, destinatario, mensaje.as_string())
                self.logger.info(f"Email enviado a {destinatario}")
        except smtplib.SMTPAuthenticationError:
            self.logger.error(f"Error: credenciales incorrectas. Revisa tu .env")
        except smtplib.SMTPException as e:
            self.logger.error(f"Error al enviar el email: {e}")

    def notificar_cuota_vencida(self, cuota):
        analizador_pagos = AnalizadorPagos().analizar()

        pass # implementar esta tarde
