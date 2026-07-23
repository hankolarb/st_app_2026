import json
import streamlit as st
from google.cloud import vision

credentials_dict = json.loads(st.secrets["google_credentials"], strict=False)
client = vision.ImageAnnotatorClient.from_service_account_info(info=credentials_dict)

@st.cache_data
def get_response(content):
   image = vision.Image(content=content)
   response = client.label_detection(image=image)


   return response



st.markdown("# 画像認識")

file = st.file_uploader("画像ファイルをアップロードしてください")

content = None
if file is not None:
   content = file.getvalue()
   st.image(content)

if st.button("解析をする"):
   if content is None:
       st.warning("画像ファイルをアップロードしてください。")
   else:
       response = get_response(content)

       if response.error.message:
           raise Exception(
               f"{response.error.message}\nFor more info on error messages, check: "
               "https://cloud.google.com/apis/design/errors"
           )

       labels = response.label_annotations
       st.write("Labels:")
       label_names = [f"• {label.description}" for label in labels]
       horizontal_labels = "  ".join(label_names)
       st.write(horizontal_labels)
