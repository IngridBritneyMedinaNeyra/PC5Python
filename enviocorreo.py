import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(destinatario, asunto, mensaje):
    # Configuración del servidor SMTP
    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587  # Puerto TLS para Gmail

    # Credenciales del remitente
    remitente = 'tucorreo@gmail.com'
    password = 'tupassword'

    # Crear instancia del objeto MIMEMultipart
    mensaje_correo = MIMEMultipart()
    mensaje_correo['From'] = remitente
    mensaje_correo['To'] = destinatario
    mensaje_correo['Subject'] = asunto

    # Añadir el mensaje al cuerpo del correo
    mensaje_correo.attach(MIMEText(mensaje, 'plain'))

    # Crear conexión segura con el servidor SMTP
    with smtplib.SMTP(host=servidor_smtp, port=puerto_smtp) as servidor_smtp:
        servidor_smtp.starttls()
        servidor_smtp.login(remitente, password)
        # Enviar correo
        servidor_smtp.send_message(mensaje_correo)

    print("Correo enviado exitosamente a", destinatario)

# Ejemplo de uso
if __name__ == "__main__":
    destinatario = 'destinatario@gmail.com'
    asunto = 'Prueba de correo desde Python'
    mensaje = 'Este es un correo de prueba enviado desde Python.'
    enviar_correo(destinatario, asunto, mensaje)
