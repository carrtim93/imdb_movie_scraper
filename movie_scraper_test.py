from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from random import randint
from IPython.core.display import clear_output
from warnings import warn

pages = [str(i) for i in range(1, 5)]
years_url = [str(i) for i in range(2012, 2020)]

names = []
years = []
imdb_ratings = []
metascores = []
votes = []

start_time = time.time()
reqs = 0

# for every year in the interval 2012-2019
for year_url in years_url:
    for page in pages:
        source = requests.get(f'http://www.imdb.com/search/title?release_date={year_url}&sort=num_votes,desc&page={page}')

        time.sleep(randint(8, 15))

        reqs += 1
        elapsed_time = time.time() - start_time
        print(f'Requests: {reqs}; Frequency: {reqs/elapsed_time}')
        clear_output(wait=True)

        # throw a warning for non 200 code
        if source.status_code != 200:
            warn(f'Request: {reqs}; Status code: {source.status_code}')

        # break if num of reqs is greater than expected
            if reqs > 72:
                warn('Number of requestes was greater than expected.')
                break

        html_soup = BeautifulSoup(source.text, 'lxml')

        movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

        for container in movie_containers:
            if container.find('div', class_='ratings-metascore') is not None:
                name = container.h3.a.text
                names.append(name)

                year = container.h3.find('span', class_='lister-item-year').text
                years.append(year)

                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                m_score = container.find('span', class_='metascore').text
                metascores.append(int(m_score))

                vote = container.find('span', attrs={'name':'nv'})['data-value']
                votes.append(int(vote))


movie_ratings_df = pd.DataFrame({'movie': names,
                                 'year': years,
                                 'imdb': imdb_ratings,
                                 'metascore': metascores,
                                 'votes': votes})
movie_ratings_df.to_pickle('./movie_rating_df.pkl')
movie_ratings_df.to_csv('./movie_rating_df.csv')
