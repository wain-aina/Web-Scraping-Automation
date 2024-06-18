from bs4 import BeautifulSoup
import lxml
import requests

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
data = response.text

soup = BeautifulSoup(data, 'html.parser')

titles = [title.getText().replace("â", "-") for title in soup.find_all(name="h3", class_="title")][::-1]

with open("movies.txt", mode="w") as file:
    for movie in titles:
        file.write(f"{movie}\n")

