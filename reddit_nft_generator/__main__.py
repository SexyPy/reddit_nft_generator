import json
import random
import string

import httpx
from bs4 import BeautifulSoup


def get_random_string(length) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def download(avatar):
    with httpx.stream("GET", avatar) as avatar_content:
        with open(f"{get_random_string(15)}.png", "wb") as f:
            for chunk in avatar_content.iter_raw(chunk_size=8192):
                f.write(chunk)


class Reddit:
    def __init__(self) -> None:
        self.username = ""
        self.password = ""
        self.session = httpx.Client()
        self.api = {
            "login": "https://www.reddit.com/login/",
            "login2": "https://www.reddit.com/login",
            "avatar": "https://snoovatar.reddit.com/api/snoovatars/random:byId",
        }

    def login(self) -> json:
        csrf_token = self.get_csrf_token()
        payload = f"csrf_token={csrf_token}&otp=&password={self.password}&dest=https%3A%2F%2Fwww.reddit.com&username={self.username}"
        self.session.post(self.api["login2"], data=payload).json()
        return self.session.cookies["reddit_session"]

    def get_csrf_token(self) -> str:
        reddit_login_content = self.session.get(self.api["login"]).text
        soup = BeautifulSoup(reddit_login_content, "html.parser")
        return soup.find("input", {"name": "csrf_token"}).get("value")

    def get_random_nft(self, reddit_session):
        headers = {"cookie": f"reddit_session={reddit_session};"}
        return self.session.get(
            "https://snoovatar.reddit.com/api/snoovatars/random:byId", headers=headers
        ).json()["image_url"]


if __name__ == "__main__":
    reddit = Reddit()
    login = reddit.login()
    avatar = reddit.get_random_nft(login)
    download(avatar)
