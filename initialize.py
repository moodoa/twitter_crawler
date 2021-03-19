from twitter_crawler import Twitter

def article_collector(access_token, access_token_secret, consumer_key, consumer_secret, accounts, color, min_ago):
    twitter = Twitter(access_token,
                        access_token_secret,
                        consumer_key,
                        consumer_secret,
                        accounts,
                        color,
                        min_ago)
    articles = twitter.get_articles()
    attachments_list = []
    if articles:
        for article in articles:
            attachments_list.append(article)
    return attachments_list
