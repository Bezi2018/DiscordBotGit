import requests
from bs4 import BeautifulSoup
import re


def get_covid():
    url = "https://www.medonet.pl/zdrowie/zdrowie-dla-kazdego,zasieg-koronawirusa-covid-19--mapa-,artykul,43602150.html"
    headers = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    text = soup.get_text()  # getting text from page

    regexNumbers = re.compile(r'(\(\+)(\d+)( \d+)?(\))') # (+___ ___)
    regexTests = re.compile(r'(doby: )(\d+)( \d+)?') #(___ ___)

    resultNumbers = regexNumbers.findall(text)

    tests = regexTests.search(text).group()[6:]

    cases = "".join(resultNumbers[0][1:-1])
    recovered = "".join(resultNumbers[1][1:-1])
    deaths = "".join(resultNumbers[2][1:-1])


    return [tests, cases, recovered, deaths]
