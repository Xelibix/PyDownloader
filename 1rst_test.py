from tqdm import tqdm #Progress bar
from pyunpack import Archive #Unpacker
import requests #Download module
import os
import re
import shutil #Remove non empty folders

def dowloadfile(adresse):
    
    adresse=adresse.replace(chr(10), "") #remove new line
    chunk_size = 1000024                 #1MB
    url = adresse
    r = requests.get(url, stream = True,allow_redirects=True) #Permet de télécharger le fichier quand t est utilisé
    total_size = int(r.headers['content-length']) #Calcul le nombre d'octets sans télécharger le fichier
    print(total_size)
    try: #Avec redirection
        fname = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0] #Find name off file
        filename = fname.replace(chr(34), "") #enlève les "" de mort
    except: #Sans redirection
        filename = url.split("/")[-1]
    print(filename)
    with open(filename, 'wb') as f:
        for data in tqdm(iterable = r.iter_content(chunk_size = chunk_size), total = int((total_size/chunk_size)*0.954), unit = 'MB'): #Download file with progress bar
            print("")
            f.write(data) #Write in file
    print("Download complete!")
    print(filename)
    foldername = filename.replace(".zip", "")#Il faudra ajouter d'autres extensions
    if os.path.exists(foldername)==True: #Check if folder already exist
        print("Already exsit deleting...")
        shutil.rmtree(foldername)
    os.mkdir(foldername)
    Archive(filename).extractall(os.getcwd()+"/"+foldername) #Décompresse ou le script ce situe
    print(foldername+" Downloaded")



file = open("links.txt", "r")
numberoflinks = len(open("links.txt").readlines()) #Cumpt number of lines
print(numberoflinks)
for i in range (numberoflinks) : #Read lines by lines
    dowloadfile(file.readline())



