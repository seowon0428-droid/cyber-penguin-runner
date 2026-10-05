"""원본 PNG 누끼 처리 및 모션 시트 분할."""
from PIL import Image
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def remove_white(im: Image.Image, threshold: int = 248) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= threshold and g >= threshold and b >= threshold:
                px[x, y] = (r, g, b, 0)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
    return im


def save_front(src_name: str, out_name: str) -> None:
    path = os.path.join(BASE, src_name)
    if not os.path.isfile(path):
        print("skip missing", src_name)
        return
    im = remove_white(Image.open(path))
    im.save(os.path.join(BASE, out_name), "PNG")
    print(out_name, im.size)


def split_motion(src_name: str, prefix: str) -> None:
    path = os.path.join(BASE, src_name)
    if not os.path.isfile(path):
        print("skip missing", src_name)
        return
    sheet = Image.open(path)
    w, h = sheet.size
    cw, ch = w // 2, h // 2
    cells = {
        "run": (0, 0),
        "turn_r": (cw, 0),
        "heal": (0, ch),
        "hit": (cw, ch),
    }
    for key, (x, y) in cells.items():
        cell = sheet.crop((x, y, x + cw, y + ch))
        cell = remove_white(cell)
        out = os.path.join(BASE, f"{prefix}_{key}.png")
        cell.save(out, "PNG")
        print(out, cell.size)


def main() -> None:
    save_front("삐야-정면.png", "삐야-정면.png")
    save_front("오르-정면.png", "오르-정면.png")
    split_motion("삐야-모션.png", "삐야")
    split_motion("오르-모션.png", "오르")


if __name__ == "__main__":
    main()
