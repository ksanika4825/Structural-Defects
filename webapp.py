import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt

import os


# Configure the model
key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key = 'AIzaSyDKO0Pm5NTjrNrKpgcLi4qbLScPiRj0Nbs')
model = genai.GenerativeModel('gemini-2.5-flash-lite')


# Upload and show image
st.sidebar.title('Upload your Image here')
uploaded_image = st.sidebar.file_uploader('Here', type=['jpeg','jpg','png'])
if uploaded_image:
  image = Image.open(uploaded_image)

  st.sidebar.subheader(':blue[UPLOADED IMAGE]')
  st.sidebar.image(image)

# Create main page
st.title(':yellow[Structural Defects] : :orange[AI Assisted structral defect identifier in construction business]')
tips = '''to use the applicaton follow the steps below:
         * Upload the Image.
         * Click on the button to generate summary
         * Click download to save the report generated'''

st.write(tips)

rep_title = st.text_input('Report Title:', None)
prep_by = st.text_input('Report Prepared by:', None)
prep_for = st.text_input('Report prepare for:',None)


prompt = f''' Assume you are a structural engineer. the user has provided an image of a structure.
you need to identify the structural defects in the image and generate a report
should contain the following.

It should start with the title, prepared by and prepared for details. provided by the user.
use {rep_title} as title, 
{prep_by} as prepared by, 
{prep_for} as prepared for the same.
 also mention current date from {dt.datetime.now().date()}
* Identify and classify the defect eg. crack, spalling, corrosion, honeycombing,
etc.
* there could more than one defect in the image. Identify all the defects seperately.
* for each defect identified, provide a short description of the defect and its potential impact on the structure.
* for each defect measure the severity of the defect as low, medium and high.
* also mention the time before this defect leads to permanent damage to the structure.
* provide short term and long term solution along with their estimated cost in rupees and time to implement.
* what precuationary measures can be taken to avoid such defects in future.
* the report generated should be in the word format.
* show the data in bullet points and tabular format whenever possible.
* make sure that the report does not exceed 3 pages.

'''
if st.button('Generate Report'):
  if uploaded_image is None:
    st.error('Please upload an image first.')
  else: 
    with st.spinner('Generating Report...'):
      response = model.generate_content([prompt,image], generation_config={'temperature':0.5})
      st.write(response.text) 

    st.download_button(
       label = 'Download Report',
       data = response.text,
       file_name = 'Structural_defect_report.txt',
       mime = 'text/plain')















