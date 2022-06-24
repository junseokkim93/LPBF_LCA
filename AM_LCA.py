import os
import csv
from pathlib import Path
from pprint import pprint
from copy import deepcopy
import logging, datetime

import pandas as pd
import brightway2 as bw
import tkinter as tk

class LCA:
    def __init__(self, input_data):
        self.input_data = input_data
        method = ("IPCC 2013", "climate change", "GTP 100a")
        excel_AM_process = bw.Database("excel_AM_process")
        ref_process= [act for act in excel_AM_process if act["name"]=="Finished Cargo Door hinge"][0]
            
        functional_unit = {ref_process:1.223}
        lca = bw.LCA(functional_unit, method)
        lca.lci()
        lca.lcia()
        # lca.score      
# import bw2io
# lca.top_emissions()
# lca.top_activities()
# from collections import defaultdict

# def top_emissions_by_name(lca, biosphere_database='biosphere3'):
    # names = defaultdict(list)

    # for flow in bw.Database("biosphere3"):
        # if flow.key in lca.biosphere_dict:
            # names[flow['name']].append(
                # lca.characterized_inventory[lca.biosphere_dict[flow.key], :].sum()
            # )
    
    # return sorted(
        # [(sum(scores), name) for name, scores in names.items()], 
        # reverse=True
    # )

# top_emissions_by_name(lca)[:5]
# from collections import defaultdict

# def top_processes_by_name(lca, technosphere_database='ecoinvent 3.8_cutoff_ecoSpold02'):
    # names = defaultdict(list)

    # for flow in ei_db:
        # if flow.key in lca.activity_dict:
            # names[flow['name']].append(
                # lca.characterized_inventory[:, lca.activity_dict[flow.key]].sum()
            # )
    
    # return sorted(
        # [(sum(scores), name) for name, scores in names.items()], 
        # reverse=True
    # )

# top_processes_by_name(lca)[:5]
# bw2io.export.excel.write_lci_excel("excel_AM_process")        
        
class AM_Data:

    def __init__(self, file_path, ecoinvent_file_path, db_name_ecoinvent ):
    
        global design_n
        logging.basicConfig(filename="Design {}.log".format(design_n), level=logging.INFO)
        
        self.db_name = self.get_db_name(file_path)
        bw.projects.set_current(self.db_name)
        
        if not self.db_name in bw.databases:
            self.assure_ei_bio_existence(ecoinvent_file_path, db_name_ecoinvent)
                    
            if not self.file_ready(file_path):
                self.act_search_history = {}
                self.create_db_from_csv(file_path)
                self.ei_db = bw.Database(db_name_ecoinvent)
                self.bio_db = bw.Database("biosphere3")
            else:
                self.create_db_from_excel(file_path, db_name_ecoinvent)
                
        logging.info("Finished loading {} data, {} and biosphere3".format(self.db_name, db_name_ecoinvent))
        
        self.input_data = bw.Database(self.db_name)
           
    def get_db_name(self, file_path):
        
        if self.file_ready(file_path):
            xl = pd.ExcelFile(file_path)
            
            for i in xl.sheet_names:
                
                df = pd.read_excel(file_path, sheet_name=i, header=None)
                
                for _, row in df.iterrows():

                    if row.iloc[0].lower()=="skip":
                        break
                        
                    if row.iloc[0].lower()=="database":
                        return row.iloc[1]
        else:
            with open(file_path, mode="r", encoding="utf-8-sig") as file:
                first_row = next(file).split(",")
            
        if first_row[0].lower()!="database":
            raise Exception("The first cell shall be 'Database'")
            
        return first_row[1]  
        
    @staticmethod    
    def file_ready(file_path):
        with open(file_path, 'rb') as f:
            first_four_bytes = f.read()[:4]
            return first_four_bytes == b'PK\x03\x04'     
            
    @staticmethod
    def assure_ei_bio_existence(ecoinvent_file_path, db_name_ecoinvent):
        logging.info(datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p"))
        logging.info("Checking if biosphere and ecoinvent exist...\n")
        
        if "biosphere3" not in bw.databases:
            logging.info("biosphere3 does not exists. Importing biosphere3...\n")
            bw.bw2setup()
        logging.info("biosphere3 exists.\n".format(db_name_ecoinvent))
        
        if db_name_ecoinvent not in bw.databases:
            logging.info("Ecoinvent does not exists. Importing ecoinvent {}...\n".format(db_name_ecoinvent))
            Ecospold_Importer = bw.SingleOutputEcospold2Importer(ecoinvent_file_path, db_name_ecoinvent, use_mp=False) 
            Ecospold_Importer.apply_strategies()
            Ecospold_Importer.statistics()
            Ecospold_Importer.write_database() 
        logging.info("Ecoinvent {} exists.\n".format(db_name_ecoinvent))

        
    @staticmethod    
    def check_empty_csv(file_path):
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            csv_reader = csv.reader(file)
            empty_list = []
            for row in csv_reader:
                empty_list += row
        return empty_list==[] 
        
    def create_db_from_excel(self, file_path, db_name_ecoinvent): 
        db_name = self.db_name
        locals()[db_name] = bw.ExcelImporter(file_path)
        locals()[db_name].apply_strategies()
        locals()[db_name].match_database(fields=('name', 'code'))
        locals()[db_name].match_database(db_name_ecoinvent, fields=('name', 'location', 'unit'))
        locals()[db_name].match_database("biosphere3", fields=('name', 'unit','location','code'))
        locals()[db_name].statistics()
        locals()[db_name].write_excel()
        
    def create_db_from_csv(self, file_path):

        if self.check_empty_csv(file_path):
            raise Exception("{} has no contents.".format(file_path))    
            
        db_dict = dict([])
        
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            
            csv_reader = csv.reader(file)
            db_name = self.db_name
            for _ in range(2):
                next(csv_reader)
            
            flag="act"

            for row in csv_reader:
                
                if "".join(row)=="":
                    if csv_reader.line_num>2:
                        if flag=="act":
                            db_dict[(db_name, act_dict["code"])] = act_dict
                            db_dict[(db_name, act_dict["code"])]["name"] = activity_name
                        elif flag=="exc":
                            db_dict[(db_name, act_dict["code"])]["exchanges"] = exchanges
                        
                    continue
                    
                if row[0].lower()=="activity":
                    act_dict = dict([])
                    activity_name = row[1]
                    flag = "act"
                    continue
            
                if row[0].lower()=="exchanges":
                    exc_dict = dict([])
                    flag = "exc"
                    exchanges = []
                    continue

                if flag=="act":
                    act_dict[row[0]] = row[1]
                    
                if flag=="exc":
                    if row[0].lower()=="name":
                        for key in row:
                            if key!="":
                                exc_dict[key]=""
                    else:
                        for key, value in zip(exc_dict.keys(), row):
                            exc_dict[key]= value
                        
                        self.process_exc_dict(file_path, exc_dict, db_dict)    
                        exchanges.append(deepcopy(exc_dict))
                        exc_dict.pop("database"); exc_dict.pop("code"); 
               
        db_dict[(db_name, act_dict["code"])]["exchanges"] = exchanges            

        db = bw.Database(db_name)
        db.write(db_dict) 
        
    def process_exc_dict(self, file_path, exc_dict, db_dict):
    
        exc_dict["amount"] = float(exc_dict["amount"])
        # find if the activity exists within our excel file
        if exc_dict["type"]=="production" or exc_dict["type"]=="technosphere":

            with open(file_path, mode="r", encoding="utf-8-sig") as file:

                csv_reader = csv.reader(file)
                db_name = self.db_name
                
                for row in csv_reader:   
                    if row[0].lower()=="activity" and exc_dict["name"]==row[1]:
                        
                        while(row[0].lower()!="code"):
                            row = next(csv_reader)
                        exc_dict["database"], exc_dict["code"] = db_name, row[1]
                        exc_dict["input"] = db_name, row[1]
                    continue
            
        if exc_dict.get("database"):
            return
        
        if exc_dict["type"]=="technosphere":
            db = self.ei_db
        elif exc_dict["type"]=="biosphere":
            db = self.bio_db
        
        (exc_dict["name"], 
         exc_dict["code"], 
         exc_dict["unit"], 
         exc_dict["database"],
         exc_dict["location"],
         exc_dict["input"]) = self.search_from_database(exc_dict["name"], db)     
         
    def search_from_database(self, name, db):
        act_list = db.search(name)
        
        if name not in [keys for keys in self.act_search_history]:
            pprint({num: elem for num, elem in zip(range(len(act_list)),act_list)})
            print()
            idx = int(input("which one do you mean by '{}'? Enter the index:".format(name)))
            print()
            act = act_list[idx]
            self.act_search_history[name] = act
        else:
            act = self.act_search_history[name]
            
        return (act["name"],
                act["code"],
                act["unit"],
                act["database"],
                act.get("location"),
                (act["database"],act["code"]))    


def main():
    
    input_file_path =  Path(r"C:\Users\kim\Desktop\Brightway2\EMI_related\AM_process.xlsx")
    ecoinvent_file_path = Path(r"C:\Users\kim\Desktop\Brightway2\ecoinvent 3.8_cutoff_ecoSpold02\datasets")
    db_name_ecoinvent =  "ecoinvent 3.8_cutoff_ecoSpold02"
    
    global design_n
    design_n = 0
    # conversion of the unit to the standard shall be done beforehand
    # Also sign as well...   
    am_data = AM_Data(input_file_path, ecoinvent_file_path, db_name_ecoinvent)
    # LCA(am_data.input_data)
    
main()
# if __name__ == "__main__":
    # main()
