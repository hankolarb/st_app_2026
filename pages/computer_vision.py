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


if file is not None:
   
   content = file.getvalue()
   st.image(content)

if st.button("解析をする"):
   response = get_response(content)
   labels = response.label_annotations
   
   # 1. 最初にタイトルを表示（順番を修正）
   st.write("Labels:")
   
   if response.error.message:
       raise Exception(
           f"{response.error.message}\nFor more info on error messages, check: "
           "https://cloud.google.com/apis/design/errors"
       )

   # 2. columnsループを廃止し、カンマ（またはスペース）区切りで1行にまとめる
   label_names = [f"• {label.description}" for label in labels]
   horizontal_labels = "  ".join(label_names)  # スペース2つで横に並べる
   
   # 3. まとめた文字列を一度に出力
   st.write(horizontal_labels)
