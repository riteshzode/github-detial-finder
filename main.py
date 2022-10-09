import requests
from bs4 import BeautifulSoup
import pandas as pd

# copy the username from your GitHub ie name that is in the link
# eg: https://github.com/riteshzode
# github_user = "riteshzode"

github_user = input("Input Github Username: ")

print(f"Github Profile Link : https://github.com/{github_user}")

r = requests.get(f"https://github.com/{github_user}")

soup = BeautifulSoup(r.content, 'html.parser')

# Profile image link

profile_image_link = soup.select_one(selector=".avatar-user")["src"]

print(f"Profile Image Link : {profile_image_link}")


# Profile Bio

profile_bio = soup.select_one(selector=".user-profile-bio")

print(f"Profile Bio : {profile_bio.get_text()}")

# Profile Location


try:
    location = soup.select_one(selector=".p-label")

    print(f"Profile Location : {location.get_text()}")
except:
    print(f"Profile Location Not Given")

try:
    website = soup.select(selector=".Link--primary")
except:
    print("Profile social link Not Exist")
else:
    for i in website[:2]:
        if "achievements" not in i.get('href'):
            try:
                print(f"Profile social link : {i.get('href')}")
            except:
                pass

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
