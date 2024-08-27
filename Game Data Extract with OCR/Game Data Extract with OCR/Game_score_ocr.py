import pytesseract
import csv
import cv2
import imutils
from time import sleep
import os
import pandas as pd
from PIL import Image
import numpy as np

def get_file_names(folder_path):
    file_names = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_names.append(file)
    return file_names

def ocr_image(img_name):
    pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    image = cv2.imread(img_name)
    image = cv2.resize(image, (0,0), fx=2.1, fy=2.1, interpolation=cv2.INTER_CUBIC)
    norm_img = np.zeros((image.shape[0], image.shape[1]))
    image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)
    image = cv2.bilateralFilter(image,9,75,75)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    data = pytesseract.image_to_string(thresh, lang='eng',config='--psm 6 --oem 1')
    # import re
    # print(type(data))
    data = data.replace('Adv,', 'Adv.')
    data = data.replace(' 11,5 ', ' 11.5 ')
    data = data.replace('0:09:24 11.5 1 5', '0:09:24 11.5 11 5')
    data = data.replace('—_ AIRPLANE Adv.', 'AIRPLANE Adv.')
    with open("data.txt", "w", encoding='utf-8') as file:
        file.write(data)
    sleep(0.1)
    with open("data.txt", "r", encoding='utf-8') as file:
        data = file.readlines()
    for line in data:
        if line[:4]=="LOSE" or line[:3]=="WIN":      #get the all data
            with open("all_data.txt", "a", encoding='utf-8') as file:
                file.write(line)
    sleep(0.1)

def lose_data():
    with open("all_data.txt","r") as file:
        lines = file.readlines()
    for line in lines:
        if line[:4]=="LOSE":      #get the lose data
            with open("lose.txt", "a") as file: 
                file.write(line)
    sleep(0.1)
    with open("lose.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        game_name =[]
        line = line[4:]
        for i in range(1, len(line)):
            if line[i].isalpha() or line[i] == " " or line[i] ==".":
                game_name.append(line[i])
            if line[i].isdigit():
                break
        game_name = ''.join(game_name)
        game_name_len = len(game_name)
        line = line[9+game_name_len:]
        line = line.split(" ")
        with open('table.csv', 'a', newline='') as file:
            writer_append = csv.writer(file)
            writer_append.writerow(["LOSE", game_name, line[0], line[1], line[2], line[3]])
def win_data():
    with open("all_data.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        if line[:3]=='WIN':     #get the win data
            with open("win.txt", "a") as file:
                file.write(line)
    sleep(0.1)
    with open("win.txt", "r") as file:
        lines = file.readlines()
    # print(lines)
    for line in lines:
        game_name =[]
        line = line[3:]
        for i in range(1, len(line)):
            if line[i].isalpha() or line[i] == " " or line[i] ==".":
                game_name.append(line[i])
            if line[i].isdigit():
                break
        game_name = ''.join(game_name)
        game_name_len = len(game_name)
        line = line[9+game_name_len:]
        line = line.split(" ")
        with open('table.csv', 'a', newline = '') as file:
            writer_append = csv.writer(file)
            writer_append.writerow(["WIN", game_name, line[0], line[1], line[2], line[3]])
def delete_data(): #delete the duplicate the data
    df = pd.read_csv('table.csv')
    df.drop_duplicates(inplace=True)
    df.to_csv('output.csv', index=False)
    df = pd.read_csv('fight.csv')
    df.drop_duplicates(inplace=True)
    df.to_csv('close_match.csv', index=False)

def jpg2png(file_name):  #save the png file
    img = Image.open("image/"+file_name) 
    img.save(os.path.join("image_png", file_name+".png"), dpi=(300,300))
def fight():
    with open("win.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        game_name =[]
        line = line[3:]
        for i in range(1, len(line)):
            if line[i].isalpha() or line[i] == " " or line[i] ==".":
                game_name.append(line[i])
            if line[i].isdigit():
                break
        game_name = ''.join(game_name)
        game_name_len = len(game_name)
        line = line[9+game_name_len:]
        line = line.split(" ")
        with open('fight.csv', 'a', newline = '') as file:
            if int(line[2])+int(line[3])>=12:
                writer_append = csv.writer(file)
                writer_append.writerow(["WIN", game_name, line[0], line[1], line[2], line[3]])
    sleep(0.1)
    with open("lose.txt", "r") as file:
        lines = file.readlines()
    for line in lines:
        game_name =[]
        line = line[4:]
        for i in range(1, len(line)):
            if line[i].isalpha() or line[i] == " " or line[i] ==".":
                game_name.append(line[i])
            if line[i].isdigit():
                break
        game_name = ''.join(game_name)
        game_name_len = len(game_name)
        line = line[9+game_name_len:]
        line = line.split(" ")
        with open('fight.csv', 'a', newline='') as file:
            if int(line[2])+int(line[3])>=12:
                writer_append = csv.writer(file)
                writer_append.writerow(["LOSE", game_name, line[0], line[1], line[2], line[3]])
                
def reswap():
    with open('all_data.txt', 'r') as file:
        lines = file.readlines()

    # Iterate over each line
    for i, line in enumerate(lines):
        # Check if the line has at least 25 characters
        if len(line) >= 25:
            # Convert 'a' to 'e' starting from the 25th character
           modified_line = line[:24] + line[24:].replace('Oo', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('T', '7')
           modified_line = modified_line[:24] + modified_line[24:].replace(')', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('(', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('oO', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('O', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('fe0', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('o', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('ri', '7')
           modified_line = modified_line[:24] + modified_line[24:].replace('3,0', '3.0')
           modified_line = modified_line[:24] + modified_line[24:].replace('i0', '0')
           modified_line = modified_line[:24] + modified_line[24:].replace('b', '9')
           modified_line = modified_line[:24] + modified_line[24:].replace('kk', '3')
           modified_line = modified_line[:24] + modified_line[24:].replace('9s ]', '9')
           modified_line = modified_line[:24] + modified_line[24:].replace('il', '11')
           modified_line = modified_line[:24] + modified_line[24:].replace('v4', '11')
           modified_line = modified_line[:24] + modified_line[24:].replace('| ', '')
           modified_line = modified_line[:24] + modified_line[24:].replace('0 k', '10')
           modified_line = modified_line[:14] + modified_line[14:].replace(',', '.')
           modified_line = modified_line[:14] + modified_line[14:].replace('fr0', '0')
           lines[i] = modified_line
    # Write the modified content back to the file
    with open('all_data.txt', 'w') as file:
        file.writelines(lines)
# print(lines)
def result_data():
    with open('output.csv','r', encoding='utf_8_sig') as f:
        # Creat a CSV reader object
        reader = csv.reader(f)

        # Read the data from the CSV file
        # data = list(reader)
        data = []
        sub_data = []
        for row in reader:
            result_column = row[0]
            map_column = row[1]
            score_column = row[2]
            death_column = row[3]
            win_round_column = row[4]
            fail_round_column = row[5]
            sub_data.append(result_column)
            sub_data.append(map_column)
            sub_data.append(score_column)
            sub_data.append(death_column)
            sub_data.append(win_round_column)
            sub_data.append(fail_round_column)
            data.append(sub_data)
            sub_data = []
        #Print or process the columns as needed
        # print(close_data)

        new_data = []
        mid_data = []
        win_number = 0
        fail_number = 0
        for i in data[1:]:
            if i[0] == "WIN":
                win_number += 1
            elif i[0] == "LOSE":
                fail_number += 1
            mid_data.append(i[1])
            mid_data.append(win_number)
            mid_data.append(fail_number)
            if i[2]=="3,0":
                i[2] = 3
            elif i[2] == "11,5":
                i[2] = "11.5"
            elif i[2]=="15,5":
                i[2] = 15.5
            # else i[2] = i[2]
            # print(i[2])
            mid_data.append(float(i[2]))
            if i[3]=="T":
                i[3] = 7
            mid_data.append(float(i[3]))
            mid_data.append(i[4])
            mid_data.append(i[5])
            new_data.append(mid_data)
            mid_data = []
            win_number = 0
            fail_number = 0
        # print(new_data)

        map = []
        close_round = 0
        final_data = []
        new_final_data = []
        for i in new_data:
            if map.__contains__(i[0]):
                index = map.index(i[0])
                # print("i", i[0])  
                sum_victory = new_final_data[index][1] + i[1]
                sum_fail = new_final_data[index][11] + i[2]
                new_final_data[index][1] = sum_victory
                new_final_data[index][2] = round(sum_victory*100/(sum_victory + sum_fail), 2)
                # print(sum_victory, sum_fail)
                sum_death = new_final_data[index][8] + i[4]
                sum_score = new_final_data[index][3] * new_final_data[index][8] + i[3]
                if sum_death == 0:
                    new_final_data[index][3] = 0
                else:
                    new_final_data[index][3] = round(sum_score/sum_death, 2)
                sum_win_round = new_final_data[index][9] + int(i[5])
                sum_fail_round = new_final_data[index][10] + int(i[6])
                new_final_data[index][4] = round(sum_death*100/(sum_win_round + sum_fail_round), 2)
                if sum_win_round == 0:
                    new_final_data[index][5] = 0
                else:
                    new_final_data[index][5] = round((sum_death-sum_fail_round)*100/sum_win_round, 2)
                sum_close_round = new_final_data[index][12] + 1
                new_final_data[index][6] = round(sum_close_round*100/(sum_victory + sum_fail), 2)
                new_final_data[index][7] = sum_score 
                new_final_data[index][8] = sum_death 
                new_final_data[index][9] = sum_win_round 
                new_final_data[index][10] = sum_fail_round 
                new_final_data[index][11] = sum_fail
                new_final_data[index][12] = sum_close_round
                sum_victory = 0
                sum_fail = 0
                sum_death = 0
                sum_score = 0
                sum_close_round = 0
                sum_win_round = 0
                sum_fail_round = 0
                # print(new_final_data)
            else:
                map.append(i[0])
                final_data.append(i[0])  #map_name
                final_data.append(i[1])  #win_num
                try:
                    final_data.append(round(i[1]*100/(i[1]+i[2]), 2))     #rate
                except:
                    final_data.append(0)
                if i[4] == 0:                                       #S/D
                    final_data.append(0)
                else:  
                    final_data.append(round(i[3]/i[4], 2))
                final_data.append(round(i[4]*100/(int(i[5])+int(i[6])), 2))             #D/T
                if int(i[5]) == 0:                                     #WD/WR
                    final_data.append(0)
                else:
                    final_data.append(round((i[4]-int(i[6]))*100/int(i[5]), 2))
                close_round +=1
                try:
                    final_data.append(round(close_round*100/(i[1]+i[2]), 2))      #close_rate
                except:
                    final_data.append(0)
                final_data.append(i[3])                    #score
                final_data.append(i[4])                    #death
                final_data.append(int(i[5]))                    #win_round
                final_data.append(int(i[6]))                    #fail_round
                final_data.append(i[2])                     #fail_num
                final_data.append(close_round)                     #close_round
                new_final_data.append(final_data)
                final_data = []
                close_round = 0
                # print(new_final_data)
                
            # print("map", map) 
        def transfer_array(array):
            return [subarray[:-7] for subarray in array]
        result = transfer_array(new_final_data)
        # print(result)         
        a_result = [[x if not isinstance(x, (int, float)) else '{:.2f}'.format(x) for x in sublist] for sublist in result]

        #Create a CSV file
        key_data = [['Map', 'Win_num', 'Rate', 'S/D', 'D/TR', 'WD/WR']]
        with open('result.csv', 'w', newline='', encoding='utf-8') as f:
            #Create a CSV writer object
            writer = csv.writer(f)

            #Write the data to the CSV file
            writer.writerows(key_data)            
            writer.writerows(a_result)
    with open('close_match.csv','r', encoding='utf_8_sig') as f:
        # Creat a CSV reader object
        close_reader = csv.reader(f)

        # Read the data from the CSV file
        # data = list(reader)
        close_data = []
        close_sub_data = []
        for row in close_reader:
            result_column = row[0]
            map_column = row[1]
            score_column = row[2]
            death_column = row[3]
            win_round_column = row[4]
            fail_round_column = row[5]
            close_sub_data.append(result_column)
            close_sub_data.append(map_column)
            close_sub_data.append(score_column)
            close_sub_data.append(death_column)
            close_sub_data.append(win_round_column)
            close_sub_data.append(fail_round_column)
            close_data.append(close_sub_data)
            close_sub_data = []
        #Print or process the columns as needed
        # print(close_data)

        close_new_data = []
        close_mid_data = []
        win_number = 0
        fail_number = 0
        for i in close_data[1:]:
            if i[0] == "WIN":
                win_number += 1
            elif i[0] == "LOSE":
                fail_number += 1
            close_mid_data.append(i[1])
            close_mid_data.append(win_number)
            close_mid_data.append(fail_number)
            if i[2]=="11,5":
                i[2] = 11.5
            elif i[2]=="15,5":
                i[2] = 15.5
            close_mid_data.append(float(i[2]))
            if i[3] == "T":
                i[3] = 7
            close_mid_data.append(float(i[3]))
            close_mid_data.append(i[4])
            close_mid_data.append(i[5])
            close_new_data.append(close_mid_data)
            close_mid_data = []
            win_number = 0
            fail_number = 0
        # print(close_new_data)

        close_map = []
        close_round = 0
        close_final_data = []
        close_new_final_data = []
        for i in close_new_data:
            if close_map.__contains__(i[0]):
                index = close_map.index(i[0])
                # print("i", i[0])  
                sum_victory = close_new_final_data[index][1] + i[1]
                sum_fail = close_new_final_data[index][11] + i[2]
                close_new_final_data[index][1] = sum_victory
                close_new_final_data[index][2] = round(sum_victory*100/(sum_victory + sum_fail), 2)
                sum_death = close_new_final_data[index][8] + i[4]
                sum_score = close_new_final_data[index][3] * close_new_final_data[index][8] + i[3]
                if sum_death == 0:
                    close_new_final_data[index][3] = 0
                else:
                    close_new_final_data[index][3] = round(sum_score/sum_death, 2)
                sum_win_round = close_new_final_data[index][9] + int(i[5])
                sum_fail_round = close_new_final_data[index][10] + int(i[6])
                close_new_final_data[index][4] = round(sum_death*100/(sum_win_round + sum_fail_round),2)
                if sum_win_round == 0:
                    close_new_final_data[index][5] = 0
                else:
                    close_new_final_data[index][5] = round((sum_death-sum_fail_round)*100/sum_win_round,2)
                for k in new_final_data:
                    if k[0] == i[0]:
                        total_round = k[1] + k[11]
                sum_close_round = close_new_final_data[index][12] + 1
                close_new_final_data[index][6] = round(sum_close_round*100/total_round,2)
                close_new_final_data[index][7] = sum_score 
                close_new_final_data[index][8] = sum_death 
                close_new_final_data[index][9] = sum_win_round 
                close_new_final_data[index][10] = sum_fail_round 
                close_new_final_data[index][11] = sum_fail 
                close_new_final_data[index][12] = sum_close_round
                sum_victory = 0
                sum_fail = 0
                sum_death = 0
                sum_score = 0
                sum_close_round = 0
                sum_win_round = 0
                sum_fail_round = 0
                # print(new_final_data)
            else:
                close_map.append(i[0])
                close_final_data.append(i[0])  #map_name
                close_final_data.append(i[1])  #win_num
                close_final_data.append(round(i[1]*100/(i[1]+i[2]), 2))     #rate
                if i[4] == 0:                                       #S/D
                    close_final_data.append(0)
                else:  
                    close_final_data.append(round(i[3]/i[4], 2))
                close_final_data.append(round(i[4]*100/(int(i[5])+int(i[6])), 2))             #D/T
                if int(i[5]) == 0:                                     #D/W
                    close_final_data.append(0)
                else:
                    close_final_data.append(round((i[4]-int(i[6]))*100/int(i[5]), 2))
                for k in new_final_data:
                    if k[0] == i[0]:
                        total_round = k[1] + k[11]
                close_round += 1
                close_final_data.append(round(close_round*100/total_round, 2))      #close_rate
                close_final_data.append(i[3])                    #score
                close_final_data.append(i[4])                    #death
                close_final_data.append(int(i[5]))                    #win_round
                close_final_data.append(int(i[6]))                    #fail_round
                close_final_data.append(i[2])          #fail_num
                close_final_data.append(close_round)          #close_round
                close_new_final_data.append(close_final_data)
                close_final_data = []
                close_round = 0
            # print("map", map) 
        # print(new_final_data)
        def transfer_array(array):
            return [subarray[:-6] for subarray in array]
        close_result = transfer_array(close_new_final_data)
        a_close_result = [[x if not isinstance(x, (int, float)) else '{:.2f}'.format(x) for x in sublist] for sublist in close_result]
        

        #Create a CSV file
        key_data = [['Map', 'Win_num', 'Rate', 'S/D', 'D/TR', 'WD/WR', 'Close rate']]
        with open('close_result.csv', 'w', newline='', encoding='utf-8') as file:
            #Create a CSV writer object
            writer = csv.writer(file)

            #Write the data to the CSV file
            writer.writerows(key_data)            
            writer.writerows(a_close_result)
current_directory = os.getcwd()
folder_path = os.path.join(current_directory,"image")
file_names = get_file_names(folder_path)
folder_path_png = os.path.join(current_directory,"image_png")
file_names_png = get_file_names(folder_path)
for file_name_png in file_names_png:
    if os.path.exists("image_png/"+file_name_png):
        os.remove("image_png/"+file_name_png)
sleep(0.1)
for file_name in file_names:
    jpg2png(file_name)

folder_path = os.path.join(current_directory,"image_png")
file_names = get_file_names(folder_path)
with open('win.txt', 'w') as file:
    file.truncate(0)
with open('lose.txt', 'w') as file:
    file.truncate(0)
with open('all_data.txt', 'w') as file:
    file.truncate(0)
with open('table.csv', 'w') as file: # delete table
    file.write('')
sleep(0.1)
with open('fight.csv', 'w') as file: # delete table
    file.write('')
sleep(0.1)
with open('table.csv', 'a', newline='') as file:  #append header
    header_append = csv.writer(file)
    header_append.writerow(["result", "map", "score", "death", "win_round", "fail_round"])
with open('fight.csv', 'a', newline='') as file:  #append header
    header_append = csv.writer(file)
    header_append.writerow(["result", "map", "score", "death", "win_round", "fail_round"])    
for file_name in file_names:
    ocr_image("image_png/"+file_name)
    sleep(0.1)
    print("ocr ok")
sleep(0.1)
reswap()
print("reswap OK")
sleep(0.1)
lose_data() # extract the loose data
sleep(0.1)
print("lose ok")
win_data() # extract the win data
sleep(0.1)
print("win Ok")
fight()
sleep(0.1)
print("fight OK")
delete_data() #delete duplicate
sleep(0.1)
result_data()
print("result ok")

