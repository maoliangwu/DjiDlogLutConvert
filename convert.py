import os
import glob
import argparse
import ffmpeg

# ==========================================================
# 【配置区】
# ==========================================================
INPUT_DIR = "input"   # 已经为你改成了小写的 input
OUTPUT_DIR = "output"
# ==========================================================


def parse_args():
    parser = argparse.ArgumentParser(
        description="批量为 input 目录中的视频应用 3D LUT。"
    )
    parser.add_argument(
        "--lut",
        required=True,
        metavar="FILE",
        help="要使用的 .cube LUT 文件路径（必填）",
    )
    return parser.parse_args()

def apply_lut_to_video(input_path, output_path, lut_path):
    if os.path.exists(output_path):
        print(f"\n[跳过] 文件已处理过: {os.path.basename(input_path)}")
        return

    print(f"\n▶ 正在处理视频: {input_path}")
    abs_lut_path = os.path.abspath(lut_path).replace('\\', '/')
    
    try:
        stream = ffmpeg.input(input_path)
        video_stream = stream.video.filter('lut3d', abs_lut_path)
        audio_stream = stream.audio
        
        out = ffmpeg.output(
            video_stream, 
            audio_stream, 
            output_path, 
            vcodec='libx264', 
            crf=18, 
            preset='fast', 
            acodec='copy'
        )
        out.run(capture_stdout=True, capture_stderr=True)
        print(f"  ✅ 渲染成功！已保存至: {output_path}")
        
    except ffmpeg.Error as e:
        print(f"  ❌ 处理失败: {os.path.basename(input_path)}")
        print(e.stderr.decode('utf8', errors='ignore'))

if __name__ == "__main__":
    args = parse_args()
    lut_file = os.path.abspath(args.lut)

    print("=== 🚀 视频批量 LUT 渲染脚本已启动 ===")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(INPUT_DIR):
        print(f"❌ 错误: 未找到输入目录 '{INPUT_DIR}'。")
        exit(1)

    if not os.path.isfile(lut_file):
        print(f"❌ 错误: 找不到 LUT 文件 '{args.lut}'。")
        exit(1)

    extensions = ("*.mp4", "*.MP4", "*.mov", "*.MOV")
    video_files = []
    for ext in extensions:
        video_files.extend(glob.glob(os.path.join(INPUT_DIR, ext)))

    if not video_files:
        print(f"⚠️ 提示: 在 '{INPUT_DIR}' 目录下没有找到任何视频文件，请确认视频是否已放进去。")
    else:
        print(f"📦 共找到 {len(video_files)} 个视频，开始增量处理...")
        for video_path in video_files:
            filename = os.path.basename(video_path)
            out_path = os.path.join(OUTPUT_DIR, filename)
            apply_lut_to_video(video_path, out_path, lut_file)
            
        print("\n🎉 所有任务已检查/处理完毕！")
