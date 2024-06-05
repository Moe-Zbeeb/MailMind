from main import Main
from spacy_extractor import SpacyExtractor    
import extract_msg
import os      
a = Main("/home/mohammad/Desktop/pj1/data","/home/mohammad/Desktop/pj1/data/output.csv","sales")    
# example = "/home/mohammad/Desktop/pj1/test/Levon _ I hope you don't mind me reaching out to you_.msg"
a.extract() 
# mymsg = extract_msg.Message(example) 
# print(mymsg.sender) 
# print(mymsg.recipients) 
# print(mymsg.subject)
# print(mymsg.date) 
# print(mymsg.body)
 