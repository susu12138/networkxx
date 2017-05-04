import networkx as nx

import csv
import os
import json

dir_dict={"PhysRevA":"PRA",
          "PhysRevB":"PRB",
          "PhysRevD":"PRD",
          "PhysRevC":"PRC",
          "PhysRevLett":"PRL",
          "PhysRevE":"PRE",
          "PhysRevApplied":"PRAPPLIED",
          "PhysRevX":"PRX"
}
dir_data="G:\\zxj_home\\network\\aps-dataset-metadata-2015"
dir_file="G:\\zxj_home\\network\\aps-dataset-citations-2015.csv"
class network:
    def __init__(self,path=dir_file):
        self.path=path
        self.START=5938152
        self.END=6438152
    def scan_csv(self,str1,str2):
        sub1=str1[:6].upper()
        year1=int(str1[6:])
        sub2=str2[:6].upper()
        year2=int(str2[6:])
        with open(self.path) as csvfile:
            file = csv.reader(csvfile)
            mvp=["",-1]
            temp_mvp=["",0]
            temp_data2=""
            i=0
            for line in file:
                i+=1
                if i<self.START or i>self.END:
                    continue
                #print(i)
                try:
                    data1 = self.get_file_json(line[0])
                    if line[1]==temp_mvp[0]:
                        data2 = temp_data2
                    else:
                        data2=self.get_file_json(line[1])
                        temp_data2=data2
                except KeyError as err:
                    #print("scan_file filename key error,pass")

                    continue
                except FileNotFoundError as err:
                    #print("scan file file not find haha")
                    continue
                try:
                    t_sub1=data1["tocSection"]["label"][:6].upper()
                    t_year1=data1["date"][:4]
                    t_year2 = data2["date"][:4]
                except KeyError as err:
                    continue
                if t_sub1 != sub1 or t_year1!=year1:
                    continue
                try:
                    t_sub2 = data2["tocSection"]["label"][:6].upper()
                    t_year2 = data2["date"][:4]
                except KeyError as err:
                    continue
                if t_sub2!=sub2 or t_year2!=year2:
                    continue
                if temp_mvp[0]==line[1]:
                    temp_mvp[1]+=1
                else:
                    if temp_mvp[1]>mvp[1]:
                        mvp=temp_mvp
                        print("mvp:",end=" ")
                        print(mvp)
                    temp_mvp[0] = line[1]
                    temp_mvp[1] = 1
            print("ans:",end=" ")
            print(mvp)

    def get_file_json(self,str="10.1103/PhysRevA.89.012102"):

        paper = str
        journal = paper.split("/")[1]
        temp = paper.split("/")
        paper = temp[1]
        journal = journal.split(".")
        if journal[0] in dir_dict:
            file_path = os.path.join(dir_data, dir_dict[journal[0]], journal[1], paper + ".json")
        else:
            raise KeyError
        # print(file_path)
        try:
            f = open(file_path, encoding="utf8")
        except FileNotFoundError as err:
            # print("in get_file_json file not find")
            raise FileNotFoundError
        data = json.load(f)
        f.close()
        return data

a=network()
str2="Elemen2008"
str1="Beyond2009"
a.scan_csv(str1,str2)








