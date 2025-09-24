import os
from tkinter import Tk, filedialog
from pydub import AudioSegment
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from mutagen.id3 import error

def select_folder(title):
    """跳出視窗選擇資料夾"""
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title=title)
    root.destroy()
    return folder_path

def select_file(title, file_types):
    """跳出視窗選擇單個檔案"""
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=title, filetypes=file_types)
    root.destroy()
    return file_path

def merge_audio_files(input_folder, output_folder):
    """合併音檔並輸出合併後的檔案"""
    try:
        # 收集所有 MP3 和 WAV 音檔
        audio_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.mp3', '.wav'))]
        audio_files.sort()

        if not audio_files:
            print("找不到音檔，請確認資料夾內有 MP3 或 WAV 檔案！")
            return None

        # 合併音檔
        combined_audio = AudioSegment.empty()
        for file in audio_files:
            file_path = os.path.join(input_folder, file)
            print(f"正在處理音檔: {file}")
            audio = AudioSegment.from_file(file_path)
            combined_audio += audio  # 音檔依序合併

        # 輸出合併後的音檔
        folder_name = os.path.basename(input_folder)
        output_file_name = f"(FULL){folder_name}.mp3"
        output_file_path = os.path.join(output_folder, output_file_name)
        combined_audio.export(output_file_path, format="mp3")
        print(f"音檔合併完成，輸出至: {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"合併音檔時發生錯誤: {e}")
        return None

def add_front_cover(mp3_file, cover_image_path):
    """將 Front Cover 圖片加入 MP3 檔案"""
    try:
        # 載入 MP3 檔案
        audio = MP3(mp3_file, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass

        # 加入封面圖片
        with open(cover_image_path, "rb") as img:
            audio.tags.add(
                APIC(
                    encoding=3,        # UTF-8
                    mime="image/jpeg", # 圖片格式 (image/jpeg 或 image/png)
                    type=3,            # 3 表示 Front Cover
                    desc="Front Cover",
                    data=img.read()
                )
            )
        audio.save()
        print(f"成功為音檔加入封面圖片: {mp3_file}")

    except Exception as e:
        print(f"添加封面圖片時發生錯誤: {e}")

def main():
    print("請選擇音檔所在的資料夾...")
    input_folder = select_folder("選擇音檔所在的資料夾")
    if not input_folder:
        print("未選擇資料夾，程式結束。")
        return

    print("請選擇輸出資料夾...")
    output_folder = select_folder("選擇輸出資料夾")
    if not output_folder:
        print("未選擇輸出資料夾，程式結束。")
        return

    print("正在合併音檔...")
    merged_file = merge_audio_files(input_folder, output_folder)
    if not merged_file:
        print("音檔合併失敗，程式結束。")
        return

    print("請選擇封面圖片...")
    cover_image = select_file("選擇封面圖片", [("Image Files", "*.jpg *.jpeg *.png")])
    if not cover_image:
        print("未選擇封面圖片，程式結束。")
        return

    print("正在為音檔添加封面圖片...")
    add_front_cover(merged_file, cover_image)

    print("程式執行完成！最終檔案已輸出。")

if __name__ == "__main__":
    main()
