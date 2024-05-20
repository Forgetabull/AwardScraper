import xmltojson 
import json 
import requests 
import re
import os
import urllib
import pandas as pd

def get_text_between_tokens(text, start_token, end_token):
    # Define the regular expression pattern to find text between the start and end tokens
    pattern = re.escape(start_token) + '(.*?)' + re.escape(end_token)
    
    # Use re.findall() to find all occurrences of the pattern
    matches = re.findall(pattern, text, flags=re.DOTALL)
    
    return matches


def strip_text_between_tokens_incl_tokens(text, start_token, end_token):

    stripped_text = strip_text_between_tokens_keep_tokens(text, start_token, end_token)
    
    stripped_text = stripped_text.replace(start_token+end_token, '')
    return stripped_text

def strip_text_between_tokens_keep_tokens(text, start_token, end_token):
    # Define the regular expression pattern to find text between the start and end tokens
    pattern = '(' + re.escape(start_token) + ').*?(' + re.escape(end_token) + ')'
    
    # Use re.sub() to replace the matched text with the start and end tokens
    stripped_text = re.sub(pattern, r'\1\2', text, flags=re.DOTALL)
    
    return stripped_text


def scrapehtml2(url, category):

    # Headers to mimic the browser 
    headers = { 
	    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36" 
    } 

    # Get the page through get() method 
    html_response = requests.get(url=url, headers = headers) 
    
    html_response_text = html_response.text


    # Example usage
    start_token = '<h3 class="category">'
    end_token   = '</div>'

    extracted_texts = get_text_between_tokens(html_response_text, start_token, end_token)

    csvLines = list()

    for extracted_text in extracted_texts :
        csvLine = category.upper() + ','        
        extracted_text = extracted_text.replace('#', ' ')
        extracted_text = extracted_text.replace('&nbsp;', ' ')
        extracted_text = extracted_text.replace(',', ' ')
        extracted_text = extracted_text.replace('\n', ' ')
        extracted_text = extracted_text.replace('</h3>', '#')
        extracted_text = extracted_text.replace('</h4>', '#')
        extracted_text = strip_text_between_tokens_incl_tokens(extracted_text, '<h3', '>')
        extracted_text = strip_text_between_tokens_incl_tokens(extracted_text, '<h4', '>')
        extracted_text = extracted_text.replace('<div class="content">             <p>', '')
        extracted_text = extracted_text.replace('<br>', '')
        extracted_text = extracted_text.replace('</p>', '')
        extracted_text = extracted_text.replace('<br />', '')
        extracted_text = extracted_text.replace('<p>', '')
        extracted_text = extracted_text.replace('\r', '')
        extracted_text_tokens = extracted_text.split("#")

        secondToken = 0
        for token in extracted_text_tokens :
            secondToken = secondToken + 1
            token = token.strip()
            csvLine += token.upper()
            csvLine += ','
            if secondToken == 2 :
                #csvLine += '<a href="https://www.google.com/search?q=' + urllib.parse.quote_plus(token.upper()) + ">Google Search</a>"
                csvLine += 'https://www.google.com/search?q=' + urllib.parse.quote_plus(token.upper())
                csvLine += ','
                #                csvLine += '<a href="https://www.google.com/search?q=linkedin:' + urllib.parse.quote_plus(token.upper()) + ">LinkedIn Search</a>"
                csvLine += 'https://www.google.com/search?q=linkedin:' + urllib.parse.quote_plus(token.upper())
                csvLine += ','
        

        csvLine = csvLine.replace('  ', ' ')
        csvLine = csvLine[:-1]
        #print("Entry:")
        #print(csvLine)
        csvLines.append(csvLine)


    return csvLines

def getCategory(url, bitWeDontWant):
    return url.replace(bitWeDontWant,'')

def writeStringArrayToFile(lines, filename):

    # Open the file in write mode
    with open(filename, "a") as file:
        # Write each element of the array to the file line by line
        for line in lines:
            file.write("%s\n" % line)


# MAIN

if os.path.exists('output.csv'):
    # Delete the file
    os.remove('output.csv')

bitWeDontWant = 'https://www.telstra.com.au/small-business/best-of-business-awards/alumni/'

csvLines = []
csvLine = "AWARD CLASS,CATEGORY,NAME,GOOGLE,LINKEDIN,DESC"
csvLines.append(csvLine)
writeStringArrayToFile(csvLines, 'output.csv')


url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2023-national-winners"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2023-state-winners/act"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2023-state-winners/nsw"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2023-state-winners/nt"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2023-state-winners/qld"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2023-state-winners/sa"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2023-state-winners/tas"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2024-national-winners"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2024-state-winners/act"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2024-state-winners/nsw"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2024-state-winners/nt"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2024-state-winners/qld"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2024-state-winners/sa"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

url = "https://www.telstra.com.au/small-business/best-of-business-awards/alumni/2024-state-winners/tas"
print('Processing: ' + url)
category = getCategory(url, bitWeDontWant)
csvLines = scrapehtml2(url, category)
writeStringArrayToFile(csvLines, 'output.csv')

read_file_product = pd.read_csv (r'output.csv')
read_file_product.to_excel (r'output.xlsx', index = None, header=True)



