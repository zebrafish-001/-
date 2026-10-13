"""Export helpers: SVG -> PNG / TIFF / PDF at journal resolution; PPTX -> preview PNG."""
from __future__ import annotations

import io
import os
import shutil
import subprocess
import tempfile
from typing import Optional

from .presets import MM_PER_IN, Preset


def svg_to_png(svg: str, path: str, preset: Preset, dpi: int = 300) -> str:
    import cairosvg
    w_px = int(round(preset.width_mm / MM_PER_IN * dpi))
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=path, output_width=w_px)
    _set_dpi(path, dpi)
    return path


def svg_to_tiff(svg: str, path: str, preset: Preset, dpi: int = 300) -> str:
    import cairosvg
    from PIL import Image
    w_px = int(round(preset.width_mm / MM_PER_IN * dpi))
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=w_px)
    im = Image.open(io.BytesIO(png)).convert("RGB")   # flatten alpha onto white for TIFF
    bg = Image.new("RGB", im.size, (255, 255, 255))
    src = Image.open(io.BytesIO(png))
    if src.mode == "RGBA":
        bg.paste(src, mask=src.split()[3])
        im = bg
    im.save(path, format="TIFF", compression="tiff_lzw", dpi=(dpi, dpi))
    return path


def svg_to_pdf(svg: str, path: str) -> str:
    import cairosvg
    cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to=path)
    return path


def _set_dpi(png_path: str, dpi: int):
    try:
        from PIL import Image
        im = Image.open(png_path)
        im.save(png_path, dpi=(dpi, dpi))
    except Exception:
        pass


def pptx_preview(pptx_path: str, out_png: str, dpi: int = 300) -> Optional[str]:
    """Render the PPTX with LibreOffice (PDF) then rasterise page 1 — a check that the deck matches the SVG."""
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        return None
    tmp = tempfile.mkdtemp(prefix="tocmaker_prev_")
    try:
        subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, pptx_path],
                       capture_output=True, timeout=180, check=False)
        pdf = os.path.join(tmp, os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf")
        if not os.path.exists(pdf):
            return None
        if shutil.which("pdftoppm"):
            base = os.path.join(tmp, "page")
            subprocess.run(["pdftoppm", "-r", str(dpi), "-png", "-singlefile", pdf, base], capture_output=True,
                           timeout=120, check=False)
            if os.path.exists(base + ".png"):
                shutil.move(base + ".png", out_png)
                return out_png
        try:
            import cairosvg  # noqa: F401  (no PDF rasteriser in cairosvg; fall back to LibreOffice PNG)
        except Exception:
            pass
        subprocess.run([soffice, "--headless", "--convert-to", "png", "--outdir", tmp, pptx_path],
                       capture_output=True, timeout=180, check=False)
        png = os.path.join(tmp, os.path.splitext(os.path.basename(pptx_path))[0] + ".png")
        if os.path.exists(png):
            shutil.move(png, out_png)
            return out_png
        return None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
