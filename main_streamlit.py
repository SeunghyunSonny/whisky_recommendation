import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

from whiskeyocr_forread import text_recognizer
from similarity import *

import numpy as np
import pandas as pd
import streamlit.components.v1 as html
import io, os, time, base64

from webcamera import WebcamCaptureHTML
from whiskeyocr_forread import TextRecognition
from image_search import ImageSearch
from whiskeylangchain import LangChainWhiskey
from embeddin import DocEmbedding



# 페이지 선택을 위한 버튼을 사이드바에 추가합니다.
with st.sidebar:
    choose = option_menu("Our Service", ["Contents", "Recommendation", "Docent", "Take a Photo"],
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
if choose == "Contents":
    # 제목
    st.title("나만의 위스키")

    # 진한 가로선 추가
    st.markdown('<hr style="border-top: 3px solid #000;">', unsafe_allow_html=True)

    # 이미지를 불러옵니다.
    image = Image.open("contents1.png")

    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image)

    # 두 번째 이미지를 불러옵니다.
    image2 = Image.open("contents2.png")

    # 두 번째 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image2)

    # 간격 조정
    st.subheader("")

    # 세 번째 이미지를 불러옵니다.
    image3 = Image.open("contents3.png")

    # 세 번째 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image3)

# "Whiskey Recommend" 페이지
if choose == "Recommendation":
  
    # 이미지를 불러옵니다.
    image4 = Image.open("recommend1.png")

    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image4)

     # 간격 조정
    st.subheader("")
    
    types = {'whiskey type을 선택해주세요': None,
            '싱글 몰트 위스키': '싱글몰트', 
            '블렌디드 위스키' : '블렌디드', 
            '블렌디드 몰트 위스키' : '블렌디드 몰트',
            '버번 & 라이 위스키' : '버번/라이'}
    
    selected_type = st.selectbox("**whiskey type 선택**", types.keys())
    
    # 간격 조정
    st.subheader("")  
    
    # 사용자로부터 최소가격과 최대가격을 입력 받음
    min_price = st.text_input("**최소 가격 입력 (최대 8자)**", max_chars=8)
    max_price = st.text_input("**최대 가격 입력 (최대 8자)**", max_chars=8)

    # 입력값이 비어있지 않은 경우에만 처리
    if min_price and max_price:
        min_price = int(min_price)
        max_price = int(max_price)
    # 입력된 최소가격과 최대가격으로 필요한 처리 수행
        st.write(f"가격 범위는 {int(min_price)}원부터 {int(max_price)}까지 입니다")


    # 간격 조정
    st.subheader("")

    # 이미지를 불러옵니다.
    image5 = Image.open("recommend2.png")

    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image5)

     # 간격 조정
    st.subheader("")
    
    # 'aroma를 선택' 제목 추가
    st.write("**aroma 선택**")

    # 체크 박스를 가로로 8개 나열
    col1_aroma, col2_aroma, col3_aroma, col4_aroma = st.columns(4)
    user_cats_list = []
    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_aroma:
        option1_aroma = st.checkbox('**나무향**', key="aroma_option1")
        if option1_aroma:
            user_cats_list.append('aroma_나무향')
        option2_aroma = st.checkbox('**잔류액향**', key="aroma_option2")
        if option2_aroma:
            user_cats_list.append('aroma_잔류액향')
            
    with col2_aroma:
        option3_aroma = st.checkbox('**와인향**', key="aroma_option3")
        if option3_aroma:
            user_cats_list.append('aroma_와인향')
        option4_aroma = st.checkbox('**피트향**', key="aroma_option4")
        if option4_aroma:
            user_cats_list.append('aroma_피트향')       

    with col3_aroma:
        option5_aroma = st.checkbox('**곡물향**', key="aroma_option5")
        if option5_aroma:
            user_cats_list.append('aroma_곡물향')  
        option6_aroma = st.checkbox('**꽃향기**', key="aroma_option6")
        if option6_aroma:
            user_cats_list.append('aroma_꽃향기')  

    with col4_aroma:
        option7_aroma = st.checkbox('**과일향**', key="aroma_option7")
        if option7_aroma:
            user_cats_list.append('aroma_과일향')  
        option8_aroma = st.checkbox('**유황**', key="aroma_option8")
        if option8_aroma:
            user_cats_list.append('aroma_유황')  

    # 'taste를 선택' 제목 추가
    st.write("**taste를 선택**")

    # 체크 박스를 가로로 8개 나열
    col1_taste, col2_taste, col3_taste, col4_taste = st.columns(4)

    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_taste:
        option1_taste = st.checkbox('**나무향**', key="taste_option1")
        if option1_taste:
            user_cats_list.append('taste_나무향')  
        option2_taste = st.checkbox('**잔류액향**', key="taste_option2")
        if option2_taste:
            user_cats_list.append('taste_잔류액향')  

    with col2_taste:
        option3_taste = st.checkbox('**와인향**', key="taste_option3")
        if option3_taste:
            user_cats_list.append('taste_와인향')  
        option4_taste = st.checkbox('**피트향**', key="taste_option4")
        if option4_taste:
            user_cats_list.append('taste_피트향')  

    with col3_taste:
        option5_taste = st.checkbox('**곡물향**', key="taste_option5")
        if option5_taste:
            user_cats_list.append('taste_곡물향')  
        option6_taste = st.checkbox('**꽃향기**', key="taste_option6")
        if option6_taste:
            user_cats_list.append('taste_꽃향기')  

    with col4_taste:
        option7_taste = st.checkbox('**과일향**', key="taste_option7")
        if option7_taste:
            user_cats_list.append('taste_과일향')  
        option8_taste = st.checkbox('**유황**', key="taste_option8")
        if option8_taste:
            user_cats_list.append('taste_유황')  

    # 'finish를 선택' 제목 추가
    st.write("**finish를 선택**")

    # 체크 박스를 가로로 8개 나열
    col1_finish, col2_finish, col3_finish, col4_finish = st.columns(4)

    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_finish:
        option1_finish = st.checkbox('**나무향**', key="finish_option1")
        if option1_finish:
            user_cats_list.append('finish_유황')  
        option2_finish = st.checkbox('**잔류액향**', key="finish_option2")
        if option2_finish:
            user_cats_list.append('finish_잔류액향')  

    with col2_finish:
        option3_finish = st.checkbox('**와인향**', key="finish_option3")
        if option3_finish:
            user_cats_list.append('finish_와인향')  
        option4_finish = st.checkbox('**피트향**', key="finish_option4")
        if option4_finish:
            user_cats_list.append('finish_피트향')  

    with col3_finish:
        option5_finish = st.checkbox('**곡물향**', key="finish_option5")
        if option5_finish:
            user_cats_list.append('finish_곡물향')  
        option6_finish = st.checkbox('**꽃향기**', key="finish_option6")
        if option6_finish:
            user_cats_list.append('finish_꽃향기')  

    with col4_finish:
        option7_finish = st.checkbox('**과일향**', key="finish_option7")
        if option7_finish:
            user_cats_list.append('finish_과일향')  
        option8_finish = st.checkbox('**유황**', key="finish_option8")
        if option8_finish:
            user_cats_list.append('finish_유황')  

    # 간격 조정
    st.subheader("")
    
    csv_file_path = r'./data/whisky_preprocessing.csv'

    # 유사도를 위한 데이터 전처리
    preprocessor = WhiskeySimilarityChecker(csv_file_path)
    preprocessor.preprocessing()

    user_name = 'User01' 
    show_list = ['Whisky Name','price','type','capacity','alcohol','country']
    
    if (types[selected_type] is not None) & (type(min_price) == int) & (type(max_price) == int) & (len(user_cats_list) > 0):
        Result = True
    else:
        Result = False

    st.write(types[selected_type])
    # "선택 완료" 버튼을 누르면 스피너가 나타나도록 설정
    if st.button("**선택 완료**"):
        with st.spinner("**위스키 추천 중입니다...**"):
            # 시뮬레이션을 위한 대기 시간, 실제로는 데이터 처리 시간에 맞게 조절
            time.sleep(3)  
            
        if Result == True:
            st.success('**위스키 찾기가 완료되었습니다**', icon="✅")     
            user_types = [types[selected_type]]
            user_price = (min_price, max_price) # (min_price , max_price)
            similar_shows = preprocessor.find_similar_shows(user_name, user_types, user_price, user_cats_list, top_n=5)
            st.write(similar_shows[show_list])
            
        elif Result == False:
            st.write('### :blue[값을 채워주세요!]')

if choose == "Docent":
    api_key_junseongs = "please put the api key"
    lcw = LangChainWhiskey(api_key_junseongs)
    
    st.title("위스키 도슨트 서비스")
    st.write("이 페이지는 위스키 도슨트 정보를 제공하는 페이지입니다.")

    # ImageSearch initialization
    driver_path = r"./chromedriver.exe"
    searcher = ImageSearch(driver_path)
    if choose == "Whiskey Docent":
        if not extracted_text:
            user_prompt = st.text_input("Enter the whiskey's full name:")
            if st.button("Generate") and user_prompt:
                searcher = ImageSearch(driver_path)
            saved_path = searcher.search_and_save_query(user_prompt)

            if saved_path:
                st.image(saved_path, caption=f"Image for {user_prompt}", use_column_width=True)
            else:
                st.write("Failed to fetch and save the image.")

            whiskey_info = lcw.get_whiskey_info(user_prompt)
            docent_description = lcw.get_docent_description(user_prompt)

            st.write(f"Whiskey Info: {whiskey_info}")
            st.write(f"Docent Description: {docent_description}")
        else:
            user_prompt = extracted_text


        # Here, use the `extracted_text` as input
        whiskey_info = lcw.get_whiskey_info(extracted_text)
        docent_description = lcw.get_docent_description(extracted_text)

        st.write(f"Whiskey Info: {whiskey_info}")
        st.write(f"Docent Description: {docent_description}")

        saved_path = searcher.search_and_save_query(extracted_text)

        if saved_path:
            st.image(saved_path, caption=f"Image for {extracted_text}", use_column_width=True)
        else:
            st.write("Failed to fetch and save the image.")

        whiskey_info = lcw.get_whiskey_info(extracted_text)
        docent_description = lcw.get_docent_description(extracted_text)

        st.write(f"Whiskey Info: {extracted_text}")
        st.write(f"Docent Description: {extracted_text}")
