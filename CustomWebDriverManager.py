# インポート
import logging
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager

class CustomWebDriverManager:
    """
    WebDriverを自動更新する\n
    browser:edge,chrome,is
    をそれぞれ返す
    注）seleniumのVerが古いとEdge.optionにadd_argumentsがないのでエラーになる
    """
    def __init__(self,browser):
        self.browser = browser.lower()
        # self.__setProxy()
        self.__set_option()
    
    def __setProxy(self): #命名規則に反する？
        """
        環境変数にproxyが設定されていない場合
        これを家の環境でやるとダメだと思う
        """
        try:
            os.environ["HTTPS_PROXY"]
        except KeyError:
            os.environ["HTTPS_PROXY"] = "" 
    def download(self):
        """
        browserに合わせてdiverをチェック/ダウンロード
        """
        if self.browser == "edge":
            return EdgeChromiumDriverManager(log_level=logging.INFO).install()
        elif self.browser == "chrome":
            return ChromeDriverManager().install()
        elif self.browser == "ie":
            return IEDriverManager(log_level=logging.INFO,os_type="win32").install() #32bit版のDriverになる
        else:
            print("Browser Error!")
            return
    def __set_option(self):
        #Edge,Chromeのオプション
        if self.browser == "chrome":
            from selenium.webdriver.chrome.options import Options
        else:
            from selenium.webdriver.edge.options import Options
        self.options = Options()
        #seleniumのバージョンによってOptionsの属性が異なる
        #hassattrでチェック
        if(hasattr(self.options,"add_argument")):
            self.options.add_argument("--headless")
            #Edge IEモードのオプション
            self.ie_options = webdriver.IeOptions()
            self.ie_options.attach_to_edge_chrome = True
            self.ie_options.edge_executablee_pah = r"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
        else:
            #msedge-selenium-toolsを使っている場合
            from msedge.selenium_tools import EdgeOptions,Edge
            self.options = EdgeOptions()
            self.options.use_chromium = True
            self.options.add_argument("--headless")

            #Edge IEモードのオプション
            self.ie_options = webdriver.IeOptions()
            self.ie_options.add_additional_option("ie.edgechromium",True)
            self.ie_options.add_additional_option("ie.edgepath","C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    def wakeup(self,headless=True):
        """
        browserの起動処理\n
        headless:True or False
        """
        if headless == False: #ヘッドレスじゃない場合
            if self.browser == "edge":
                return webdriver.Edge(self.download())
            elif self.browser == "chrome":
                return webdriver.Chrome(self.download())
            elif self.browser == "ie":
                return webdriver.Ie(self.download(),options=self.ie_options)
        else:
            if self.browser == "edge":
                return webdriver.Edge(self.download(),options=self.options)
            elif self.browser == "chrome":
                return webdriver.Chrome(self.download(),options=self.options)
            elif self.browser == "ie": #ieはヘッドレスに対応してない
                self.ie_options.add_argument("--headless")
                return webdriver.Ie(self.download(),options=self.ie_options)

