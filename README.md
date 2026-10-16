# 视频 LUT 批量转换工具

这个工具会批量读取 `input` 目录中的视频，应用指定的 3D LUT（`.cube`），并把处理结果保存到 `output` 目录。

当前脚本支持的视频扩展名：`.mp4`、`.MP4`、`.mov`、`.MOV`。

## 一、准备项目文件

请保持下面的目录结构（文件名可以按需替换，但运行命令中的路径要对应）：

```text
video_convert/
├── convert.py
├── DJI OSMO Action 5 Pro D-Log M to Rec.709 V1.cube
├── input/          # 放待处理的视频
└── output/         # 处理结果自动生成到这里
```

建议在项目目录中打开终端，后续命令都在这个目录执行。也可以先切换目录：

```text
cd 项目目录路径
```

## 二、Windows 配置

### 1. 安装 Python

从 <https://www.python.org/downloads/windows/> 安装 Python 3.10 或更高版本。

安装器第一页务必勾选 **Add Python.exe to PATH**，然后完成安装。打开 PowerShell 验证：

```powershell
python --version
```

如果 `python` 不可用，也可以尝试：

```powershell
py --version
```

### 2. 安装 FFmpeg

可以使用 `winget`：

```powershell
winget install Gyan.FFmpeg.Shared
```

安装完成后重新打开 PowerShell，验证：

```powershell
ffmpeg -version
```

如果提示找不到命令，需要把 FFmpeg 的 `bin` 目录加入系统 `Path`，例如 `C:\ffmpeg\bin`，再重新打开终端。

### 3. 创建虚拟环境并安装 Python 依赖

在项目目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install ffmpeg-python
```

如果 PowerShell 禁止执行激活脚本，可执行一次下面的命令后再激活：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 三、macOS 配置

### 1. 安装 Python 和 FFmpeg

先安装 Homebrew（已安装可跳过）：<https://brew.sh/>。然后在终端执行：

```bash
brew install python ffmpeg
```

验证安装：

```bash
python3 --version
ffmpeg -version
```

### 2. 创建虚拟环境并安装 Python 依赖

在项目目录执行：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ffmpeg-python
```

## 四、运行

1. 把要处理的视频复制到 `input` 目录。
2. 确认 `.cube` LUT 文件存在。
3. 在项目根目录、并且虚拟环境已激活的情况下运行。

macOS：

```bash
python convert.py --lut "DJI OSMO Action 5 Pro D-Log M to Rec.709 V1.cube"
```

Windows PowerShell：

```powershell
python convert.py --lut ".\DJI OSMO Action 5 Pro D-Log M to Rec.709 V1.cube"
```

处理完成后，结果会出现在 `output` 目录。脚本使用 H.264 编码（`libx264`），保留原视频音频；如果 `output` 中已有同名文件，该文件会被跳过，不会覆盖。

## 五、再次运行和退出环境

每次打开新的终端窗口后，先进入项目目录并激活虚拟环境：

macOS：

```bash
cd 项目目录路径
source .venv/bin/activate
```

Windows PowerShell：

```powershell
cd 项目目录路径
.\.venv\Scripts\Activate.ps1
```

处理新的素材前，把视频放进 `input` 即可；如果要重新处理某个文件，需要先删除 `output` 中对应的同名结果。

处理完后可以退出虚拟环境：

```text
deactivate
```

## 六、常见问题

### `No module named 'ffmpeg'`

说明 Python 依赖没有安装到当前环境。确认虚拟环境已激活，然后执行：

```text
python -m pip install ffmpeg-python
```

### `ffmpeg is not recognized` 或 `No such file or directory: ffmpeg`

说明 FFmpeg 未安装，或其 `bin` 目录没有加入 `Path`。重新安装 FFmpeg 并打开一个新的终端窗口，再执行 `ffmpeg -version` 验证。

### 找不到视频或提示没有找到视频

请确认视频直接放在项目下的 `input` 目录中，而不是放在更深的子目录；同时检查扩展名是否为 `.mp4` 或 `.mov`。

### LUT 文件路径包含空格

运行命令时用双引号包住路径，例如：

```text
python convert.py --lut "我的 LUT 文件.cube"
```

### 处理失败或画面异常

确认 LUT 与素材的色彩空间匹配（本项目附带的 LUT 是 DJI OSMO Action 5 Pro D-Log M 到 Rec.709），并查看终端中脚本输出的 FFmpeg 错误信息。
