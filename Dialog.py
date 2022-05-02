#インポート
import tkinter as tk
import tkinter.font
import sys

class Dialog:
    def __init__(self,label_name = "", show=False) :
        """
        任意の値を登録するためのダイアログを生成
        label_name:表示されるラベル
        show:入力の非表示。Trueで"*"表示
        """
        self.lable_name = label_name
        self._text = "" #空文字にする
        self.show = show
    #tkinterのcommandはラムダかコールバックにしないと引数をとれない
    def callback(self,func,text1,window):
        def call_def():
            return func(text1,window)
        return call_def
    #入力されたテキストの取得
    def get_inputed_data(self,text1,window):
        self._text = text1.get() #空でもそのまま返す
        self.window_close(window)
    
    @property #getter
    def text(self):
        return self._text
    
    def callback2(self,func,window): #関数名の付け方がよろしくないorz
        def call_def():
            return func(window)
        return call_def
    def window_close(self,window):
        window.destroy()
    def cancel_click(self,window):
        window.destroy()
        # sys.exit() # jupyterの時は不要

    #GUI
    def window_show(self):
        root = tk.Tk()
        font_family = tk.font.Font(family="Meiryo UI", size=16)
        root.title(self.lable_name + "登録") #hogehoge登録と表示される
        root.geometry("300x100")
        label1 = tk.Label(root,text=self.lable_name,font=font_family)
        label1.grid(row=1,column=1,padx=10)
        text1 = tk.Entry(root,show="*",width=30) if self.show == True \
        else tk.Entry(root,width=30)
        text1.grid(row=1,column=3)
        btn = tk.Button(root,text="登録",font=font_family,
                        command=self.callback(self.get_inputed_data,text1,root))
        btn.grid(row=3,column=3,sticky=tk.W)
        btn_cancel = tk.Button(root,text="キャンセル",font=font_family,
                        command=self.callback2(self.cancel_click,root))
        btn_cancel.grid(row=3,column=3,sticky=tk.E,padx=10)
        root.mainloop()