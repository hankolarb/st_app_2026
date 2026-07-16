import json
import requests
import streamlit as st

# ----------------------------------------------------
# 【Python 3.14対応】st-annotated-textの自作代替関数
# ----------------------------------------------------
def annotated_text(*args):
    """
    外部ライブラリを使わずに、同じアノテーション表示をHTML/CSSで再現する関数。
    """
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        items = args[0]
    else:
        items = args

    html_elements = []
    
    # 品詞ごとに見やすいパステルカラーを定義
    color_map = {
        "名詞": "#DDF2FF",      # 薄い青
        "動詞": "#FCE4D6",      # 薄いオレンジ/ピーチ
        "形容詞": "#FFF2CC",    # 薄い黄
        "副詞": "#E1D5E7",      # 薄い紫
        "助詞": "#EDEDED",      # 薄いグレー
        "助動詞": "#F2F2F2",    # 極薄のグレー
    }

    for item in items:
        if isinstance(item, tuple):
            text = item[0]
            label = item[1] if len(item) > 1 else ""
            bg_color = item[2] if len(item) > 2 else color_map.get(label, "#E5E7EB")
            
            # ラベル（品詞名など）がある場合のHTML
            label_html = ""
            if label:
                label_html = f"""<span style="
                    font-size: 0.75em; 
                    opacity: 0.85; 
                    font-weight: bold; 
                    margin-left: 5px; 
                    border-left: 1px solid rgba(0,0,0,0.15); 
                    padding-left: 5px;
                    color: #374151;
                ">{label}</span>"""
            
            # 1単語ごとのバッジ
            html_elements.append(f"""
            <span style="
                background-color: {bg_color}; 
                color: #111827;
                padding: 2px 8px; 
                border-radius: 4px; 
                margin: 3px 2px; 
                display: inline-flex;
                align-items: center;
                font-size: 0.95em;
                font-family: inherit;
                border: 1px solid rgba(0,0,0,0.05);
            ">
                <strong>{text}</strong>{label_html}
            </span>
            """)
        else:
            # 一般テキストのHTMLエスケープ処理
            text = str(item).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            html_elements.append(f'<span style="font-size: 0.95em; margin: 3px 2px; display: inline-block; color: #1F2937;">{text}</span>')

    # 全体をきれいに包むコンテナ
    full_html = f"""
    <div style="line-height: 2.2; display: flex; flex-wrap: wrap; align-items: center; background-color: #f9fafb; padding: 15px; border-radius: 8px; border: 1px solid #e5e7eb;">
        {"".join(html_elements)}
    </div>
    """
    st.markdown(full_html, unsafe_allow_html=True)


# ----------------------------------------------------
# Yahoo API クラス部分
# ----------------------------------------------------
class YahooNlpApi:
    post_id = 0

    def __init__(self, client_id):
        self.__client_id = client_id

    @classmethod
    def get_id(cls):
        post_id = cls.post_id
        cls.post_id += 1
        return str(post_id)
  
    def get_headers(self):
        headers = {
            "Content-Type":"application/json",
            "User-Agent":f"Yahoo AppID: {self.__client_id}"
        }
        return headers

    def parameterize(self, post_id=None, jsonrpc="2.0", method="", params={}):
        if post_id is None:
            post_id = self.get_id()
        else:
            post_id = str(post_id)           
        req_obj = {
            "id":post_id,
            "jsonrpc":jsonrpc,
            "method":method,
            "params":params
        }
        return json.dumps(req_obj).encode("utf-8")
      
    def post(self, url, *args, **kwargs):
        headers = self.get_headers()
        payload = self.parameterize(*args, **kwargs)
        resp = requests.post(url, headers=headers, data=payload)
        return json.loads(resp.content)
  
    @staticmethod
    def tokenize(token):
        var_names = ["表記","読みがな","基本形表記","品詞","品詞細分類","活用型","活用系"]
        return dict(zip(var_names, token))
  
    def parse(self, q):
        url = "https://jlp.yahooapis.jp/MAService/V2/parse"
        method = "jlp.maservice.parse"
        params = {"q":q}
        data = self.post(url=url, method=method, params=params)
        tokens = data["result"]["tokens"]
        tokens = list(map(self.tokenize, tokens))
        return tokens

    def extract(self, q):
        url = "https://jlp.yahooapis.jp/KeyphraseService/V2/extract"
        method = "jlp.keyphraseservice.extract"
        params = {"q":q}
        data = self.post(url=url, method=method, params=params)
        tokens = data["result"]["phrases"]
        return tokens       
      
# APIの初期化
api = YahooNlpApi(st.secrets["yahoo_app_id"])

# ----------------------------------------------------
# UI / アプリロジック部分
# ----------------------------------------------------
if "result" not in st.session_state:
    st.session_state["result"] = None
if "keyword" not in st.session_state:
    st.session_state["keyword"] = None

def reset():
    st.session_state["result"] = None
    st.session_state["keyword"] = None

st.markdown("# 品詞解析")
st.markdown("## 入力")
document = st.text_area("分析したい文章を入力してください。")
mode = st.radio("分析モード", ["形態素解析", "キーワード抽出"], on_change=reset)

if st.button("分析"):
    if mode == "形態素解析":
        # 文章の構文解析
        st.session_state["result"] = api.parse(document)

    elif mode == "キーワード抽出":
        # キーワードの抽出
        st.session_state["result"] = api.extract(document)

if st.session_state["result"]:
    st.markdown("## 分析結果")
    if mode == "形態素解析":
        # ToDo : 選んだ品詞だけアノテーションする
        words = list(map(lambda wd:(wd["表記"], wd["品詞"]), st.session_state["result"]))
        annotated_text(words)
    elif mode == "キーワード抽出":
        # キーワードのリスト化
        keywords = list(map(lambda kw:kw["text"], st.session_state["result"]))
        kw = st.selectbox("キーワード", keywords)
        words = document.split(kw)
        for i in range(len(words)-1):
            words.insert(2*i+1, (kw,))
        annotated_text(words)