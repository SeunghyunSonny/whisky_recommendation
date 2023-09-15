import streamlit as st

from streamlit_option_menu import option_menu
from similarity import *
from PIL import Image

import streamlit.components.v1 as html
import numpy as np
import pandas as pd
import io, time

# 페이지 선택을 위한 버튼을 사이드바에 추가합니다.
with st.sidebar:
    choose = option_menu("Our Service", ["Welcome","Whiskey Recommend", "Whiskey Docent", "Take a Photo"],
                         icons=["emoji-kiss", "search-heart", "chat-left-text","camera-fill"],
                         menu_icon="menu-up" ,default_index=0,
                         styles={
                             "container": {"padding": "5!important", "background-color": "#000000"},
                             "icon": {"color": "white", "font-size": "25px"},
                             "nav-link": {"font-size": "16px","color":"white" ,"text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                             "nav-link-selected": {"background-color": "000000"},
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
    
    type = ['whiskey type을 선택해주세요','싱글 몰트 위스키', '블렌디드 위스키', '블렌디드 몰트 위스키', '버번 & 라이 위스키']
    selected_type = st.selectbox("whiskey type 선택", type)
    
    if selected_type != type[0]:
        if selected_type == type[1]:
            st.write("싱글 몰트 위스키는 하나의 곡물(보리)로 만들어진 것으로, 한 개의 증류기(distillery)에서 생산된 것을 의미합니다.\n이것은 특정 증류소의 고유한 스타일과 특징을 나타내며, 일반적으로 순수한 풍미와 독특한 향을 가지고 있습니다.")
            user_type = ['싱글몰트']
        elif selected_type == type[2]:
            st.write("블렌디드 위스키는 여러 가지 원료를 혼합하여 만들어지는 것으로, 보통 싱글 몰트 위스키와 그레인 위스키를 섞어 만듭니다.")
            user_type = ['블렌디드']
        elif selected_type == type[3]:
            st.write("블렌디드 몰트 위스키는 싱글 몰트 위스키만을 혼합하여 만들어집니다. 다른 곡물(예: 보리)을 사용하지 않고 순수한 싱글 몰트 위스키를 섞어 만듭니다.")
            user_type = ['블렌디드 몰트']
        elif selected_type == type[4]: 
            st.write("버번 위스키는 옥수수로 만들어지며, 단맛과 부드러움이 특징입니다. 켄터키 버번은 가장 유명한 스타일 중 하나입니다.\n라이 위스키는 곡물 중 라이를 사용하여 만들어지며, 특유의 향과 맛이 있습니다. 미국 라이 위스키와 캐나다 라이 위스키가 있습니다.")
            user_type = ['버번/라이']
    
    # 사용자로부터 최소가격과 최대가격을 입력 받음
    min_price = st.text_input("최소 가격 입력 (최대 8자)", max_chars=8)
    max_price = st.text_input("최대 가격 입력 (최대 8자)", max_chars=8)

    # 입력값이 비어있지 않은 경우에만 처리
    if min_price and max_price:
        min_price = int(min_price)
        max_price = int(max_price)
    # 입력된 최소가격과 최대가격으로 필요한 처리 수행
        st.write(f"가격 범위는 {int(min_price)}원부터 {int(max_price)}까지 입니다")

    # 'aroma를 선택' 제목 추가
    st.write("aroma를 선택:")

    # 체크 박스를 가로로 8개 나열
    col1_aroma, col2_aroma, col3_aroma, col4_aroma = st.columns(4)

    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_aroma:
        option1_aroma = st.checkbox('나무향', key="aroma_option1")
        option2_aroma = st.checkbox('잔류액향', key="aroma_option2")

    with col2_aroma:
        option3_aroma = st.checkbox('와인향', key="aroma_option3")
        option4_aroma = st.checkbox('피트향', key="aroma_option4")

    with col3_aroma:
        option5_aroma = st.checkbox('곡물향', key="aroma_option5")
        option6_aroma = st.checkbox('꽃향기', key="aroma_option6")

    with col4_aroma:
        option7_aroma = st.checkbox('과일향', key="aroma_option7")
        option8_aroma = st.checkbox('유황', key="aroma_option8")

    # 'taste를 선택' 제목 추가
    st.write("taste를 선택:")

    # 체크 박스를 가로로 8개 나열
    col1_taste, col2_taste, col3_taste, col4_taste = st.columns(4)

    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_taste:
        option1_taste = st.checkbox('나무향', key="taste_option1")
        option2_taste = st.checkbox('잔류액향', key="taste_option2")

    with col2_taste:
        option3_taste = st.checkbox('와인향', key="taste_option3")
        option4_taste = st.checkbox('피트향', key="taste_option4")

    with col3_taste:
        option5_taste = st.checkbox('곡물향', key="taste_option5")
        option6_taste = st.checkbox('꽃향기', key="taste_option6")

    with col4_taste:
        option7_taste = st.checkbox('과일향', key="taste_option7")
        option8_taste = st.checkbox('유황', key="taste_option8")

    # 'finish를 선택' 제목 추가
    st.write("finish를 선택:")

    # 체크 박스를 가로로 8개 나열
    col1_finish, col2_finish, col3_finish, col4_finish = st.columns(4)

    # 각 열(column)에 4개씩 체크 박스 추가
    with col1_finish:
        option1_finish = st.checkbox('나무향', key="finish_option1")
        option2_finish = st.checkbox('잔류액향', key="finish_option2")

    with col2_finish:
        option3_finish = st.checkbox('와인향', key="finish_option3")
        option4_finish = st.checkbox('피트향', key="finish_option4")

    with col3_finish:
        option5_finish = st.checkbox('곡물향', key="finish_option5")
        option6_finish = st.checkbox('꽃향기', key="finish_option6")

    with col4_finish:
        option7_finish = st.checkbox('과일향', key="finish_option7")
        option8_finish = st.checkbox('유황', key="finish_option8")


    file_path = r'C:\Users\Playdata\Documents\DataScience\source\13_3rd_TP_1\output\whisky_preprocessing.xlsx'

    # 유사도를 위한 데이터 전처리
    preprocessor = WhiskeySimilarityChecker(file_path)
    preprocessor.preprocessing()

    # 고정
    user_name = 'User01' 
    # streamlit에서 해당 부분으로 대체해주세요
    user_types = user_type 
    user_price = (min_price, max_price) # (min_price , max_price)
    user_cats_list = ['aroma_와인향', 'aroma_과일향', 'taste_과일향', 'finish_과일향', 'finish_잔류액향']
    show_list = ['nameEng','price','type','capacity','alcohol','country']
    similar_shows = preprocessor.find_similar_shows(user_name, user_types, user_price, user_cats_list, top_n=5)
    

    # "선택 완료" 버튼을 누르면 스피너가 나타나도록 설정
    if st.button("선택 완료"):
        with st.spinner("위스키 추천 중입니다..."):
    # 시뮬레이션을 위한 대기 시간, 실제로는 데이터 처리 시간에 맞게 조절
            time.sleep(3)  
        st.success('위스키 찾기가 완료되었습니다', icon="✅")
        st.write(similar_shows[show_list])

# "Whiskey Docent" 페이지
if choose == "Whiskey Docent":
    st.title("위스키 도슨트 서비스")
    st.write("이 페이지는 위스키 도슨트 정보를 제공하는 페이지입니다.")

# "Take a Photo" 페이지
if choose == "Take a Photo":
    st.title("")
    st.subheader("")