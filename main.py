from collections import defaultdict
from functools import cmp_to_key
from datetime import datetime
import re
import requests


access_token = '95b99cff95b99cff95b99cff3695c28249995b995b99cfff443e38afa2f007ca65de6de'


def find_id(uid):
    if "https://vk.com/" in uid:
        uid = uid[15:]
    if "id" in uid:
        uid = uid[2:]
    return uid


def make_date_good(date):
    reg_good = r'(?:\d{2})(?:\.\d{2})(?:\.\d{4})'
    reg_bad1 = r'(?:\d{2})(?:\.\d)(?:\.\d{4})'
    reg_bad2 = r'(?:\d{1})(?:\.\d{2})(?:\.\d{4})'
    reg_bad3 = r'(?:\d{1})(?:\.\d{1})(?:\.\d{4})'
    if re.match(reg_good, date):
        return date
    if re.match(reg_bad1, date):
        return date[0:3] + '0' + date[3:]
    if re.match(reg_bad2, date):
        return '0' + date
    if re.match(reg_bad3, date):
        return '0' + date[0:2] + '0' + date[2:]

def comp(item1, item2):
    if item1[1] == item2[1]:
        if item1[0] < item2[0]:
            return -1
        elif item1[0] > item2[0]:
            return 1
        elif item1[0] == item2[0]:
            return 0
    elif item1[1] < item2[1]:
        return 1
    elif item1[1] > item2[1]:
        return -1

def make_sort_list(maped):
    ans = list()
    for key, val in maped.items():
        ans.append((key, val))
    ans = sorted(ans, key=cmp_to_key(comp))
    return ans



def calc_age(uid):
    uid = find_id(str(uid))
    base_url = "https://api.vk.com/method"
    req1 = requests.get(f"{base_url}/users.get?v=5.81&access_token={access_token}&user_ids={uid}")
    uid = req1.json()['response'][0]['id']
    req2 = requests.get(f"{base_url}/friends.get?v=5.81&access_token={access_token}&user_id={uid}&fields=bdate")
    friends = req2.json()['response']['items']
    answer = defaultdict(int)
    regexpr = r'(?:\d{1,2})(?:\.\d{1,2})(?:\.\d{4})'
    for human in friends:
        if human.setdefault('bdate') == None:
            continue
        if re.match(regexpr, human['bdate']):
            date_bad = make_date_good(human['bdate'])
            today = datetime.today()
            past = int(date_bad[-4:])
            answer[(today.year - past)] \
                = answer[(today.year - past)] + 1
    return make_sort_list(answer)


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)