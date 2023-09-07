import csv

sentiment_count = {'-1': 0, '0': 0, '1': 0} # een dictionary om het aantal voorkomens van elke waarde bij te houden

with open('C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\\HC code\\Week 9\\BolSentiment.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        sentiment_count[row['sentiment']] += 1 # verhoog het juiste teller voor elke voorkomen waarde

print('Aantal voorkomens van sentiment -1:', sentiment_count['-1'])
print('Aantal voorkomens van sentiment 0:', sentiment_count['0'])
print('Aantal voorkomens van sentiment 1:', sentiment_count['1'])
