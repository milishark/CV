#!/usr/bin/env python3
"""
重命名帧文件夹中的所有图片文件为纯数字序列（如 000001.jpg, 000002.jpg ...）
解决 SAM2 加载帧时遇到非数字文件名（如 frame_11.20s.jpg）的 ValueError。
"""

import os
import sys
import argparse
from pathlib import Path

SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}

def rename_frames_to_digits(folder_path: str, dry_run: bool = False, ext: str = None):
    """
    将文件夹内的所有图片文件按自然顺序重命名为数字序列。

    Args:
        folder_path: 图片所在文件夹路径
        dry_run: 若为 True，仅打印将要执行的操作，不实际重命名
        ext: 可选，只重命名指定扩展名的文件（如 '.jpg'），不填则处理所有支持的图片格式
    """
    folder = Path(folder_path)
    if not folder.exists() or not folder.is_dir():
        print(f"❌ 错误：目录不存在或不是文件夹: {folder_path}")
        return

    # 收集所有图片文件
    if ext:
        if not ext.startswith('.'):
            ext = '.' + ext
        files = list(folder.glob(f"*{ext}"))
    else:
        files = []
        for e in SUPPORTED_EXTS:
            files.extend(folder.glob(f"*{e}"))
    
    if not files:
        print(f"⚠️ 警告：在 {folder_path} 中没有找到任何图片文件。")
        return

    # 按原始文件名排序（确保顺序与视频帧一致）
    files.sort(key=lambda f: f.name)

    print(f"📁 找到 {len(files)} 个图片文件，将按当前排序重命名为数字序列。")
    if dry_run:
        print("🔍 [试运行模式] 不会实际重命名文件")

    # 计算数字位数（至少4位，自动根据文件数量决定）
    digits = max(5, len(str(len(files))))
    for idx, f in enumerate(files, start=1):
        new_name = f"{idx:0{digits}d}{f.suffix}"
        new_path = f.parent / new_name
        if dry_run:
            print(f"  [试运行] {f.name} -> {new_name}")
        else:
            # 如果新文件名已经存在且不是当前文件，先处理冲突（极少发生）
            if new_path.exists() and new_path != f:
                print(f"⚠️ 冲突：{new_name} 已存在，跳过 {f.name}")
                continue
            f.rename(new_path)
            print(f"  ✅ {f.name} -> {new_name}")

    if not dry_run:
        print(f"🎉 重命名完成！所有文件已保存为纯数字名称，位于 {folder}")
    else:
        print("🏁 试运行结束，未实际修改任何文件。")

def main():
    parser = argparse.ArgumentParser(description="将图片文件夹中的文件重命名为纯数字序列")
    parser.add_argument("folder", type=str, help="帧文件夹路径")
    parser.add_argument("--dry-run", action="store_true", help="试运行，只显示将要进行的更改，不实际重命名")
    parser.add_argument("--ext", type=str, default=None, help="指定扩展名（如 jpg），不指定则处理所有支持的图片格式")
    args = parser.parse_args()

    rename_frames_to_digits(args.folder, dry_run=args.dry_run, ext=args.ext)

if __name__ == "__main__":
    main()