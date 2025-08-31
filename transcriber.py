import os
import whisper

# Paths
video_folder = r" put your video/audio folder path here like C:\ccvidoes"
output_folder = r" put path of folder where you want to save the transcript path here like C:\ccvidoes\caption"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load Whisper model (small = faster + accurate)
print("🔄 Loading Whisper model... Please wait...")
model = whisper.load_model("small")

# Supported video formats
video_extensions = [".mp4", ".mkv", ".avi", ".mov" ,".mp3"]

# Scan for videos
videos = [f for f in os.listdir(video_folder) if os.path.splitext(f)[1].lower() in video_extensions]

if not videos:
    print("⚠️ No videos found in the folder!")
else:
    print(f"🎥 Found {len(videos)} videos. Starting transcription...\n")

    for video in videos:
        video_path = os.path.join(video_folder, video)
        base_name = os.path.splitext(video)[0]
        txt_filename = os.path.join(output_folder, f"{base_name}.txt")

        # Skip if transcript already exists
        if os.path.exists(txt_filename):
            print(f"✅ Skipping '{video}' → Transcript already exists.")
            continue

        # Ask user what to do **before starting transcription**
        while True:
            choice = input(
                f"\n▶ Video: {video}\n"
                "Press [Enter] to continue, [S] to skip, [P] to pause: "
            ).strip().lower()

            if choice == "s":
                print(f"⏩ Skipping '{video}'...")
                break
            elif choice == "p":
                input("⏸ Paused. Press Enter to resume...")
                # After pause, show the prompt again before continuing
                continue
            elif choice == "":
                # Continue transcription
                print(f"⏳ Transcribing: {video} ...")
                result = model.transcribe(video_path)

                # Save transcript with same video name
                with open(txt_filename, "w", encoding="utf-8") as f:
                    f.write(result["text"])

                print(f"💾 Saved transcript: {txt_filename}")
                break
            else:
                print("⚠️ Invalid option! Please press Enter, S, or P.")

print("\n🎉 Done! All transcripts saved successfully in:")
print(output_folder)
