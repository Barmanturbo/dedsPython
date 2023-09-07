import csv

with open('C:\\Users\\Burto\\Downloads\\GO-databases DEDS-week 4 & 5\\HC code\\Week 9\\BolSentiment.csv', newline='', encoding='utf-8') as infile, open('reviews_fixed.csv', mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')

    # Write headers
    headers = next(reader)
    headers.append('first_5_words')
    writer.writerow(headers)

    # Write rows
    for row in reader:
        if len(row) >= 2:
            review = row[1]
            first_5_words = " ".join(review.split()[:5])
            inhoud = " ".join(review.split()[5:])
            row[1] = inhoud
            row.append(first_5_words)
            writer.writerow(row)

print('Done')