import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from PIL import Image
import numpy as np
import pandas as pd
import io
import time
from image_search import ImageSearch
from works_and_streamlit import LangChainWhiskey
from whiskeyocr_forread import text_recognizer
import os
import base64

api_key_junseongs = "please put the api key"
lcw = LangChainWhiskey(api_key_junseongs)

# 페이지 선택을 위한 버튼을 사이드바에 추가합니다.
with st.sidebar:
    choose = option_menu("Our Service", ["Welcome", "Whiskey Recommend", "Whiskey Docent", "Take a Photo"],
                         icons=["emoji-kiss", "search-heart", "chat-left-text", "camera"],
                         menu_icon="menu-up", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#fafafa"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "color": "black", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#02ab21"},
                         })
# "Welcome" 페이지
if choose == "Welcome":
    # 크게하고 굵게 텍스트 표시 (가운데 정렬)
    st.markdown(
        f'<p style="text-align: center; font-size: 35px; font-weight: bold;">위스키 추천 프로그램</p>',
        unsafe_allow_html=True
    )
    # 이미지 로드 및 표시
    image_path = 'whiskey_on_the_rock.png'  # 이미지 파일의 경로를 지정해주세요
    img = Image.open(image_path)

    # 이미지를 중앙에 배치하고 Streamlit으로 출력
    # 이미지를 저장할 임시 버퍼를 만듭니다.io.BytesIO()는 이미지 데이터를 임시로 저장하기 위한 바이트 스트림을 생성
    buffered = io.BytesIO()
    # 이미지를 지정된 버퍼에 PNG형식으로 저장 이것은 PIL 라이브러리를 사용하여 이미지를 열고 저장하는 부분입니다
    img.save(buffered, format="PNG")
    # buffered:이미지가 저장된 버퍼, width=400:이미지의 가로 크기를 400픽셀로 설정
    # use_column_width=True: 이미지의 너비를 현재 열의 너비에 맞게 자동 저장
    # caption='이미지 캡션 : 이미지 하단에 표시되는 캡션(설명)을 설정
    st.image(buffered, width=400, use_column_width=True)

    st.markdown(
        f'<p style="text-align: center; font-size: 20px; font-weight: bold;">위스키 추천 프로그램 소개</p>',
        unsafe_allow_html=True
    )

    st.write("""
여러분을 위한 맞춤형 위스키를 추천해드립니다! 우리의 위스키 추천 프로그램은 개인의 취향을 고려하여, 다양한 종류와 테이스팅 노트를 가진 위스키 중에 딱 맞는 원하던 위스키를 찾아드립니다.

위스키는 주류 시장에서 대세로 성장하고 있습니다!

그래서 우리는 —기술을 활용하여, 사용자의 기호와 취향을 파악하여 최적의 향수를 추천해드립니다

우리의 위스키 추천 프로그램은 다음과 같은 특징을 가지고 있습니다.

:thumbsup: **맞춤형 추천**\n
사용자의 선호하는 맛/향/피니시를 기반으로, 다양한 위스키 중에서 가장 적합한 위스키를 찾아드립니다.

:thumbsup: **다양한 브랜드와 위스키**\n
다양한 브랜드와 수많은 향수 중에서 선택할 수 있습니다

:thumbsup: **정확한 추천**\n
유사도 분석을 통한, 사용자의 취향에 따른 정확한추천을 제공합니다

:thumbsup: **간편한 사용**\n
사용자 친화적인 인터페이스로 몇 가지 간단한 선택을 마치면 손쉽게 위스키를 추천 받을 수 있습니다

지금 바로 우리의 위스키 추천 프로그램을 통해 나의 취향의 맞는 위스키를 찾아보세요!!

내가 찾던 나만의 위스키를 통해 더욱 더 즐거운 목넘김을 시작해보세요!!
             """)

# "Whiskey Recommend" 페이지
if choose == "Whiskey Recommend":
    st.title("위스키 추천 서비스")
    st.subheader("원하는 위스키를 만나보세요")

    type = ['whiskey type을 선택해주세요', 'Single Malt whiskey', 'Blended whiskey', 'Blended Malt whiskey',
            'Bourbon & Rye whiskey']
    selected_type = st.selectbox("whiskey type 선택", type)

    if selected_type != type[0]:
        if selected_type == type[1]:
            st.write(
                "싱글 몰트 위스키는 하나의 곡물(보리)로 만들어진 것으로, 한 개의 증류기(distillery)에서 생산된 것을 의미합니다.\n이것은 특정 증류소의 고유한 스타일과 특징을 나타내며, 일반적으로 순수한 풍미와 독특한 향을 가지고 있습니다.")
        elif selected_type == type[2]:
            st.write("블렌디드 위스키는 여러 가지 원료를 혼합하여 만들어지는 것으로, 보통 싱글 몰트 위스키와 그레인 위스키를 섞어 만듭니다.")
        elif selected_type == type[3]:
            st.write("블렌디드 몰트 위스키는 싱글 몰트 위스키만을 혼합하여 만들어집니다. 다른 곡물(예: 보리)을 사용하지 않고 순수한 싱글 몰트 위스키를 섞어 만듭니다.")
        elif selected_type == type[4]:
            st.write(
                "버번 위스키는 옥수수로 만들어지며, 단맛과 부드러움이 특징입니다. 켄터키 버번은 가장 유명한 스타일 중 하나입니다.\n라이 위스키는 곡물 중 라이를 사용하여 만들어지며, 특유의 향과 맛이 있습니다. 미국 라이 위스키와 캐나다 라이 위스키가 있습니다.")

    aroma = ['Woody', 'Feinty', 'Winey', 'Peaty', 'Cereal', 'Floral', 'Fruity', 'Sulphur']
    selected_aroma = st.multiselect("aroma를 선택", aroma)

    taste = ['Woody', 'Feinty', 'Winey', 'Peaty', 'Cereal', 'Floral', 'Fruity', 'Sulphur']
    selected_taste = st.multiselect("tastef를 선택", taste)

    finish = ['Woody', 'Feinty', 'Winey', 'Peaty', 'Cereal', 'Floral', 'Fruity', 'Sulphur']
    selected_finish = st.multiselect("finish를 선택", finish)

    price = st.select_slider("whiskey price 선택(단위:원)", options=range(0, 30000001, 10000))

    if price > 0:
        st.write(f"0~{price}원까지 가격대 위스키를 찾으시나요?")
    else:
        st.write("원하는 가격대를 설정해주세요")

# "Whiskey Docent" 페이지
if choose == "Whiskey Docent":
    st.title("위스키 도슨트 서비스")
    st.write("이 페이지는 위스키 도슨트 정보를 제공하는 페이지입니다.")

# "Take a Photo" 페이지
if choose == "Take a Photo":
    st.title("Webcam Photo Capture in Streamlit")

    # User input for folder path
    folder_path = "./capturedimage"

    # HTML to create a video element and capture button
    html_code = """
        <div style="display: flex; justify-content: center;">
            <video id="webcam" width="640" height="480" autoplay></video>
            <button id="capture" style="margin-top: 10px;">Capture</button>
        </div>
        <canvas id="canvas" style="display:none;"></canvas>

        <script>
            const webcamElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('canvas');
            const captureButton = document.getElementById('capture');

            navigator.mediaDevices.getUserMedia({ 'video': true })
            .then(stream => {
                webcamElement.srcObject = stream;
            });

            captureButton.addEventListener('click', () => {
                canvasElement.width = webcamElement.videoWidth;
                canvasElement.height = webcamElement.videoHeight;
                const context = canvasElement.getContext('2d');
                context.drawImage(webcamElement, 0, 0);
                let photo = canvasElement.toDataURL('image/jpeg');
                document.getElementById('photo').value = photo;
            });
        </script>
    """

    # Embed the HTML in the Streamlit app
    st.markdown(html_code, unsafe_allow_html=True)

    # Capture the photo data
    photo_data = st.text_area(label="Captured Photo (base64)", height=200, key="photo")

    if photo_data and folder_path:
        header, encoded = photo_data.split(",", 1)
        photo_bytes = base64.b64decode(encoded)

        # Save the photo to the specified folder
        file_path = os.path.join(folder_path, "captured_photo.jpg")
        with open(file_path, "wb") as f:
            f.write(photo_bytes)

        st.success(f"Photo saved to: {file_path}")

    st.subheader("")
