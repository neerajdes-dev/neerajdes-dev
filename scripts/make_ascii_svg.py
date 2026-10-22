"""Generate one-shot animated ASCII SVG from a prepared grayscale portrait."""
import argparse
from html import escape
from pathlib import Path
from PIL import Image, ImageOps

RAMP = " .`:-=+*cs#%@"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("source-prepped.png"))
    parser.add_argument("--output", type=Path, default=Path("assets/portrait-ascii.svg"))
    parser.add_argument("--columns", type=int, default=94)
    args = parser.parse_args()
    if not args.input.exists():
        parser.error(f"Cannot find {args.input}; run prep_photo.py first.")
    source = Image.open(args.input).convert("L")
    columns = max(20, min(160, args.columns))
    rows = max(15, round(source.height / source.width * columns * .52))
    image = ImageOps.autocontrast(source).resize((columns, rows), Image.Resampling.LANCZOS)
    chars = []
    for y in range(rows):
        row = "".join(RAMP[min(len(RAMP)-1, (255-image.getpixel((x,y)))*len(RAMP)//256)] for x in range(columns))
        chars.append(row)
    char_width, row_height = 9, 15
    width, height = columns*char_width+36, rows*row_height+42
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII portrait of Neeraj Desai">',
             '<rect width="100%" height="100%" rx="16" fill="#0d1117"/>',
             '<style>text{font-family:Consolas,monospace;font-size:15px;fill:#d6e8dc;white-space:pre}@media(prefers-reduced-motion:reduce){.reveal{display:none}.full{display:inline}}</style>']
    for y, row in enumerate(chars):
        yy=26+y*row_height
        delay=f"{y*0.037:.3f}s"
        name=f"c{y}"
        parts += [f'<defs><clipPath id="{name}"><rect x="17" y="{yy-13}" width="0" height="17"><animate attributeName="width" from="0" to="{columns*char_width}" begin="{delay}" dur="0.6s" fill="freeze"/></rect></clipPath></defs>',
                  f'<text x="17" y="{yy}" xml:space="preserve" clip-path="url(#{name})">{escape(row)}</text>']
    parts += ['</svg>']
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text("\n".join(parts), encoding="utf-8")
    print(f"Saved {args.output} ({columns} columns x {rows} rows)")

if __name__=="__main__":
    main()
