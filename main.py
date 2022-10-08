import requests
from bs4 import BeautifulSoup
import pandas as pd

# copy the username from your GitHub ie name that is in the link
# eg: https://github.com/riteshzode
# github_user = "riteshzode"

github_user = input("Input Github Username: ")

r = requests.get(f"https://github.com/{github_user}")

soup = BeautifulSoup(r.content, 'html.parser')

profile_image_link = soup.select_one(selector=".avatar-user")["src"]

print(f"Profile Image Link : {profile_image_link}")

project_name = []
project_link = []

for i in range(1, 5):
    # if you have more than 100 Repositories then you can change the range to 10 ie range(1, 10)

    # if this code give error then use try and expect
    r = requests.get(f"https://github.com/{github_user}?page={i}&tab=repositories")

    soup = BeautifulSoup(r.content, 'html.parser')

    repos = soup.find_all(class_="wb-break-all")

    for repo in repos:
        project_name.append(repo.a.text.strip())
        project_link.append(f"https://github.com{repo.a['href']}")


print(f"Number of Repositories : {len(project_name)}")

dict = {"Repository Name": project_name, "Repository Link": project_link}

df = pd.DataFrame(dict)

df.to_csv("github_repo.csv")

print("File created")