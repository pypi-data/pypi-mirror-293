import json
import re
import os.path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle
import logging
import requests
import zipfile

logger = logging.getLogger(__name__)

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""


def generate_background(proxy_host, proxy_port, proxy_user, proxy_pass):
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
        """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
    return background_js


def get_chromedriver(proxy, host, use_proxy=False, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = webdriver.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        proxy_pattern = re.compile(
                r'^http://(?:([^:]+):([^@]+)@)?([^:]+):(\d+)$')
        match = re.match(proxy_pattern, proxy)
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr(
                    "background.js",
                    generate_background(match.group(3), match.group(4),
                                        match.group(1), match.group(2)))
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = webdriver.Remote(
        host,
        options=chrome_options)
    return driver


class TelegramAccount:
    base_url = "https://web.telegram.org"

    def __init__(self, account_name, sessions_dir, host, proxy_data=None, mobile_proxy=False, user_agent=None):
        self.account_name = account_name
        self.sessions_dir = sessions_dir
        os.makedirs(sessions_dir, exist_ok=True)
        if mobile_proxy:
            proxy_url = get_mobile_proxy(proxy_data)
        else:
            proxy_url = self.get_proxy()
        self.driver = get_chromedriver(proxy_url, host, use_proxy=proxy_url != "-", user_agent=user_agent)
        self.fetch_account()

    def get_proxy(self):
        try:
            with open(os.path.join(self.sessions_dir, f'{self.account_name}_proxy.txt'), 'r') as file:
                proxy = file.readline()
                return proxy
        except FileNotFoundError:
            # Request proxy from stdin until valid
            proxy_pattern = re.compile(r'^http://(?:\S+:\S+@)?\S+:\d+$')
            while True:
                proxy = input("Enter a proxy (format: http://username:password@host:port) or - to avoid proxy: ")
                if proxy == "-" or re.match(proxy_pattern, proxy) is not None:
                    print(f"Valid proxy entered: {proxy}")
                    with open(os.path.join(self.sessions_dir, f'{self.account_name}_proxy.txt'), 'w') as file:
                        file.write(proxy)
                    return proxy
                else:
                    print("Invalid proxy format. Please try again.")

    def save_state(self):
        cookies = self.driver.get_cookies()
        with open(os.path.join(self.sessions_dir, f'{self.account_name}_cookies.pkl'), 'wb') as file:
            pickle.dump(cookies, file)
        local_storage = self.driver.execute_script("return window.localStorage;")
        with open(os.path.join(self.sessions_dir, f'{self.account_name}_local_storage.json'), 'w') as file:
            json.dump(local_storage, file)

    def login(self):
        # Go to login page
        self.driver.get(self.base_url)

        input("Type any key, when login finished:")
        time.sleep(2)
        self.save_state()
        logger.warning(f"Logged into Telegram Account: {self.account_name}")

    def fetch_account(self):
        logger.warning(f"fetching account {self.account_name} data")
        try:
            self.driver.get(self.base_url)
            with open(os.path.join(self.sessions_dir, f'{self.account_name}_cookies.pkl'), 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            with open(os.path.join(self.sessions_dir, f'{self.account_name}_local_storage.json'), 'r') as file:
                local_storage = json.load(file)
                for key, value in local_storage.items():
                    self.driver.execute_script(f"window.localStorage.setItem(arguments[0], arguments[1]);", key, value)
            self.driver.refresh()
        except FileNotFoundError:
            logger.warning(f"No session data for {self.account_name}, log in manually.")
            self.login()

    def close(self):
        self.driver.quit()


def get_mobile_proxy(proxy):
    url = f"https://changeip.mobileproxy.space/?proxy_key={proxy['key']}&format=json"
    headers = {
        'User-Agent': "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.102011-10-16 20:23:10"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        if data['code'] == 200:
            return get_proxy_details(data['proxy_id'], proxy['authorization'])
        else:
            raise ValueError(f"Error in response: {data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


def get_proxy_details(proxy_id, authorization):
    url = f"https://mobileproxy.space/api.html?command=get_my_proxy&proxy_id={proxy_id}"
    headers = {
        'Authorization': f"Bearer {authorization}"
    }

    response = requests.get(url, headers=headers)

    proxy_data = response.json()[0]
    login = proxy_data['proxy_login']
    password = proxy_data['proxy_pass']
    new_ip = proxy_data['proxy_host_ip']
    port = proxy_data['proxy_http_port']

    return f"http://{login}:{password}@{new_ip}:{port}"
