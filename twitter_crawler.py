import re
import time
import tweepy
import requests

from datetime import datetime, timedelta

class Twitter:
    def __init__(self, access_token, access_token_secret, consumer_key, consumer_secret, accounts, color, min_ago):
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.accounts = accounts
        self.color = color
        self.min_ago = min_ago*-1

    def _crawl_twitter(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        all_tweet_infos = []
        for account in self.accounts:
            status = api.user_timeline(account, tweet_mode="extended")
            tweet_infos = []
            for idx in range(0, len(status)):
                if not status[idx]._json["entities"]["user_mentions"]:
                    tweet_info = {}
                    time_string = status[idx]._json["created_at"].replace("+0000 ", "")
                    t_format = datetime.strptime(time_string, "%a %b %d %H:%M:%S %Y") + timedelta(
                        hours=8
                    )
                    tweet_info["create_time"] = t_format
                    tweet_info["retweet_count"] = str(status[idx]._json["retweet_count"])
                    tweet_info["favorite_count"] = str(status[idx]._json["favorite_count"])
                    tweet_info["user_name"] = status[idx]._json["user"]["name"]
                    tweet_info["link_tweet"] = (
                        f"https://twitter.com/{account}/status/" + status[idx]._json["id_str"]
                    )
                    tweet_info["tweet_content"] = "\n".join(
                        re.split(r"\n+", status[idx]._json["full_text"])
                    )
                    tweet_infos.append(tweet_info)
            all_tweet_infos.append(tweet_infos)
        return all_tweet_infos

    def get_articles(self):
        all_tweet_infos = self._crawl_twitter()
        output = []
        time_limit = datetime.now() + timedelta(minutes=self.min_ago)
        if all_tweet_infos:
            for tweet_infos in all_tweet_infos:
                for tweet_info in tweet_infos:
                    if (tweet_info["create_time"]) >= time_limit:
                        output.append(
                            self._set_attachments(
                                self.color,
                                "TWITTER",
                                tweet_info["user_name"],
                                "",
                                tweet_info["link_tweet"],
                                tweet_info["tweet_content"],
                                tweet_info["retweet_count"],
                                tweet_info["favorite_count"],
                                str(tweet_info["create_time"]),
                            )
                        )
        return output

    def _set_attachments(
        self,
        color,
        forum,
        author_name,
        title,
        title_link,
        article_content,
        retweet_count,
        favorite_count,
        post_time,
    ):
        output = {
            "mrkdwn_in": ["text"],
            "color": color,
            "pretext": f"<!channel>\n{author_name} 最新 Tweet",
            "author_name": f"🖋{author_name}",
            "title": title,
            "title_link": title_link,
            "text": "內文:\n" + article_content + ("\n" * 2) + "文章連結:\n" + title_link,
            "fields": [{"title": "", "value": "", "short": False},],
            "thumb_url": "https://i.imgur.com/LS08Auh.jpg",
            "footer": f"Twitter 發文時間：{post_time}",
        }
        return output