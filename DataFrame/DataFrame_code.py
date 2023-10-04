import os
import re
import sys
import pandas as pd

aromaSet = set()
tasteSet = set()
finishSet = set()

class Whisky:
    def __init__(self, id, nameEng, nameKor, price, aroma, taste, finish, type, capacity, alcohol, country, description):
        self.id = id
        self.nameEng = nameEng
        self.nameKor = nameKor
        self.price = price
        self.aroma = aroma
        self.taste = taste
        self.finish = finish
        self.type = type
        self.capacity = capacity
        self.alcohol = alcohol
        self.country = country
        self.description = description

    def __str__(self):
        return "nameEng: " + self.nameEng + "\n" + \
            "nameKor: " + self.nameKor + "\n" + \
            "price: " + self.price + "\n" + \
            "aroma: " + ", ".join(self.aroma) + "\n" + \
            "taste: " + ", ".join(self.taste) + "\n" + \
            "finish: " + ", ".join(self.finish) + "\n" + \
            "type: " + self.type + "\n" + \
            "capacity: " + self.capacity + "\n" + \
            "alcohol: " + self.alcohol + "\n" + \
            "description: " + self.description + "\n"
        

def preprocess(filename):            
    def is_match(text):
        pattern = r'\b\d{1,3}(?:,\d{3})+(?!(병|개))'
        return re.match(pattern, text)

    def handle_tasting_notes(lines):
        
        if(lines[0] == "Tasting Notes"):
            lines.pop(0)

        aroma_different_line = False
        aroma = []

        if(not str(lines[0]).startswith("Aroma")):
            lines.pop(0)
        else:
            if(lines[0] == "Aroma"):
                lines.pop(0)
            else:
                aroma = lines.pop(0).split(" ")
                aroma = [item.rstrip(",") for item in aroma]
                if(aroma_different_line is False):
                    aroma.pop(0)
                aromaSet.update(aroma)

        if(not str(lines[0]).startswith("Taste")):
            lines.pop(0)

        taste = lines.pop(0).split(" ")
        taste = [item.rstrip(",") for item in taste]
        taste.pop(0)
        tasteSet.update(taste)

        if(not str(lines[0]).startswith("Finish")):
            lines.pop(0)
        finish = lines.pop(0).split(" ")
        finish = [item.rstrip(",") for item in finish]
        finish.pop(0)
        finishSet.update(finish)

        return (aroma, taste, finish)

    data = []
    result = []


    print(f"opening {filename}...")
    with open(filename, "r", encoding='utf-8') as f:
        for line in f:
            data.append(line.strip())



    temp = []
    filter_flag = False
    filter_keywords = set(["지역", "케이스", "Information", ""])
    keywords = set(["국가", "종류", "도수", "용량"])

    index_arr = []

    print("Truncating useless data...")
    for i in range(0, len(data)):
        if(filter_flag):
            filter_flag = False
            continue

        line = data[i]
        if(line in filter_keywords):
            if(line == "Information" or line == ""):
                continue
            else:
                filter_flag = True
                continue
        elif(line in keywords):
            continue

        temp.append(line)
    
    data = temp


    print("Setting up data index...")
    for i in range(0, len(data)):
        line = data[i]
        if(is_match(line)):
            index_arr.append(i - 2)

    temp = []
    
    for i in range(0, len(index_arr) - 1):
        temp_arr = data[index_arr[i] : index_arr[i + 1]]
        temp.append(temp_arr)

    data = temp


    print("Creating object...")
    for i in range(0, len(data)):
        lines = data[i]
        print(lines)
        
        nameEng = lines.pop(0)
        nameKor = lines.pop(0)
        price = lines.pop(0)

        price = price.split(" ")[0]
        price = re.sub(r'\D', '', price)
        
        
        aroma, taste, finish = handle_tasting_notes(lines)

        type = lines.pop(0)

        cap_and_alc = lines[0:2]

        for item in cap_and_alc:
            if(re.search(r'\d+ml', item)):
                capacity = item
            elif(re.search(r'\d+%', item)):
                alcohol = item

        del lines[0:2]


        country = lines.pop(0)

        description = ""        
        if(len(lines) != 0 and lines[0] != ""):
            description = " ".join(lines)

        whisky = Whisky(i, nameEng, nameKor, price, aroma, taste, finish, type, capacity, alcohol, country, description)

        result.append(whisky)

    return result

def process_subset(data, columnSet):
    print(f"Processing {columnSet} subset...")
    df = pd.DataFrame(columns=["id", *list(columnSet)])

    for i in range(0, len(data)):
        new_row = {'id': i}
        for item in data[i]:
            new_row[item] = 1
        df.loc[i] = new_row

    df = df.fillna(0)
    df = df.astype(int)

    return df
    
def export_to_csv(df, name):
    df.to_csv(f"{name}.csv", index=False, encoding='utf-8-sig')
    print(f"{name} got created!")


def main(data):
    print("Converting to DataFrame...")
    df = pd.DataFrame([vars(s) for s in data])

    aroma_df = process_subset(df["aroma"], aromaSet)
    taste_df = process_subset(df["taste"], tasteSet)
    finish_df = process_subset(df["finish"], finishSet)

    name = re.search(r'(.+?)\.[^.]*$', filename).group(1)

    if not os.path.exists(f'outputs/{name}'):
        os.makedirs(name)
        
    print("Exporting...")
    export_to_csv(df, f"./outputs/{name}/{name}")

    export_to_csv(aroma_df, f"./outputs/{name}/aroma_data")
    export_to_csv(taste_df, f"./outputs/{name}/taste_data")
    export_to_csv(finish_df, f"./outputs/{name}/finish_data")

if(len(sys.argv) < 2):
    print("Please provide filename (e.g: \"python main.py ./whisky_data.txt\")")
    exit(0)
filename = sys.argv[1]
filename = os.path.basename(filename)

data = preprocess(filename)
main(data)

