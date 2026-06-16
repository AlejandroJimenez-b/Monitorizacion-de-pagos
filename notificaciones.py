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

load_dotenv()  # lee el archivo .env y carga las variables(con las credenciales)

class Notificaciones:

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
                pass  # aquí irá el log de éxito
        except smtplib.SMTPAuthenticationError:
            pass  # aquí irá el log de error de credenciales
        except smtplib.SMTPException as e:
            pass  # aquí irá el log de error genera
