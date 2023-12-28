from gooey import Gooey, GooeyParser
import subprocess
from faster_whisper import WhisperModel
import datetime  # 用於計算日期和時間
import os

@Gooey(
    program_name="whisper GUI",
    program_description="whisper 語音轉文字",
)
def main():
    parser = GooeyParser()
    converter = parser.add_argument_group("Video Converter")
    converter.add_argument(
        "-i",
        "--input_file", 
        required=True,
        help="File to be converted",
        widget="FileChooser",
        gooey_options=dict(wildcard="Video files (*.mp4, *.mkv,*.mp3,*.m4a,*.wav)|*.mp4;*.mkv;*.mp3;*.m4a;*.wav")
    )
    languages=["自動判斷","zh","en"]
    converter.add_argument(
        "-l",
        "--language",
        required=True,
        choices=languages,
        default=languages[0],
        metavar="Language",
        help=f"選擇語言: {', '.join(languages)}"
        )
    models = ["large-v3", "tiny","base","small","medium","large","large-v2"]
    converter.add_argument(
        "-m",
        "--model",
        required=True,
        choices=models,
        default=models[0],
        metavar="Model",
        help=f"選擇使用的模型: {', '.join(models)}"
    )
    if_cuda=["是","否"]
    converter.add_argument(
        "-c",
        "--cuda",
        required=True,
        choices=if_cuda,
        default=if_cuda[0],
        metavar="cuda",
        help=f"是否使用cuda顯卡: {', '.join(if_cuda)}"
    )
    converter.add_argument(
        "-o",
        "--output_folder",
        required=False,
        metavar="Output Folder",
        help="指定輸出資料夾",
        widget="DirChooser"
    )
    args = parser.parse_args()
    fast_convert(args.input_file, args.language, args.model, args.output_folder,args.cuda)

def fast_convert(infile, language, model_type, output_folder,cuda):
    start_times = datetime.datetime.now()  # 記錄程式開始執行時間
    print(start_times)
    if cuda=="是":
        model = WhisperModel(model_type, device="cuda", compute_type="float16")
    else:
        model = WhisperModel(model_type, device="cpu")
    if language=="自動判斷":
        segments, info = model.transcribe(infile, beam_size=5,vad_filter=True)
        print("偵測到的語言為 '%s'，概率為 %f" % (info.language, info.language_probability))
    else:
        segments, info = model.transcribe(infile, beam_size=5, language=language,vad_filter=True)
        print(f"選擇使用{language}來轉譯")
    # 這些代碼行創建並使用UTF-8編碼以寫模式打開三個不同的文件
    
    if not output_folder:
        script_dir = os.path.dirname(os.path.abspath(__file__))  # 取得程式檔案所在目錄
        output_folder = os.path.join(script_dir, 'out')          # 加入 'out' 子目錄
        os.makedirs(output_folder, exist_ok=True)
    # output_folder = r"G:\python_data\TEST_whisper\out"
    print(output_folder)
    subtitle_file = open(os.path.join(output_folder, "subtitle.srt"), "w", encoding="utf-8") # 這個文件是SRT格式的字幕
    text_file = open(os.path.join(output_folder, "text.txt"), "w", encoding="utf-8") # 這個文件是純文本文件
    tsv_file = open(os.path.join(output_folder, "data.tsv"), "w", encoding="utf-8") # 這個文件是TAB分隔的值


    # 以下代碼行在TSV文件中編寫標題列，包括開始時間、結束時間和文本列。
    tsv_file.write("start_time\tend_time\ttext\n")
    counter = 1
# 循環遍歷從音頻轉錄生成的所有片段，並將它們寫入三個文件之一。
    for segment in segments:
        start_time = datetime.timedelta(seconds=segment.start)
        end_time = datetime.timedelta(seconds=segment.end)
        subtitle_text = f"{counter}\n{start_time} --> {end_time}\n{segment.text}\n\n"
        subtitle_file.write(subtitle_text)
        text_file.write(segment.text + "\n")
        tsv_file.write(f"{start_time}\t{end_time}\t{segment.text}\n")
        counter += 1
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    # 關閉打開的文件
    subtitle_file.close()
    text_file.close()
    tsv_file.close()
    end_times = datetime.datetime.now()  # 記錄程式結束執行時間
    print(end_times)

    # elapsed_time = end_times - start_times

    seconds = (end_times - start_times).seconds
    minutes = seconds // 60
    seconds = seconds-(minutes*60)
    print("程式執行所花費的時間： %d 分 %d 秒" % (minutes, seconds))  # 輸出總執行時間 

if __name__ == '__main__':
    main()