import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class WhiskeySimilarityChecker:
    def __init__(self, csv_file_path):
        self.df = pd.read_csv(csv_file_path, encoding = 'utf-8')
        self.cols = ['aroma', 'taste', 'finish']

    def preprocessing(self):
        # 전처리 프로세스
        for col in self.cols:
            self.str_to_list(col)
        self.change_element_name()
        self.concat_cols()

    def str_to_list(self, col):
        self.df[col] = self.df[col].apply(eval)
        self.df[col] = self.df[col].apply(sorted)

    def change_element_name(self):
        for col in self.cols:
            for idx in self.df.index:
                new_elements = [f'{col}_{e}' for e in self.df.at[idx, col]]
                self.df.at[idx, col] = new_elements

    def concat_cols(self):
        self.df['new_elements'] = ''
        for idx in self.df.index:
            extend_list = []
            for col in self.cols:
                e_list = self.df.at[idx, col]
                extend_list.extend(e_list)
            self.df.at[idx, 'new_elements'] = extend_list

    def find_similar_shows(self, user_name, user_types, user_price, user_cats_list, top_n=3):
        # 유저 데이터 생성
        col_list = ['nameEng', 'type', 'price', 'new_elements']
        user_record = [(user_name, user_types, user_price, user_cats_list)]
        user_df = pd.DataFrame(user_record, columns=col_list)

        # 위스키 타입과 가격조건이 맞는 데이터만 가져오고, 유저 데이터 추가
        min_price, max_price = user_price
        user_shows_df = self.df[(self.df['price'] >= min_price) & (self.df['price'] <= max_price) &
                                (self.df['type'].isin(user_types))]
        user_shows_df = user_shows_df.append(user_df).reset_index(drop=True)
        user_shows_df.rename(columns = {'nameEng':'Whisky Name'},inplace = True)

        # 자연어처리
        # CountVectorizer를 적용하기 위해 공백 문자로 word 단위가 구분되는 문자열로 변환
        user_shows_df['categories_literal'] = user_shows_df['new_elements'].apply(lambda x: (' ').join(x))

        # min_df 최소빈도수(예.m=2: 최소등장횟수 2번), ngram_range=(1,2): 단어 묶음, 단어의 묶음을 1개에서 2개까지 설정 
        count_vect = CountVectorizer( ngram_range=(1, 2)) #min_df=0,
        category_mat = count_vect.fit_transform(user_shows_df['categories_literal'])

        category_sim = cosine_similarity(category_mat, category_mat)
        category_sim_sorted_ind = category_sim.argsort()[:, ::-1]  # 유사한 순서대로 정렬

        # 기준이 되는 유저의 data와 index를 가져온다
        title_show = user_shows_df[user_shows_df['Whisky Name'] == user_name]
        title_index = title_show.index.values

        # (top_n)+1에 해당하는 장르 유사성이 높은 index 추출(유저 index를 삭제할 것이기 때문)
        similar_indexes = category_sim_sorted_ind[title_index, :(top_n) + 1]
        similar_indexes = similar_indexes.reshape(-1)

        # 유저 index는 제외
        similar_indexes = similar_indexes[similar_indexes != title_index]

        return user_shows_df.iloc[similar_indexes]

# # 사용 예시
# file_path = '../output/whisky_preprocessing_done.csv'
# preprocessor = WhiskeySimilarityChecker(file_path)
# preprocessor.preprocessing()

# # 고정
# user_name = 'User01' 
# # streamlit에서 해당 부분으로 대체해주세요
# user_types = ['블렌디드 위스키'] # selected_type 
# user_price = (40000, 99000) # (min_price , max_price)
# user_cats_list = ['aroma_와인향', 'aroma_과일향', 'taste_과일향', 'finish_과일향', 'finish_잔류액향']

# similar_shows = preprocessor.find_similar_shows(user_name, user_types, user_price, user_cats_list, top_n=5)
# print(similar_shows) # df이라 해당 부분
