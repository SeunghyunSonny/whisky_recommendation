import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import numpy as np
import pandas as pd

# 추천시스템 유사도
from Recommend.similarity import *

import streamlit.components.v1 as html
import io, os, time, base64, cv2

# 도슨트
from OCR.whiskylogoprocess import WhiskeyLogoProcessor
from OCR.image_search import ImageSearch
from llm.whiskeylangchain import LangChainWhiskey



# 페이지 선택을 위한 버튼을 사이드바에 추가합니다.
with st.sidebar:
    choose = option_menu("나만의 위스키", ["컨텐츠", "위스키 추천", "사진 찍기", "도슨트"],
                         icons=["emoji-kiss", "search-heart", "camera", "chat-left-text"],
                         menu_icon="menu-up", default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#FAFAFA"},
                             "icon": {"color": "black", "font-size": "25px"},
                             "nav-link": {"font-size": "16px", "color": "black", "text-align": "left", "margin": "0px",
                                          "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "#EDF6F9"},
                         })
# "Welcome" 페이지
if choose == "컨텐츠":

    # 제목
    image = Image.open("./image/main_img_1.jpg")
    st.image(image)
    
    
    # 이미지를 불러옵니다.
    image2 = Image.open("./image/main_img_2.jpg")

    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image2)

    # 두 번째 이미지를 불러옵니다.
    image3 = Image.open("./image/main_img_3.jpg")

    # 두 번째 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image3)

    # 간격 조정
    st.subheader("")

    # 세 번째 이미지를 불러옵니다.
    image4 = Image.open("./image/main_img_4.jpg")

    # 세 번째 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image4)

# "Whiskey Recommend" 페이지
if choose == "위스키 추천":
  
    # 이미지를 불러옵니다.
    image5 = Image.open("./image/main_img_5.jpg")

    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image5)

     # 간격 조정
    st.subheader("")
    
    types = {'위스키 타입을 선택해주세요': None,
            '싱글 몰트 위스키': '싱글몰트', 
            '블렌디드 위스키' : '블렌디드', 
            '블렌디드 몰트 위스키' : '블렌디드 몰트',
            '버번 & 라이 위스키' : '버번/라이'}
    
    selected_type = st.selectbox("**위스키 타입 선택**", types.keys())
    
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
        st.write(f"가격 범위는 {int(min_price)}원부터 {int(max_price)}원 까지 입니다")


    # 간격 조정
    st.subheader("")

    # 이미지를 불러옵니다.
    image6 = Image.open("./image/main_img_6.jpg")

    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image6)
    
    image7 = Image.open("./image/main_img_7.jpg")

    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image7)

     # 간격 조정
    st.subheader("")
    
    # 'aroma를 선택' 제목 추가
    st.write("**향 선택 (1 ~ 3 개)**")

    # 체크 박스를 가로로 8개 나열
    col1_aroma, col2_aroma, col3_aroma, col4_aroma = st.columns(4)
    user_cats_list = []
    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_aroma:
        option1_aroma = st.checkbox('**나무**', key="aroma_option1")
        if option1_aroma:
            user_cats_list.append('aroma_나무향')
        option2_aroma = st.checkbox('**잔류액**', key="aroma_option2")
        if option2_aroma:
            user_cats_list.append('aroma_잔류액향')
            
    with col2_aroma:
        option3_aroma = st.checkbox('**와인**', key="aroma_option3")
        if option3_aroma:
            user_cats_list.append('aroma_와인향')
        option4_aroma = st.checkbox('**피트**', key="aroma_option4")
        if option4_aroma:
            user_cats_list.append('aroma_피트향')       

    with col3_aroma:
        option5_aroma = st.checkbox('**곡물**', key="aroma_option5")
        if option5_aroma:
            user_cats_list.append('aroma_곡물향')  
        option6_aroma = st.checkbox('**꽃향기**', key="aroma_option6")
        if option6_aroma:
            user_cats_list.append('aroma_꽃향기')  

    with col4_aroma:
        option7_aroma = st.checkbox('**과일향**', key="aroma_option7")
        if option7_aroma:
            user_cats_list.append('aroma_과일')  
        option8_aroma = st.checkbox('**유황**', key="aroma_option8")
        if option8_aroma:
            user_cats_list.append('aroma_유황')  

    # 'taste를 선택' 제목 추가
    st.write("**맛 선택 (1 ~ 3 개)**")

    # 체크 박스를 가로로 8개 나열
    col1_taste, col2_taste, col3_taste, col4_taste = st.columns(4)

    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_taste:
        option1_taste = st.checkbox('**나무**', key="taste_option1")
        if option1_taste:
            user_cats_list.append('taste_나무향')  
        option2_taste = st.checkbox('**잔류액**', key="taste_option2")
        if option2_taste:
            user_cats_list.append('taste_잔류액향')  

    with col2_taste:
        option3_taste = st.checkbox('**와인**', key="taste_option3")
        if option3_taste:
            user_cats_list.append('taste_와인향')  
        option4_taste = st.checkbox('**피트**', key="taste_option4")
        if option4_taste:
            user_cats_list.append('taste_피트향')  

    with col3_taste:
        option5_taste = st.checkbox('**곡물**', key="taste_option5")
        if option5_taste:
            user_cats_list.append('taste_곡물향')  
        option6_taste = st.checkbox('**꽃향기**', key="taste_option6")
        if option6_taste:
            user_cats_list.append('taste_꽃향기')  

    with col4_taste:
        option7_taste = st.checkbox('**과일향**', key="taste_option7")
        if option7_taste:
            user_cats_list.append('taste_과일')  
        option8_taste = st.checkbox('**유황**', key="taste_option8")
        if option8_taste:
            user_cats_list.append('taste_유황')  

    # 'finish를 선택' 제목 추가
    st.write("**여운 선택 (1 ~ 3 개)**")

    # 체크 박스를 가로로 8개 나열
    col1_finish, col2_finish, col3_finish, col4_finish = st.columns(4)

    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_finish:
        option1_finish = st.checkbox('**나무**', key="finish_option1")
        if option1_finish:
            user_cats_list.append('finish_유황')  
        option2_finish = st.checkbox('**잔류액**', key="finish_option2")
        if option2_finish:
            user_cats_list.append('finish_잔류액향')  

    with col2_finish:
        option3_finish = st.checkbox('**와인**', key="finish_option3")
        if option3_finish:
            user_cats_list.append('finish_와인향')  
        option4_finish = st.checkbox('**피트**', key="finish_option4")
        if option4_finish:
            user_cats_list.append('finish_피트향')  

    with col3_finish:
        option5_finish = st.checkbox('**곡물**', key="finish_option5")
        if option5_finish:
            user_cats_list.append('finish_곡물향')  
        option6_finish = st.checkbox('**꽃향기**', key="finish_option6")
        if option6_finish:
            user_cats_list.append('finish_꽃향기')  

    with col4_finish:
        option7_finish = st.checkbox('**과일**', key="finish_option7")
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
    show_list = ['위스키 이름','가격','타입','용량','도수','국가']
    
    if (types[selected_type] is not None) & (type(min_price) == int) & (type(max_price) == int) & (len(user_cats_list) > 0):
        Result = True
    else:
        Result = False

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
            similar_shows.rename(columns = {'nameKor': '위스키 이름','type':'타입',
                                'price':'가격','capacity':'용량', 'country':'국가','alcohol':'도수'},inplace = True)
            
            st.write(similar_shows[show_list])
            
        elif Result == False:
            st.write('### :blue[값을 채워주세요!]')

if choose == "사진 찍기":
    # 이미지를 불러옵니다.
    image8 = Image.open("./image/서비스 준비 중.png")
    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image8)
    
    
    
    
if choose == "도슨트":
    api_key_junseongs = "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"
    lcw = LangChainWhiskey(api_key_junseongs)
    
    # 이미지를 불러옵니다.
    image9 = Image.open("./image/사진업로드 로고타입.jpg")
    # 이미지를 좌우로 정렬하여 페이지의 너비에 맞게 표시합니다.
    st.image(image9)
    # 간격 조정
    st.subheader("")
    logo_type = {"로고 타입을 선택해 주세요.":None,
            "한 줄짜리 로고사진": '하나',
            "두 줄짜리 로고사진": '둘'}
    
    selected_logo_type = st.selectbox("**로고 타입 선택**", logo_type.keys())
    # 간격 조정
    st.subheader("")
    # 파일 업로드를 위한 컴포넌트
    
    uploaded_file = st.file_uploader("로고 이미지 파일 업로드", type=["jpg", "png", "jpeg"])
    # 업로드한 파일이 있다면 이미지로 표시
    
    if uploaded_file is not None:
        pil_image = Image.open(uploaded_file)
        img = np.array(pil_image)
        
        st.image(uploaded_file, caption="업로드한 이미지", use_column_width=True)

    df_path = './data/whisky_preprocessing.csv'
    
    trocr_model_name = "microsoft/trocr-large-handwritten"
    threshold_similarity = 60

    processor = WhiskeyLogoProcessor(df_path, trocr_model_name, threshold_similarity)
    select_box = logo_type[selected_logo_type]  # 한줄 또는 두줄

    if select_box == '하나':
        str_text = processor.line_process(img)
    elif select_box == '둘':
        str_text = processor.lines_process(img)

    target_list = processor.result_list(str_text, length=5)
    extracted_text = st.selectbox('위스키를 선택해주세요: ', target_list)
        

    # ImageSearch 객체 초기화
    driver_path = r"./chromedriver.exe"
    searcher = ImageSearch(driver_path)

    user_prompt = extracted_text
    st.write(user_prompt)
    if st.button("Generate") and user_prompt:
        saved_path = searcher.search_and_save_query(user_prompt)

        if os.path.exists(saved_path):
            st.image(saved_path, caption=f"Image for {user_prompt}", width=200)
        else:
            st.write("Failed to fetch and save the image.")

        whiskey_info = lcw.get_info_and_description(whisky = user_prompt)

        # 도슨트 출력 참고: whiskey_info는 whiskey_info와 docent_description를 키값으로 갖는 딕셔너리 형식, 영어로 출력
        st.write(f"'{extracted_text}' 위스키에 대한 설명입니다. \n {whiskey_info}")
        # st.write(f"Docent Description: {docent_description}")


