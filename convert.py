import os
import subprocess

# --- 配置区 ---

# 1. 设置 FFmpeg.exe 的完整路径
# 注意：在 Python 中，路径中的反斜杠 \ 最好使用正斜杠 / 或者双反斜杠 \\
FFMPEG_PATH = "C:/Users/Lenovo/Downloads/ffmpeg-8.0.1-essentials_build/ffmpeg-8.0.1-essentials_build/bin/ffmpeg.exe"

# 2. 设置存放所有视频的根文件夹路径
VIDEOS_ROOT = "./assets/artimuse/videos"


# --- 脚本执行区 ---

def convert_videos():
    """
    递归查找并转换指定目录下的所有 .mp4 文件。
    """
    # 检查 FFmpeg 是否存在
    if not os.path.exists(FFMPEG_PATH):
        print(f"错误: 在指定路径下找不到 ffmpeg.exe: {FFMPEG_PATH}")
        print("请检查路径是否正确。")
        return

    # 检查视频根文件夹是否存在
    if not os.path.isdir(VIDEOS_ROOT):
        print(f"错误: 找不到视频根文件夹: {VIDEOS_ROOT}")
        print("请检查路径是否正确。")
        return

    print("开始查找并转换视频...")
    print("--------------------------------------------------------")

    # 使用 os.walk 递归遍历所有子文件夹
    for dirpath, _, filenames in os.walk(VIDEOS_ROOT):
        for filename in filenames:
            # 检查文件是否是 .mp4 并且不是已经转换过的文件
            if filename.endswith(".mp4") and not filename.endswith("-h264.mp4"):

                input_file = os.path.join(dirpath, filename)

                # 构建输出文件名
                base_name, ext = os.path.splitext(filename)
                output_file = os.path.join(dirpath, f"{base_name}-h264.mp4")

                print(f"正在转换: {input_file}")

                # 构建 FFmpeg 命令
                command = [
                    FFMPEG_PATH,
                    '-y',  # 自动覆盖已存在的文件
                    '-i', input_file,
                    '-c:v', 'libx264',
                    '-crf', '23',
                    '-preset', 'fast',
                    output_file
                ]

                # 执行命令
                try:
                    # 使用 subprocess.run 来执行命令，并捕获输出
                    result = subprocess.run(
                        command,
                        check=True,  # 如果命令返回非零退出码（错误），则抛出异常
                        capture_output=True,  # 捕获 stdout 和 stderr
                        text=True  # 将 stdout 和 stderr 解码为文本
                    )
                    print(f"成功 -> {output_file}")
                except subprocess.CalledProcessError as e:
                    print(f"失败 X  转换文件时发生错误: {input_file}")
                    print(f"FFmpeg 错误信息:\n{e.stderr}")
                except FileNotFoundError:
                    print(f"错误: 无法执行 ffmpeg。请确保 FFMPEG_PATH 配置正确并且 ffmpeg 已经安装。")
                    return  # 如果 ffmpeg 找不到，就没必要继续了

                print("")  # 输出一个空行用于分隔

    print("--------------------------------------------------------")
    print("所有视频转换完成！")


if __name__ == "__main__":
    convert_videos()