# SubtitleMask

一个适用于 Windows 系统的字幕遮挡工具 — 在屏幕底部生成可拖拽的黑色遮罩条，用于遮挡视频中的字幕。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 🖱️ **拖拽移动** | 左键按住遮挡条中间区域拖动，可自由移动位置 |
| 📐 **边缘缩放** | 拖拽遮挡条的上下左右边缘，可调整高度和宽度 |
| 👁️ **临时透明** | 按住左键拖动时遮挡条自动变半透明，松开恢复不透明 |
| ⌨️ **Z 键透明** | 按住 `Z` 键等同于按住左键的效果，遮挡条变半透明，松开恢复 |
| 🚫 **屏幕边界限制** | 遮挡条的左右两侧不会移出屏幕，确保始终在可见范围内 |
| 📌 **始终置顶** | 遮挡条始终位于所有窗口之上（包括任务栏上方） |
| 🎯 **DPI 感知** | 自动适配高 DPI 显示器（Windows） |
| ❌ **双击右键关闭** | 快速双击鼠标右键即可退出程序 |

## 🎮 快捷键与操作

| 操作 | 效果 |
|------|------|
| **鼠标左键拖拽**（遮挡条中间） | 移动遮挡条位置 |
| **鼠标左键拖拽**（遮挡条边缘） | 调整遮挡条大小 |
| **按住鼠标左键** | 遮挡条变半透明（松开恢复） |
| **按住 `Z` 键** | 遮挡条变半透明（松开恢复） |
| **双击鼠标右键** | 关闭程序 |

## 📥 下载

前往 [Releases 页面](https://github.com/Micheal-Reber/subtitlemask/releases) 下载最新的 `SubtitleMask.exe`，无需安装 Python 即可直接运行。

## 🔧 从源码运行

### 环境要求
- Python 3.8+
- Windows 操作系统

### 运行
```bash
git clone https://github.com/Micheal-Reber/subtitlemask.git
cd subtitlemask
python mask.py
```

### 自行打包为 exe
```bash
pip install pyinstaller
pyinstaller --onefile --windowed mask.py
```
打包后的 exe 文件位于 `dist/` 目录下。

## 📁 项目结构

```
SubtitleMask/
├── mask.py          # 主程序
├── .gitignore       # Git 忽略规则
└── README.md        # 项目说明
```

## ⚙️ 自定义配置

在 `mask.py` 顶部可修改以下参数：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MASK_COLOR` | `#000000` | 遮挡条颜色 |
| `MASK_ALPHA` | `1.0` | 遮挡条不透明度（0.0 ~ 1.0） |
| `DRAG_ALPHA` | `0.35` | 拖拽/按 Z 键时的透明度 |
| `DEFAULT_HEIGHT` | `110` | 遮挡条默认高度（像素） |
| `BOTTOM_GAP` | `0` | 遮挡条与屏幕底部的间距（像素） |

## 📄 许可证

MIT License
