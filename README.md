# tweet-bot
Selenium based solution for creating a twitter bot. Selenium is a very powerful tool for web automation and scraping. For making Twitter bot, one can use Twitter api, but its paid. This solution on the other hand is not but does require much more work to get things right. 

## Features:
- Logging into your Twitter account
- Searching for some keyword or hashtag
- Follow,Like,retweet,reply tweets of the search results
- Posting tweets

## Running project locally:

 1. Have `python3` environment setup
 2. Clone the repo and go to the cloned directory
 3. Run `pip3 install selenium`
 4. Set up your username, password and search keywords and reply text
 4. Now you may run "python3 tweet-bot.py"

 # 推特机器人
 该项目基于selenium开发，之所以没使用twitter api是因为不容易申请，有很多限制，容易被封等问题，
 
 ## 主要特点
 - 自动登录，保存登录记录，避免每次重复登录
 - 搜索关键词和hashtag标签
 - 关注、喜欢、转推、回复搜索结果
 - 发送推文

 主要用途可以使用该机器人搜索抽白名单关键词，自动完成一键三连。