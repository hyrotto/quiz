import pandas as pd
import tkinter as tk
from tkinter import messagebox as mbox
import tkinter.ttk as ttk
from functools import partial
import sys
import os

#pyinstallerでのファイルパス参照用
def resourcePath(filename):
  if hasattr(sys, "_MEIPASS"):
      return os.path.join(sys._MEIPASS, filename)
  return os.path.join(filename)

#問題文の自動改行
def on_config(event):
    event.widget.config(width=root.winfo_width())

#出題中かの確認用フラグ
is_activ = False

#出題用関数
def start():
    global quiz_frame,current_num,start_num,end_num,quiz_list,is_activ,count

    #同時に出題するのを回避するための処理
    if is_activ == True :
        raise mbox.showerror("","すでに出題中です。")
    is_activ = True

    #エントリ値の取得
    try:
        start_num = int(entry1.get())
        end_num = int(entry2.get())
        count = 1
        current_num = start_num

        if start_num < 1 or end_num < 1:
            is_activ = False
            raise mbox.showerror("入力エラー", "無効な問題番号です。")
        if end_num < current_num:
            is_activ = False
            raise mbox.showerror("入力エラー", "終了番号が開始番号より小さです。")
    except ValueError:
        is_activ = False
        mbox.showerror("入力エラー", "問題番号には整数を入力してください。")
        return
    
    #csvからデータフレームに読み込み
    quiz_list = load_quiz_list(start_num, end_num)

    #シャッフル
    if selected_value.get() == 1:
        quiz_list = quiz_list.sample(frac=1).reset_index(drop=True)
    
    #出題用フレーム
    quiz_frame = tk.Frame(root,padx=5,pady=5,relief=tk.RAISED, bd=2)
    quiz_frame.pack(expand=True,fill = tk.BOTH	,side = tk.TOP)
    
    show_mondai_str()

#出題停止用関数
def end():
    global quiz_frame,current_num,start_num,end_num,quiz_list,is_activ,count
    quiz_frame.destroy()
    is_activ = False

#指定された範囲の問題を取り出す関数
def load_quiz_list(start_num, end_num):
    df = pd.read_csv(resourcePath("quiz_list/minhaya_list.csv"))
    return df.loc[start_num-1:end_num-1, :]

#問題文のフレームを生成
def show_mondai_str():
    
    mondai_str = quiz_list.iloc[count-1,0]
    kaitou_str = quiz_list.iloc[count-1,1]

    #出題数表示
    tk.Label(quiz_frame,text=str(count)+"/"+str(end_num-start_num+1) ,font=("meiryo", 20)).pack(anchor=tk.NW)

    #問題文表示
    tk.Label(quiz_frame,text="問題文",font=("meiryo", 20, "bold")).pack(anchor=tk.NW)
    Mondai = tk.Message(quiz_frame,font=("MSゴシック", "15"),text=mondai_str,width=700)
    Mondai.pack(side=tk.TOP)
    Mondai.bind("<Configure>",on_config)

    #解答表示
    tk.Label(quiz_frame,text="解答",font=("meiryo", 20, "bold")).pack(anchor=tk.NW,pady=10)
    result = tk.Label(quiz_frame,text="ここに解答を表示",font=("MSゴシック", "15"))
    result.pack(fill = tk.X,side = tk.TOP)
    tk.Button(quiz_frame,text="解答",command=partial(answer,result,kaitou_str)).pack(side=tk.TOP)

    #問題移動用フレーム
    button_frame = tk.Frame(quiz_frame)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X)
    tk.Button(button_frame,text="次の問題へ進む",command=next).pack(side=tk.RIGHT)
    tk.Button(button_frame,text="前の問題へ戻る",command=previous).pack(side=tk.LEFT)
    

#解答を表示ボタンに連動する関数
def answer(result,kaitou_str):
    result['text'] = kaitou_str
    result.update

#次の問題に進むボタンに連動する関数
def next():
    global current_num, end_num,quiz_frame,is_activ,count
    current_num += 1
    count += 1
    quiz_frame.destroy()
    if current_num <= end_num:
        quiz_frame = tk.Frame(root,padx=5,pady=5,relief=tk.RAISED, bd=2)
        quiz_frame.pack(expand=True,fill = tk.BOTH	,side = tk.TOP)
        show_mondai_str()
    else:
        is_activ = False
        mbox.showinfo("終了", "全ての問題が終了しました。")

#前の問題に進むボタンに連動する関数
def previous():
    global current_num,quiz_frame,count
    if count == 1:
        return
    else :
        current_num -= 1
        count -= 1
        quiz_frame.destroy()
        quiz_frame = tk.Frame(root,padx=5,pady=5,relief=tk.RAISED, bd=2)
        quiz_frame.pack(expand=True,fill = tk.BOTH	,side = tk.TOP)
        show_mondai_str()


#メインウィンド
if __name__ == '__main__':
    #メインウィンドを定義
    root = tk.Tk()
    root.geometry("900x500")
    root.title("クイズ出題くん")

    #上部フレームウィジェット
    frame_top = tk.Frame(root,padx=5,pady=5,relief=tk.RAISED, bd=2)
    frame_top.pack(fill=tk.X,side=tk.TOP)

    #問題範囲指定フレーム
    nums_entry  = tk.Frame (frame_top)
    nums_entry.pack(side=tk.TOP)

    #入力エントリ
    label1 = tk.Label(nums_entry,text="開始番号",font=("MSゴシック", "10", "bold"))
    label1.pack(side=tk.LEFT,pady=10)
    entry1 = tk.Entry(nums_entry)
    entry1.pack(side=tk.LEFT)
    label2 = tk.Label(nums_entry,text="終了番号",font=("MSゴシック", "10", "bold"))
    label2.pack(side=tk.LEFT,pady=10)
    entry2 = tk.Entry(nums_entry)
    entry2.pack(side=tk.LEFT)

    #問題数表示
    quiz_num = pd.read_csv(resourcePath("quiz_list\minhaya_list.csv")).shape[0]
    tk.Label(nums_entry,text="(総問題数："+str(quiz_num)+")",font=("MSゴシック", "10")).pack(anchor=tk.S,pady=10, padx=30)

    #出題モードラジオボタン
    selected_value = tk.IntVar()
    selected_value.set(0)
    sequential = tk.Radiobutton(frame_top,text="順番",variable=selected_value,value=0).pack(anchor=tk.SE)
    randum = tk.Radiobutton(frame_top,text="ランダム",variable=selected_value,value=1).pack(anchor=tk.SE)

    #問題範囲指定フレーム
    start_stop = tk.Frame (frame_top)
    start_stop.pack(side=tk.TOP)
    #出題開始ボタン
    tk.Button(start_stop,text="出題開始",command=start).pack(side=tk.LEFT,padx=10)
    #出題停止ボタン
    tk.Button(start_stop,text="出題停止",command=end).pack(side=tk.LEFT,padx=10)

    root.mainloop()
