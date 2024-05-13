from pytube import YouTube
import streamlit as st
from streamlit_option_menu import option_menu
import os
import PyPDF2


page_title = "Club de padel"
page_icon= "💻"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# st.image("assets/padel_principal.jpg", width=700)
st.title("Multi Funciones/programas")
st.text("Calle Garcia....")

selected = option_menu(menu_title=None, options=["Bajar videos", "Unir PDFs", "Detalles"], icons=["youtube", "file-pdf", "clipboard-data"], orientation="horizontal")


# if selected=="Detalles":
    
#     st.subheader("Ubicacion")
#     st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d6290.590308358365!2d-57.5599504!3d-37.9702407!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x9584dbd62ce65ceb%3A0x703f9cf5823d2926!2sOnce%20Unidos!5e0!3m2!1ses-419!2sar!4v1715439330925!5m2!1ses-419!2sar" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
   
    
#     st.subheader("Horarios")
#     dia, hora =st.columns(2)
    
    
#     dia.text("Lunes")
#     hora.text("10:00 - 19:00")
    
#     dia.text("Martes")
#     hora.text("10:00 - 19:00")
    
#     dia.text("Miercoles")
#     hora.text("10:00 - 19:00")
    
#     dia.text("Jueves")
#     hora.text("10:00 - 19:00")
    
#     dia.text("Viernes")
#     hora.text("10:00 - 19:00")
    
#     dia.text("Sabado")
#     hora.text("10:00 - 19:00")
    
#     dia.text("Domingo")
#     hora.text("10:00 - 14:00")
    
#     st.subheader("Contacto")
#     st.text("📞011-0025366565")
    
#     st.subheader("Instagram")
#     st.markdown("Siganos [Aqui]() en instagram")
    
   
# if selected=="Pistas":
#     st.write("#")
#     st.image("assets/pista1.jpg", caption="Esta es una de nuestras pistas", width=700)    
#     st.image("assets/pista2.jpg", caption="Esta es una de nuestras pistas", width=700)
#     st.image("assets/pista3.jpg", caption="Esta es una de nuestras pistas", width=700) 

if selected == "Bajar videos":
    st.subheader("Baje videos de YouTube")
     
    url = st.text_input("Ingrese la URL del video*")
    bajar = st.button("Donwload")
    
    # Backend
    if bajar:
        if url == "":
            
           st.warning("URL es obligatorio")         
        
        else:
           #descargar el video 
            carpeta_descargas = os.path.join(os.path.expanduser('~'), 'Downloads')
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            
            video.download(carpeta_descargas)
            st.success("Descarga exitosa!") 
            
           


##############################################################################################

if selected== "Unir PDFs":
   
   # Funciones
   def unir_pdfs(output_pdf, documents):
      pdf_final = PyPDF2.PdfMerger()
      
      for document in documents:
         pdf_final.append(document) 
      
      with open(output_pdf, 'wb') as file:  # Abre el archivo en modo de escritura de bytes
         pdf_final.write(file) 
   
   
   
   # Configuración de la interfaz de Streamlit
   st.subheader("Adjuntar PDFs para unir")
   pdf_adjuntos = st.file_uploader(label="", accept_multiple_files=True)
   unir = st.button(label="Unir PDFs")

   if unir:
      if len(pdf_adjuntos) <= 1:
         st.warning("Debe adjuntar más de un PDF")
      else:
         output_pdf = "pdf_final.pdf"  # Nombre del archivo de salida
         unir_pdfs(output_pdf, pdf_adjuntos)
         st.success("Desde aquí puedes descargar el archivo")
         
         with open(output_pdf, 'rb') as file:
               pdf_data = file.read()
         
         st.download_button(label="Descarga de PDF final", data=pdf_data, file_name="pdf_final.pdf")
               




# if selected=="Reserva":
#     st.subheader("Reservar")  
#     c1,c2 = st.columns(2)  
#     nombre =c1.text_input("Tu nombre*")
#     email = c2.text_input("Tu email*")
    
#     fecha = c1.date_input("Fecha")
#     hora = c2.selectbox("Hora", horas)
#     pista = c1.selectbox("Pista", pistas)
#     nota = c2.text_area("Nota")
    
#     enviar = st.button("Reservar")
    
#     # Backend
#     if enviar:
#         if nombre == "":
            
#             st.warning("El nombre es obligatorio")
            
#         elif email == "":
            
#             st.warning("El email es obligatorio")  
            
#         elif not valida_email(email):
#              st.warning("El email no es valido")
        
#         else:
            
#             #falta crear evento en google calendar
            
#             calendar = GoogleCalendarManager()
            
#             # Convertir la cadena a un objeto datetime
#             hora_dt = datetime.strptime(hora, "%H:%M")

#             # Sumar 1 hora
#             hora_nueva_dt = hora_dt + timedelta(hours=1)

#             # Convertir el resultado a una cadena en formato "HH:MM"
#             hora_nueva_str = hora_nueva_dt.strftime("%H:%M")
#             calendar.create_event(nombre, fecha, hora, hora_nueva_str, 'America/Argentina/Buenos_Aires', pista, email)
#             #---------------------------------------------------------------------
#             #crear registro en google sheet
#             #credenciales 
#             file_name_gs = "credencial_google_sheets.json"
#             google_sheet = "club padel"
#             sheet_name = "reserva" 
            
#             #funciones llamada del archivo google_sheet_action.py 
#             uid = generate_uid()
#             #Init
#             #conexion al archivo
#             google = GoogleSheet(file_name_gs, google_sheet, sheet_name)
#             created_at =  datetime.now()
#             # Valore ingresados en el formulario de reserva
#             value =[[nombre, email, str(fecha), hora, pista, nota, uid, str(created_at)]]
            
#             #obtenemos la ultiuma linea disponible en google sheet
#             range = google.get_last_row_range()
#             #escribimos en la hoja 
#             google.write_data(range, value)   
            
#             #---------------------------------------------------------------------------
            
#             #Enviar email al usuario
#             send(email, nombre, fecha, hora, pista)
#             st.success("Su pista a sido reservada de forma correcta") 
              
            

