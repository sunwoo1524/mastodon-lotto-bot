from mastodon import Mastodon
from time import sleep
import html2text
import random
import sys

"""
Please install package "Mastodon.py" and "html2text"!
pip install -r requirements.txt

Set your mastodon accesstoken in token.secret and change api_base_url
"""

mastodon = Mastodon(
    access_token = "token.secret",
    api_base_url = "https://pointless.chat/"
)

mentions = []
h = html2text.HTML2Text()


def check_mentions():
    try:
        notifications = mastodon.notifications(mentions_only = True)
    except:
        return

    for noti in notifications:
        mentions.append(noti)
        mastodon.notifications_dismiss(noti["id"])
    
    reply_mentions()


def reply_mentions():
    for mention in mentions:
        content = h.handle(mention["status"]["content"]).split()
        
        if content[1] == "추첨":
            if len(content) < 3:
                status = f"생성된 로또 번호는\n{lotto()} 입니다!\n복권은 소액으로 건전하게! 당첨 되시기를 바랍니다 :)"

                try:
                    mastodon.status_reply(in_reply_to_id = mention["status"]["id"], status = status, to_status = mention["status"])
                    print(status + "\n\n")
                except:
                    print("Not found toot")
            elif content[2] == "세트":
                lottonum = ""

                for _ in range(5):
                    lottonum += lotto() + "\n"
                
                status = f"생성된 로또 번호는\n{lottonum}입니다!\n복권은 소액으로 건전하게! 당첨 되시기를 바랍니다 :)"

                try:
                    mastodon.status_reply(in_reply_to_id = mention["status"]["id"], status = status, to_status = mention["status"])
                    print(status + "\n\n")
                except:
                    print("Not found toot")

        mentions.pop(0)


def lotto():
    nums = list(range(1, 46))
    picked_nums = []

    for _ in range(6):
        i = random.randint(0, len(nums) - 1)
        picked_nums.append(nums[i])
        nums.pop(i)

    picked_nums.sort()

    result = ""

    for n in picked_nums:
        result += f"{n} "

    return result[:-1]


while True:
    check_mentions()

    sleep(5)
