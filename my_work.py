#! usr/bin/python
#coding=utf-8   。

import networkx as nx
import os
import json
import csv
dir_dict={"PhysRevA":"PRA",
          "PhysRevB":"PRB",
          "PhysRevD":"PRD",
          "PhysRevC":"PRC",
          "PhysRevLett":"PRL",
          "PhysRevE":"PRE",
          "PhysRevApplied":"PRAPPLIED",
          "PhysRevX":"PRX"
}
dir_write="D:\\data\\data\\aps-dataset-metadata-2015\\"
dir_data="D:\\data\\data\\aps-dataset-metadata-2015"
dir_csv="D:\\data\\data\\aps-dataset-citations-2015.csv"
dir_keys="D:\\data\\data\\aps-dataset-metadata-2015\\dict_keys.txt"
def get_file_json(str="10.1103/PhysRevA.89.012102"):


    paper=str
    journal=paper.split("/")[1]
    temp=paper.split("/")
    paper=temp[1]
    journal=journal.split(".")
    if journal[0] in dir_dict:
        file_path=os.path.join(dir_data,dir_dict[journal[0]],journal[1],paper+".json")
    else:
        raise KeyError
    print(file_path)
    f=open(file_path,encoding="utf8")
    data=json.load(f)
    f.close()
    #print(data)
    return data




def get_sub_info(data,writer):
    '''if "id" in data:
        print(data["id"])
        writer.write(data["id"]+"   ")
    else:
        print("no id")
    if "date" in data:
        print(data["date"])
        writer.write(data["date"]+"   ")
    else:
        print("no date")
    if "journal" in data:
        print(data["journal"]["id"])
    else:
        print("no journal")'''
    if "tocSection" in data:
        print(data["tocSection"]["label"])
        writer.write(data["tocSection"]["label"])
    else:
        print("no scetion")
    writer.write("\n")



'''
def get_sub_keys(data,writer):
    if "journal" in  data:
        print(data["journal"]["id"])
        writer.write(data["journal"]["id"]+" ")
    else:
        print("no journal")
        writer.write("nojournal ")

    for key in data.keys():
        writer.write(key+" ")
    writer.write("\n")'''

#data=get_file_json()
#get_sub_subject(data)
#get_sub_info(data)
def write_sub():
    with open(dir_csv,"r") as csvfile:
        reader=csv.reader(csvfile)
        writer_a=open(dir_write+"a.txt","w")
        writer_b=open(dir_write+"b.txt","w")
        writer_c = open(dir_write + "c.txt", "w")
        writer_e = open(dir_write + "e.txt", "w")
        i=1
        for line in reader:
            i+=1
            if(i<6900000):
                continue
            else:
                try:
                    data=get_file_json(line[1])
                except KeyError as err:
                    print("filename key error,pass")
                    continue
                if data["journal"]["id"]=="PRA":
                    get_sub_info(data,writer_a)
                elif data["journal"]["id"]=="PRB":
                    get_sub_info(data,writer_b)
                elif data["journal"]["id"]=="PRC":
                    get_sub_info(data,writer_c)
                elif data["journal"]["id"]=="PRE":
                    get_sub_info(data,writer_e)

                #print("\n")
        writer_a.close()
        writer_b.close()
        writer_c.close()
        writer_e.close()

def write_keys():
    with open(dir_csv,"r") as csvfile:
        reader = csv.reader(csvfile)
        writer=open(dir_keys,"w")
        i = 1
        for line in reader:
            i+=1
            if(i<6900000):
                continue
            else:
                try:
                    data=get_file_json(line[1])
                except KeyError as err:
                    print("filename can not find\n")
                    continue
                #get_sub_keys(data,writer)
        writer.close()

def gen_distinct_keys():
    d_keys={}
    with open(dir_write+"temp\\"+"e.txt","r") as cfile:
        for line in cfile:
            if line in d_keys.keys():
                d_keys[line]+=1
            else:
                d_keys[line]=1

    with open(dir_write+"e_d.txt","w") as wfile:
        for line in d_keys.keys():
            wfile.write(line)
gen_distinct_keys()




