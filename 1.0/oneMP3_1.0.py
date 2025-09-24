import os
from tkinter import Tk, filedialog
from pydub import AudioSegment

def select_folder(title):
    """彈出視窗選擇資料夾"""
    root = Tk()
    root.withdraw()  # 隱藏主視窗
    folder_path = filedialog.askdirectory(title=title)
    root.destroy()  # 關閉主視窗
    return folder_path

def merge_audio_files(input_folder, output_folder):
    """合併資料夾內的音檔並輸出到指定位置"""
    try:
        # 獲取音檔列表，過濾出 mp3 和 wav 檔案
        audio_files = [file for file in os.listdir(input_folder) if file.lower().endswith(('.mp3', '.wav'))]
        audio_files.sort()  # 按照名稱排序

        if not audio_files:
            print("資料夾內沒有可用的音檔！")
            return

        # 建立合併的音檔
        combined_audio = AudioSegment.empty()
        for audio_file in audio_files:
            file_path = os.path.join(input_folder, audio_file)
            print(f"正在處理：{file_path}")
            audio = AudioSegment.from_file(file_path)
            combined_audio += audio  # 合併音檔

        # 確定輸出檔名和路徑
        folder_name = os.path.basename(input_folder)
        output_file_name = f"(FULL){folder_name}.mp3"
        output_file_path = os.path.join(output_folder, output_file_name)

        # 將合併後的音檔匯出
        combined_audio.export(output_file_path, format="mp3")
        print(f"合併完成，輸出檔案：{output_file_path}")

    except Exception as e:
        print(f"處理過程中發生錯誤：{e}")

if __name__ == "__main__":
    print("選擇包含音檔的資料夾...")
    input_folder = select_folder("選擇包含音檔的資料夾")
    if not input_folder:
        print("未選擇資料夾，程式結束。")
        exit()

    print("選擇輸出資料夾...")
    output_folder = select_folder("選擇輸出資料夾")
    if not output_folder:
        print("未選擇輸出資料夾，程式結束。")
        exit()

    merge_audio_files(input_folder, output_folder)
