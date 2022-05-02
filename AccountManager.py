#インポート
from msilib.schema import Dialog
import os
import getpass
from tkinter import dialog

#keyring
import keyring
from keyring.errors import PasswordDeleteError,PasswordSetError

from Dialog import Dialog

class AccountManager:
    """
    資格情報マネージャーでユーザー名/パスワードを管理するクラス
    service_name:サービス名
    """
    def __init__(self,service_name):
        self.service_name = service_name
    def create_account(self):
        """
        新規作成
        """
        self.username = getpass.getuser() #ログイン名をユーザー名として取得
        dialog = Dialog("パスワード",show=True) #パスワード入力ダイアログ
        dialog.window_show()
        self.password = dialog.text #入力されたパスワードを取得
        #資格情報マネージャーに情報を設定
        if self.password == "": #空文字だったら
            print("Failed: Set password to Credential manager")
            return False
        keyring.set_password(self.service_name,self.username,self.password)
        print("Success: Set password to Credential Manager")
    def get_account(self):
        """
        資格情報取得
        戻り値：ユーザー名、パスワード
        """
        self.username = getpass.getuser() #ユーザー名
        credentials = keyring.get_credential(self.service_name,self.username)
        if credentials: #指定したサービス名があればパスワードを取得
            self.password = credentials.password
        else: #空＝サービス名がなかったら
            print("Service was not found. Create new account!")
            self.create_account()
        return self.username,self.password
    def delete_account(self):
        """
        対象のサービス名を削除する\n
        注）ダイアログは表示しない
        """
        self.username = getpass.getuser() #ユーザー名
        try:
            keyring.delete_password(self.service_name,self.username)
        except PasswordDeleteError:
            print("Failed: Delete Error Occur")
            return
        print("Success: Delete password from Credential Manager")
