import csv
import re
import time
import requests
import os
import threading

# Open het invoerbestand voor lezen en het uitvoerbestand voor schrijven
with open('C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\\HC code\\Week 8\\CSV files\\Bol_com_reviews_metSterren.csv', 'r') as infile,  open('uitvoer.csv', 'w', newline='') as outfile:
    reader = csv.reader(infile)
    #writer = csv.writer(outfile)
    Linklijst = []

    # Schrijf de kopregel naar het uitvoerbestand
    #writer.writerow(['Link'])

    # Doorloop de rijen van het invoerbestand en haal de link eruit met behulp van reguliere expressies
    for row in reader:
        try:
            link = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', row[2])
            if link:
                # Schrijf de link naar het uitvoerbestand
                #writer.writerow(link)
                Linklijst.append(link)
        except:
            print('error at {row}')

download_folder = './Fotofolder/'
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

class ImageDownloader(threading.Thread):
    def __init__(self,link):
        threading.Thread.__init__(self)
        self.link = link

    def run(self):
        # Download de afbeelding
        response = requests.get(self.link)
        # Bepaal het bestandsnaam van de afbeelding
        filename = self.link.split('/')[-1]
        try:
            filename = filename.split('?')[0]
        except:
            print('')
        # Schrijf de afbeelding naar de map
        try:
            with open(os.path.join(download_folder, filename), 'wb') as f:
                f.write(response.content)
        except:
            url = download_folder + "/" + filename
            try:
                with open(os.path.join(url), 'wb') as f:
                    f.write(response.content)
            except:
                print(download_folder)
                print(self.link.split('/')[-1])
                url = download_folder + "/" + filename
                print(url)
                print("skipped")


threads = []
for link in Linklijst:
    # Start een nieuwe thread voor het downloaden van de afbeelding
    thread = ImageDownloader(link[0])
    thread.start()
    threads.append(thread)
    time.sleep(.1)

# Wacht tot alle threads zijn voltooid
for thread in threads:
    thread.join()
