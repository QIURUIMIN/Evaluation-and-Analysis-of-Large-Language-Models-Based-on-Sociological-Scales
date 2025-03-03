'''import win32com.client as win32


def read_doc(file_path):
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    doc = word.Documents.Open(file_path)

    text = ""
    for paragraph in doc.Paragraphs:
        text += paragraph.Range.Text + "\n"

    doc.Close()
    word.Quit()

    return text


try:
    doc_text = read_doc("D:/Desktop/MBTI.doc")
    print(doc_text)
except FileNotFoundError:
    print("指定的文件未找到。")
except Exception as e:
    print(f"发生错误: {e}")'''

import pandas as pd

# 读取xlsx文件
data = pd.read_excel('C:/Users/14542/Desktop/MProject/scales/MBTI_Q.xlsx')

# 打印数据
print(data)
