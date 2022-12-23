import streamlit as st
from PIL import Image,ImageOps
import io
import os
import shutil

st.set_option('deprecation.showfileUploaderEncoding', False)

with open('favicon.png', 'rb') as f:
    favicon = io.BytesIO(f.read())

st.set_page_config(page_title='Resizing images',
                   page_icon=favicon, 
                   layout='wide', 
                   initial_sidebar_state='expanded')
                
st.title('Resizing')

st.header("Upload one or more images")
uploaded_images = st.file_uploader(label='',accept_multiple_files=True)

st.info("Please upload images and click on **Resize** button once all images are uploaded. **Resize** button will appear after the images have been uploaded.")

input_dir_name = 'tmp_img'
output_dir_name = 'resized'

if len(uploaded_images) > 0:

    resize_button = st.button('Resize')

    if resize_button:
        os.makedirs(input_dir_name,exist_ok=True)
        os.makedirs(output_dir_name,exist_ok=True)

        
        for uploaded_file in uploaded_images:
            
            # bytes_data = uploaded_file.read()
            with open(os.path.join(input_dir_name,uploaded_file.name),"wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.write("Resizing :", uploaded_file.name)     
            img = Image.open(os.path.join(input_dir_name,uploaded_file.name))       
            img.thumbnail((400,400), Image.ANTIALIAS)
            img = ImageOps.expand(img, border=((400-img.size[0])//2,(400-img.size[1])//2), fill=(255,255,255)) 
            img.save(f'./{output_dir_name}/{uploaded_file.name}')   

        shutil.make_archive(os.path.join('resized_image'), 'zip',f'./{output_dir_name}') 

        with open('resized_image.zip', 'rb') as f:
            st.download_button('Download Zip', f, file_name='resized_image.zip')
            shutil.rmtree(input_dir_name)
            shutil.rmtree(output_dir_name)

        
          
    

