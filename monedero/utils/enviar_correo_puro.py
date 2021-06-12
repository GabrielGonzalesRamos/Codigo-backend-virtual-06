from email import message
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
import smtplib
# MIME = Multi-Proporse Internet Mail Extensions
from email.mime.multipart import MIMEMultipart
from os import environ
from dotenv import load_dotenv
load_dotenv()

mensaje = MIMEMultipart()
password = environ.get("EMAIL_PASSWORD") # contraseña del correo
mensaje['From'] = environ.get("EMAIL") # correo del remitente
mensaje['Subject'] = "Solicitud de olvido de contraseña" # Titulo del correo

def enviarCorreo(destinatario, nombre, link):
    mensaje['To'] = destinatario
    # """ Para insertar texto con saltos del linea
    texto = """ Hola {} !
    Has solicitado recuperar tu contraseña. Para tal efecto te enviamos el siguiente link que 
    deberas ingresar para completar el cambio: 
    {}
    Si no fuiste tu, ignora este mensaje
    """.format(nombre, link)
    # Luego de definir el cuerpo del correo, lo agregamos al mensaje mediante su metodo attach y en formato mimetext en el cual recibira el texto y luego 
    # El formato a convertir, si queremos enviar un html entonces deberemos de poner en 'html',  caso contrario si enviamos un texto plano (puro texto) su formato 
    # Será pain
    mensaje.attach(MIMEText(texto, 'plain'))
    try:
        servidorSMTP = smtplib.SMTP('smtp.office365.com', 587) # Configuro mi servidor SMTP
        servidorSMTP.starttls() # indico que el protocolo será tls
        servidorSMTP.login(mensaje['From'], password)
        servidorSMTP.sendmail(
            from_addr=mensaje['From'],
            to_addrs=mensaje['To'],
            msg=mensaje.as_string()
        )
        servidorSMTP.quit()
        return True
    except Exception as e:
        print(e)
        return False    