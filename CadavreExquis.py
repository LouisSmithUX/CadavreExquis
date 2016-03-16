#!usr/bin/env python

import random
import requests
import json
import nltk
import os
from bs4 import BeautifulSoup


class Main:
    def __init__(self):
        self.names = self.prepare_names()
        self.places = self.prepare_places()

        self.generate_cadavre_exquis()

    def prepare_names(self):
        names = []
        name_files = ['facebookPeople.txt', 'famousPeople.txt', 'fictionalPeople.txt']
        for file in name_files:
            with open('data/' + file, 'r') as listOfNames:
                names += [line.strip() for line in listOfNames if line.strip() != '']
        return set(names)

    def prepare_places(self):
        places = []
        place_files = ['famousPlaces.txt', 'places.txt']
        for file in place_files:
            with open('data/' + file, 'r') as listOfPlaces:
                places += [line.strip().lower().capitalize() for line in listOfPlaces if line.strip() != '']
        return set(places)

    def get_quote(self):
        response = requests.post(
            "https://andruxnet-random-famous-quotes.p.mashape.com/cat=" + random.choice(['famous', 'movies']),
            headers={
                "X-Mashape-Key": "F7Y4R3CTqUmshzUWwj2J2WcyvHmXp1AeSsOjsnxby17uniAXmI",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
        )
        json_dic = response.json()
        return json_dic['quote']

    def get_conclusion(self):
        pass
        response = requests.get(
            "http://www.omdbapi.com/?i=tt" + str(random.randint(0, 5251600)).rjust(7, '0') + "&plot=short&r=json")

        response_json = response.json()
        if 'Plot' not in response_json or response_json['Plot'] in ['', 'N/A']:
            return ''
        sentences = [sentence for sentence in response_json['Plot'].split('.') if sentence!='']
        last_sentence = sentences[-1]
        words = nltk.word_tokenize(last_sentence)
        tags = nltk.pos_tag(words)
        for i, (w, tag) in enumerate(tags):
            if tag in ['NN','NNP','PRP']:
                tags[i] = ('they','PRP')
                break
        return ' '.join([w for w, tag in tags])

    def get_aphorism(self):
        url = 'http://www.aphorismsgalore.com/aphorisms/A-'+str(random.randint(1100,2760))
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        aphorism = soup.find("div", class_="nodeBody")
        return aphorism.p.text

    def generate_cadavre_exquis(self):
        name1, name2 = random.sample(self.names, 2)

        place = random.sample(self.places, 1)[0]

        quote1 = self.get_quote()
        quote2 = self.get_quote()

        conclusion = self.get_conclusion()
        tries = 1
        while not conclusion and tries < 10:
            conclusion = self.get_conclusion()
            tries += 1

        aphorism = self.get_aphorism()

        # format and print
        print(name1, name2, place, quote1, quote2, conclusion, aphorism, sep='\n')


if __name__ == "__main__":
    launcher = Main()
