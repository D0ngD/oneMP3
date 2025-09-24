# oneMP3 — One-Click Audio Merger
Merge all `.mp3` / `.wav` files in a folder into a single MP3, sorted by filename.  

---

## Features
- Select an audio folder → outputs `(FULL)FolderName.mp3`  
- Optional cover image (JPG/PNG) → embedded into ID3 Front Cover  
- Saves tags as **ID3v2.3** (better compatibility with Windows / car players)  

---

## Download
Go to **[Releases](../../releases)** and grab the latest `oneMP3.exe`.  

---

## Usage

### Version 1.0
1. Run `oneMP3_1.0.exe`  
2. Choose the **audio folder** → choose the **output folder**  

> Requires **ffmpeg** installed and added to PATH.  

---

### Version 2.0 (Cover Image Support)
1. Run `oneMP3_2.0.exe`  
2. Choose the **audio folder** → choose the **output folder**  
3. Choose the **cover image (JPG/PNG)** → done  

---

### Version 3.0 (Beginner-Friendly, Manual ffmpeg Path)
1. Download ffmpeg from: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)  
2. Run `oneMP3.exe`  
3. Choose the **ffmpeg.exe folder**  
4. Choose the **audio folder** → choose the **output folder**  
5. Choose the **cover image (JPG/PNG)** → done  

---

## FAQ
- **Windows SmartScreen warning**: click *More info* → *Run anyway*.  
- **Cover not visible in File Explorer preview**: test with **VLC** or **Mp3tag**; sometimes Explorer requires a refresh or cache clear.  

---

## Version Comparison

| Version | Features |
|---------|----------|
| **1.0** | Basic merge (requires ffmpeg in PATH) |
| **2.0** | Merge + custom cover image |
| **3.0** | Merge + custom cover + manual ffmpeg path (no PATH setup needed) |

---

## License
- Free for personal use  
- Redistribution allowed (must include source GitHub link)  
- Commercial use prohibited  
