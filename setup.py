# setup the account and team for participants
import json
import csv
import random
import string

base_team_id = 1000

# generate password
def generate_password(length):
    letters = string.ascii_letters + string.digits

    # 移除容易混淆的字元 (0, O, o, 1, l, I)
    easy_confuse = "0Oo1lI"
    for c in easy_confuse:
        letters = letters.replace(c, '')

    return ''.join(random.choice(letters) for i in range(length))

# create team
def create_team():
    # read team name from .csv
    data = []
    ret = []
    with open('team.csv', newline='', encoding='utf-8') as csvfile:
        # one team per line
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    
    teams = []
    counter = 1
    for team in data:
        payload = {
            "name": team['name'],
            "display_name": "team_" + str(base_team_id + counter),
            "group_ids": [team['category']], # category
            "organization_id": "CCU",
            "id": str(base_team_id + counter),
        }
        print("creating team: ", payload)
        try:
            teams.append(payload)
            ret.append({"team_id": str(base_team_id + counter), "name": team['name'], "category": team['category']})
            counter += 1

        except Exception as e:
            print(e)

    with open('teams.json', 'w', encoding = 'utf-8') as f:
        json.dump(teams, f, indent=4, ensure_ascii=False)

    print("team creation done")
    return ret

# create account
def create_account(team_info):
    accounts = []
    for team in team_info:
        payload = {
            "id": team['team_id'],
            "username": "team" + team['team_id'],
            "password": generate_password(14),
            "type": "team",
            "team_id": team['team_id'],
            "name": team['name']
        }
        print("creating account: ", payload)
        try:
            accounts.append(payload)
        except Exception as e:
            print(e)

    with open('accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=4, ensure_ascii=False)

    for i in range(len(accounts)):
        accounts[i]['category'] = team_info[i]['category']

    # save some information for later use in the competition, e.g., team_id, username, password
    # file format: team_id, name, username, password, into a .csv file
    with open('account_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['team_id', 'category', 'name', 'username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for team in accounts:
            writer.writerow({'team_id': team['team_id'], 'category': team['category'], 'name': team['name'], 'username': team['username'], 'password': team['password']})

    print("account creation done")
    print("account information saved in account_info.csv")

team_info = create_team()
create_account(team_info)