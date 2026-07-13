import csv
from math import log
import secrets
import string
import logging
import requests
import argparse

# 設定日誌顯示格式
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def generate_password(length: int = 10) -> str:
    """使用 secrets 產生高強度且不含易混淆字元的密碼"""
    alphabet = string.ascii_letters + string.digits
    for c in "0Oo1lI":
        alphabet = alphabet.replace(c, '')
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_teams_and_accounts(api_url: str, api_user: str, api_pass: str, csv_filename: str):
    try:
        with open(csv_filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            teams_data = list(reader)
    except FileNotFoundError:
        logging.error(f"找不到檔案: {csv_filename}")
        return

    # 設定 API 驗證
    API_Base = "https://{}:{}@{}/api/v4".format(api_user, api_pass, api_url)
    account_info = []

    for idx, team in enumerate(teams_data, start=1001):
        team_name = team.get('name')
        category = team.get('category')

        if not team_name or not category:
            logging.warning(f"跳過無效的資料行 (缺少 name 或 category): {team}")
            continue

        check = input(f"Before creating team {idx}: {team_name}, ARE YOU SURE TEAM CATEGORY: {category} exists? (y/n): ")
        if check.lower() != 'y':
            logging.info(f"Skipping team {idx}: {team_name}")
            logging.info(f"Category {category} should be created on domjudge manually")
            continue

        # 1. 建立隊伍 (Team)
        team_payload = {
            "id": str(idx),
            "name": team_name,
            "display_name": f"{idx}: {team_name}",
            "group_ids": [str(category)]
        }

        try:
            logging.info(f"正在建立隊伍: {team_name} (ID: {idx}) ...")
            team_res = requests.post(API_Base + "/teams", json=team_payload)
            team_res.raise_for_status()
            created_team = team_res.json()

            team_id = str(created_team.get('id'))

            # 2. 建立該隊伍的帳號 (User / Account)
            password = generate_password(10)
            username = f"team{team_id}"

            user_payload = {
                "username": username,
                "name": team_name,
                "password": password,
                "team_id": int(team_id),
                "roles": ["team"]
            }

            logging.info(f"正在建立帳號: {username} ...")
            user_res = requests.post(API_Base + "/users", json=user_payload)
            user_res.raise_for_status()

            account_info.append({
                'id': team_id,
                'category': category,
                'name': team_name,
                'username': username,
                'password': password
            })
            logging.info(f"成功建立: {team_name} ({username})")

        except requests.exceptions.RequestException as e:
            logging.error(f"❌ 建立 {team_name} 失敗: {e}")
            if e.response is not None:
                logging.error(f"詳細錯誤訊息: {e.response.text}")
            continue

    # 3. 輸出成功名單
    if account_info:
        output_file = 'account_info.csv'
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'category', 'name', 'username', 'password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(account_info)
        logging.info(f"建立完畢！所有成功帳號資訊已儲存至 {output_file}")
    else:
        logging.warning("沒有成功建立任何隊伍與帳號。")

if __name__ == "__main__":
    # 使用 argparse 來處理命令列引數
    parser = argparse.ArgumentParser(description="DOMjudge API 隊伍與帳號建立工具")

    # 增加所需的引數
    parser.add_argument('-u', '--url', required=True, help="DOMjudge API v4 基礎網址 (例如: https://domjudge.example.com/api/v4)")
    parser.add_argument('-a', '--admin', required=True, help="管理員帳號")
    parser.add_argument('-p', '--password', required=True, help="管理員密碼")
    parser.add_argument('-f', '--file', default='team.csv', help="輸入的 CSV 檔案名稱 (預設: team.csv)")

    # 執行解析
    args = parser.parse_args()

    # 將解析出來的引數傳給主函式
    create_teams_and_accounts(
        api_url=args.url,
        api_user=args.admin,
        api_pass=args.password,
        csv_filename=args.file
    )
