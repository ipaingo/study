# -*- coding: utf-8 -*-
import sys
from pptx import Presentation
from pptx.util import Emu

path = sys.argv[1]
prs = Presentation(path)
print(f"Slide size: {prs.slide_width} x {prs.slide_height} ({Emu(prs.slide_width).inches:.2f}in x {Emu(prs.slide_height).inches:.2f}in)")
print(f"Slides: {len(prs.slides)}")
print(f"Layouts in master: {len(prs.slide_masters)} master(s)")
for i, slide in enumerate(prs.slides, 1):
    print(f"\n===== СЛАЙД {i} (layout: {slide.slide_layout.name}) =====")
    for shape in slide.shapes:
        ph = ""
        if shape.is_placeholder:
            ph = f" [PH idx={shape.placeholder_format.idx} type={shape.placeholder_format.type}]"
        info = f"  shape: {shape.shape_type}, name={shape.name!r}{ph}"
        try:
            info += f", pos=({Emu(shape.left).inches:.2f},{Emu(shape.top).inches:.2f}), size=({Emu(shape.width).inches:.2f}x{Emu(shape.height).inches:.2f})"
        except Exception:
            pass
        print(info)
        if shape.has_text_frame and shape.text_frame.text.strip():
            for p in shape.text_frame.paragraphs:
                txt = "".join(r.text for r in p.runs)
                if txt.strip():
                    print(f"    > {txt}")
        if shape.has_table:
            print("    [TABLE]")
            for row in shape.table.rows:
                print("      " + " | ".join(c.text.strip() for c in row.cells))
    if slide.has_notes_slide and slide.notes_slide.notes_text_frame.text.strip():
        print(f"  [Заметки] {slide.notes_slide.notes_text_frame.text.strip()}")
