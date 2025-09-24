import os
from tkinter import Tk, filedialog, messagebox
from pydub import AudioSegment
from pydub.utils import which
from mutagen.id3 import ID3, APIC
from mutagen.mp3 import MP3
from mutagen.id3 import error

# ---------- UI helpers ----------
def select_folder(title):
    root = Tk(); root.withdraw()
    p = filedialog.askdirectory(title=title)
    root.destroy()
    return p

def select_file(title, file_types):
    root = Tk(); root.withdraw()
    p = filedialog.askopenfilename(title=title, filetypes=file_types)
    root.destroy()
    return p

def select_exec(title):
    root = Tk(); root.withdraw()
    p = filedialog.askopenfilename(title=title,
                                   filetypes=[("Executable", "*.exe"), ("All files", "*.*")])
    root.destroy()
    return p

# ---------- FFmpeg setup ----------
def ensure_ffmpeg():
    """
    1) 先從 PATH 找 ffmpeg/ffprobe
    2) 找不到就跳窗讓使用者選 ffmpeg.exe，並自動推測同資料夾的 ffprobe.exe
    3) 設定給 pydub
    """
    ffmpeg_path = which("ffmpeg")
    ffprobe_path = which("ffprobe")

    if not ffmpeg_path:
        ffmpeg_path = select_exec("請選擇 ffmpeg.exe（在 FFmpeg 的 bin 資料夾內）")
    if not ffmpeg_path:
        raise RuntimeError("未選擇 ffmpeg.exe")

    if not ffprobe_path:
        # 嘗試用 ffmpeg.exe 的同一路徑推測 ffprobe.exe
        base = os.path.dirname(ffmpeg_path)
        guess = os.path.join(base, "ffprobe.exe")
        ffprobe_path = guess if os.path.exists(guess) else select_exec("請選擇 ffprobe.exe（在 FFmpeg 的 bin 資料夾內）")
    if not ffprobe_path:
        raise RuntimeError("未選擇 ffprobe.exe")

    # 設定給 pydub
    AudioSegment.converter = ffmpeg_path
    AudioSegment.ffprobe = ffprobe_path

    # 也把 ffmpeg 的 bin 夾加進 PATH
    os.environ["PATH"] = base + os.pathsep + os.environ.get("PATH", "")

    print(f"[ffmpeg] 使用路徑：{ffmpeg_path}")
    print(f"[ffprobe] 使用路徑：{ffprobe_path}")

# ---------- Core ----------
def merge_audio_files(input_folder, output_folder):
    try:
        audio_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.mp3', '.wav'))]
        audio_files.sort()
        if not audio_files:
            print("找不到音檔，請確認資料夾內有 MP3 或 WAV 檔案！")
            return None

        combined_audio = AudioSegment.empty()
        for file in audio_files:
            file_path = os.path.join(input_folder, file)
            print(f"正在處理音檔: {file}")
            audio = AudioSegment.from_file(file_path)  # 這行需要 ffmpeg 已設定
            combined_audio += audio

        folder_name = os.path.basename(input_folder.rstrip("\\/"))
        output_file_name = f"(FULL){folder_name}.mp3"
        output_file_path = os.path.join(output_folder, output_file_name)
        combined_audio.export(output_file_path, format="mp3")  # 這行也會呼叫 ffmpeg
        print(f"音檔合併完成，輸出至: {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"合併音檔時發生錯誤: {e}")
        return None

def add_front_cover(mp3_file, cover_image_path):
    try:
        ext = os.path.splitext(cover_image_path)[1].lower()
        mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"

        audio = MP3(mp3_file, ID3=ID3)
        try:
            audio.add_tags()
        except error:
            pass

        # 清除既有 APIC，避免播放器只讀第一張
        if audio.tags is not None:
            for k in list(audio.tags.keys()):
                if k.startswith("APIC"):
                    del audio.tags[k]

        with open(cover_image_path, "rb") as img:
            audio.tags.add(APIC(
                encoding=3, mime=mime, type=3, desc="Front Cover", data=img.read()
            ))
        audio.save(v2_version=3)  # ID3v2.3 相容性佳
        print(f"成功為音檔加入封面圖片: {mp3_file}")

    except Exception as e:
        print(f"添加封面圖片時發生錯誤: {e}")

def main():
    try:
        # *** 一開始就先設定 ffmpeg/ffprobe，避免 WinError 2 ***
        ensure_ffmpeg()
    except Exception as e:
        messagebox.showerror("錯誤", f"FFmpeg 設定失敗：{e}")
        return

    print("請選擇音檔所在的資料夾...")
    input_folder = select_folder("選擇音檔所在的資料夾")
    if not input_folder:
        print("未選擇資料夾，程式結束。"); return

    print("請選擇輸出資料夾...")
    output_folder = select_folder("選擇輸出資料夾")
    if not output_folder:
        print("未選擇輸出資料夾，程式結束。"); return

    print("正在合併音檔...")
    merged_file = merge_audio_files(input_folder, output_folder)
    if not merged_file:
        print("音檔合併失敗，程式結束。"); return

    print("請選擇封面圖片...")
    cover_image = select_file("選擇封面圖片", [("Image Files", "*.jpg *.jpeg *.png")])
    if not cover_image:
        print("未選擇封面圖片，程式結束。"); return

    print("正在為音檔添加封面圖片...")
    add_front_cover(merged_file, cover_image)
    print("程式執行完成！最終檔案已輸出。")

if __name__ == "__main__":
    main()
