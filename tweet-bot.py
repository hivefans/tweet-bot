from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time,random,os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

work_dir = os.path.dirname(os.path.abspath(__file__)) + "/session"
if not os.path.exists(work_dir):
    os.makedirs(work_dir)

class TwitterBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        options=Options()
        #options.add_argument('incognito')  # 隐身模式（无痕模式）
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('disable-extensions')
        options.add_argument('--user-data-dir=' + work_dir)
        options.add_argument("profile-directory=" + username)
        self.bot = webdriver.Chrome(options=options)
        self.bot.maximize_window()

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(3)
        if len(bot.find_elements(By.NAME, "text")) <= 0:
            print("Already Logined!")
            return True
        else:
            username = bot.find_element_by_name("text")
            username.clear()
            #password.clear()
            username.send_keys(self.username)
            time.sleep(2)
            element_login = bot.find_element_by_xpath('//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
            element_login.click()
            time.sleep(2) 
            element_pass = bot.find_element_by_name("password")
            element_pass.clear()
            element_pass.send_keys(password)
            time.sleep(2) 
            element_login = bot.find_element_by_xpath('//*[@data-testid="LoginForm_Login_Button"]')
            element_login.click()
            time.sleep(2) 
            loginError = bot.find_elements_by_xpath(
                "//span[contains(text(), 'match our records')]")  # not the best solution, sometimes works with few words
            time.sleep(5)
            if not loginError:
                print("Login Successful!")
                return True
            else:
                print("Your credentials were incorrect...\nBot is dead!")
                bot.close()
                return False
            print(loginError)
            time.sleep(5)

    def send_tweet(self,text):
        bot = self.bot
        element_text = bot.find_element_by_class_name("notranslate")
        element_text.click()
        element_text.send_keys(text)
        tweet_button = bot.find_element_by_xpath('//*[@data-testid="tweetButtonInline"]')
        bot.execute_script("arguments[0].click();", tweet_button)

    def find_action(self, term):
        links = list()
        counter = 1  # count the retrieved tweets
        bot = self.bot
        bot.get('https://twitter.com/search?q=' + term + '&src=typd')
        time.sleep(5)

        # Loop how many times we scroll down and new tweets are loaded
        for i in range(1, 5):
            # The tweet's url can be found in several positions in the DOM
            # tree, we fetch it once from the anchor tag containing the
            # word "status" (ex. https://twitter.com/tweet_author_name/status/some_digits)
            tweets = bot.find_elements_by_css_selector(
                'a[href*="status"]:not([href*=photo]):not([href*=retweets]):not([href*=likes]):not([href*=media_tags])')
            time.sleep(2)

            # Get the tweet's actual url and store them in a list
            tempLoopLinks = [elem.get_attribute("href") for elem in tweets]
            for x in tempLoopLinks:
                links.append(x)
            time.sleep(2)
            print("Loop " + str(i) + " complete!")

            # Scroll down in order to load new tweets
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(10)
        links = list(dict.fromkeys(links)) 
        
        for link in links:
            print(counter, link)
            bot.get(link)
            time.sleep(3)
            self.follow_user(link)
            self.like_retweet(link)
            counter = counter + 1
            time.sleep(1)

    def like_retweet(self,url):
        bot = self.bot
        #bot.get(url)
        try:
            like_button = WebDriverWait(bot, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Like']")))
            like_button.click()
        except:
            pass
        try:
            retweet_button = WebDriverWait(bot, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Retweet']")))
            retweet_button.click()
            retweet_confirm = WebDriverWait(bot, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='retweetConfirm']")))
            retweet_confirm.click()
        except:
            pass
        comment_text = WebDriverWait(bot, 3).until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']")))
        comment_text.send_keys(sq)
        time.sleep(2)
        replybutton=bot.find_element_by_css_selector('div[role="button"][data-testid="tweetButtonInline"]').click()
        print("一键三连成功")

    def follow_user(self,url):
        bot = self.bot
        #bot.get(url)
        page_cards = bot.find_elements_by_xpath('//div[@data-testid="UserCell"]')
        for card in page_cards:
            try:
                followbutton = WebDriverWait(bot, 3).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Follow"]')))
                followbutton.click()
                print("follow success")
                time.sleep(2)
            except:
                print("already following")

username = "user"
password = "pass"
sq=' good luck!'
term = "giveaway WL follow"
bix = TwitterBot(username, password)
loginSuccess = bix.login()
if loginSuccess:
    bix.find_action(term)
