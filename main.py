from pytube import YouTube
import streamlit as st
from streamlit_option_menu import option_menu
import os
import PyPDF2
from PIL import Image
from rembg import remove
import io
from os import listdir
from os.path import isfile, join
import uuid



page_title = "Club de padel"
page_icon= "💻"
layout = "centered"

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

# st.image("assets/padel_principal.jpg", width=700)
st.title("Multi Funciones/programas")
st.text("Calle Garcia....")

selected = option_menu(menu_title=None, options=["Bajar videos", "Unir PDFs", "Remover fondo"], icons=["youtube", "file-pdf", "image"], orientation="horizontal")

 
######################################################################################
if selected == "Bajar videos":
   
   class Staging:

      def __init__(self,prefix):
         self.uniquename = uuid.uuid1()
         self.staging_path = '/data/{}/{}'.format(prefix.replace(' ','_') , self.uniquename  )

      def run(self):
         self.free()
         cmd = "mkdir -p {staging_path}".format(staging_path=self.staging_path)
         output = os.popen(cmd).read()
         return self.staging_path

      def free(self):
         cmd = "rm -Rf {staging_path} ".format(staging_path=self.staging_path)
         output = os.popen(cmd).read()
   
   class VideoDownloader:

      def __init__(self,youtube_url,start_second):
         self.youtube_url = youtube_url
         self.start_second = start_second

      def run(self,staging_path):
         
         d = YouTube(self.youtube_url).streams.get_highest_resolution()
         d.download(staging_path)

         onlyfiles = [f for f in listdir(staging_path) if isfile(join(staging_path, f))]
         filename = onlyfiles[0]
         filepath =  f"{staging_path}/{filename}"

         with open( filepath, "rb") as file:
               file_bytes = file.read()
               return file_bytes,filepath,filename
   
   def download_video(youtube_url,start_second):

      staging = Staging("tmp")
      staging_path = staging.run()

      file_bytes,filepath,filename = VideoDownloader(youtube_url,start_second).run(staging_path)
      st.session_state['video_downloaded'] = True
      st.session_state['video_filename'] = filename
      st.session_state['video_filepath'] = filepath
      st.session_state['video_bytes'] = file_bytes

      staging.free()
      
   st.title("Video Downloader")

   youtube_url = st.text_input("Youtube URL:",placeholder="Enter here...")
   st.button("Get Video", on_click=download_video,args=(youtube_url,0))

   if 'video_downloaded' in st.session_state:
      st.download_button(label="Video Download",data=st.session_state['video_bytes'],file_name=st.session_state['video_filename'],mime='application/octet-stream')


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
               
#########################################################################################################

if selected == "Remover fondo":
   #-----funciones------
   def process_image(image_uploaded):
      image = Image.open(image_uploaded)
      processed_imagen = remove_background(image)
      return processed_imagen
   
   def remove_background(image):
      image_byte = io.BytesIO()
      image.save(image_byte, format="PNG")
      image_byte.seek(0)
      processed_image_bytes = remove(image_byte.read())
      return Image.open(io.BytesIO(processed_image_bytes))
   
   st.subheader("Upload an Image")
   uploaded_image = st.file_uploader("Choose an image", type=["jpg","jpeg", "png"] )
   
   if uploaded_image is not None:
      
      st.image(uploaded_image, caption="Imagen subida", use_column_width=True)
      remove_button = st.button(label="Quitar fondo")
      
      if remove_button:
         processed_image = process_image(uploaded_image)
         st.image(processed_image, caption="Background Removed", use_column_width=True)
         
         processed_image.save("processed_image.png")
         with open("processed_image.png", "rb" ) as f:
            image_data = f.read()
         
         st.download_button("Donwload Processed Image", data=image_data, file_name="processed_image.png" )
         os.remove("processed_image.png")   
         
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
              
            

