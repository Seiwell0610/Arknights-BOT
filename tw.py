import tweepy

#各種キー・トークン
CONSUMER_KEY = "R7ZxacyJRiQTYH6SmYut6vSXf"
CONSUMER_SECRET = "CmtD0xsjPm1G6tlE7g9Xedgi9OoUJvKzJ4pW4buPCJtSZmaC9t"
ACCESS_TOKEN = "1160348809450311682-dsxLEbWCeNSa1EbuoP3Oixht2skks9"
ACCESS_TOKEN_SECRET = "731Mv1ekdaYo1hdbHXnKyGcipcMN6jWTsKtG4KJOhWqI1"

#認証
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#APIインスタンスを作成
api = tweepy.API(auth)

#キー・トークンの流出注意。流出すると最悪の場合乗っ取られる。
