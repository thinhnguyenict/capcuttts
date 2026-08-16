"""Tạo tuần tự các text clip trong CapCut từ một tệp văn bản.

Script được thiết kế cho CapCut Desktop trên Windows.  Chạy ``--dry-run`` để
kiểm tra cách chia đoạn mà không cần cài các thư viện automation.
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path
from typing import Callable, Sequence


SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?…])\s+")


def split_text(text: str, max_len: int = 350) -> list[str]:
    """Chia văn bản thành các đoạn không dài quá ``max_len`` ký tự.

    Ưu tiên ranh giới câu, sau đó đến khoảng trắng. Từ dài hơn giới hạn sẽ
    được cắt cứng để mọi đoạn luôn thỏa giới hạn.
    """
    if max_len < 1:
        raise ValueError("max_len phải lớn hơn 0")

    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []

    blocks: list[str] = []
    current = ""

    def append_piece(piece: str) -> None:
        nonlocal current
        piece = piece.strip()
        while piece:
            separator = " " if current else ""
            room = max_len - len(current) - len(separator)
            if len(piece) <= room:
                current += separator + piece
                return
            if current:
                blocks.append(current)
                current = ""
                continue

            cut = piece.rfind(" ", 0, max_len + 1)
            if cut <= 0:
                cut = max_len
            blocks.append(piece[:cut].strip())
            piece = piece[cut:].strip()

    for sentence in SENTENCE_BOUNDARY.split(normalized):
        append_piece(sentence)
    if current:
        blocks.append(current)
    return blocks


def run_automation(
    blocks: Sequence[str],
    start_delay: float,
    block_delay: float,
    start_at: int = 1,
    *,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Kích hoạt CapCut rồi paste từng đoạn vào ô text đang được chọn."""
    try:
        import pyautogui
        import pygetwindow as gw
        import pyperclip
    except ImportError as exc:
        raise RuntimeError(
            "Thiếu thư viện automation. Chạy: "
            "pip install pyautogui pyperclip pygetwindow"
        ) from exc

    windows = gw.getWindowsWithTitle("CapCut")
    if not windows:
        raise RuntimeError("Không tìm thấy cửa sổ CapCut")

    windows[0].activate()
    print(f"🚀 Bắt đầu sau {start_delay:g} giây...", flush=True)
    sleep(start_delay)

    total = len(blocks)
    for index in range(start_at - 1, total):
        pyperclip.copy(blocks[index])
        pyautogui.hotkey("ctrl", "v")
        sleep(0.3)
        pyautogui.press("enter")
        print(f"✅ Đã paste đoạn {index + 1}/{total}", flush=True)
        sleep(block_delay)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tự động tạo text clip CapCut từ truyện trong tệp TXT."
    )
    parser.add_argument("file", nargs="?", default="truyen.txt", type=Path)
    parser.add_argument("--max-len", type=int, default=350)
    parser.add_argument("--delay", type=float, default=1.5, help="Nghỉ giữa các đoạn")
    parser.add_argument("--start-delay", type=float, default=5.0)
    parser.add_argument(
        "--start-at", type=int, default=1, help="Tiếp tục từ đoạn thứ N (bắt đầu từ 1)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Chỉ chia và in đoạn, không điều khiển CapCut"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.delay < 0 or args.start_delay < 0:
        print("❌ Thời gian chờ không được âm", file=sys.stderr)
        return 2
    try:
        text = args.file.read_text(encoding="utf-8-sig")
        blocks = split_text(text, args.max_len)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"❌ Không thể đọc/chia tệp: {exc}", file=sys.stderr)
        return 2

    if not blocks:
        print("❌ Tệp truyện không có nội dung", file=sys.stderr)
        return 2
    if not 1 <= args.start_at <= len(blocks):
        print(f"❌ --start-at phải từ 1 đến {len(blocks)}", file=sys.stderr)
        return 2

    print(f"✅ Tổng số đoạn: {len(blocks)}")
    if args.dry_run:
        for index, block in enumerate(blocks, 1):
            print(f"[{index}/{len(blocks)}] ({len(block)} ký tự) {block}")
        return 0

    try:
        run_automation(blocks, args.start_delay, args.delay, args.start_at)
    except RuntimeError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n⏹ Đã dừng. Dùng --start-at N để tiếp tục.", file=sys.stderr)
        return 130

    print("🎉 HOÀN TẤT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
