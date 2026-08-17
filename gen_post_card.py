"""
Generador de tarjetas visuales de contenido para redes sociales (Zentiq).

Uso:
    python3 gen_post_card.py

Edita las variables al final del archivo (bloque __main__) para cada post,
o importa `make_card()` desde otro script y llámala con esos parámetros.

Rutas relativas: este script asume que se ejecuta desde la raíz del repo,
con fonts/Inter.ttf y brand/zentiq_icon_512x512_white.png presentes.
"""
import os
import re
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# La fuente de marca (Inter) no trae glifos de emoji a color, y Pillow no hace
# fallback a otra fuente para dibujarlos: el resultado es un cuadro "sin glifo"
# roto en vez del emoji. Los quitamos solo del texto que se dibuja en la imagen
# (los captions de texto para LinkedIn/Facebook sí pueden llevar emojis).
_EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # símbolos y pictogramas variados, emoticones, transporte, etc.
    "\U00002600-\U000027BF"  # símbolos misceláneos y dingbats
    "\U0001F1E6-\U0001F1FF"  # banderas (pares de letras regionales)
    "\U00002190-\U000021FF"  # flechas (algunas usadas como emoji)
    "\U0000FE0F"              # variation selector-16 (fuerza estilo emoji)
    "\U0000200D"              # zero-width joiner (emojis compuestos)
    "]+",
    flags=re.UNICODE,
)


def strip_emoji(text):
    return _EMOJI_PATTERN.sub("", text).strip()

# ---------- Paleta de marca ----------
BG = (10, 10, 15)          # casi negro, con un toque azulado
ACCENT = (99, 102, 241)    # morado Zentiq (versión clara, para fondo oscuro)
WHITE = (245, 245, 247)
MUTED = (150, 150, 160)

W, H = 1080, 1080
FONT_PATH = os.path.join(BASE_DIR, "fonts", "Inter.ttf")
ICON_PATH = os.path.join(BASE_DIR, "brand", "zentiq_icon_512x512_white.png")


def load_font(size, weight="Regular"):
    font = ImageFont.truetype(FONT_PATH, size)
    font.set_variation_by_name(weight)
    return font


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def make_card(tag, headline, subtext, out_path, accent_words=None):
    accent_words = accent_words or []
    tag = strip_emoji(tag)
    headline = strip_emoji(headline)
    subtext = strip_emoji(subtext)
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Blob de luz decorativo
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    for r, alpha in [(420, 10), (320, 14), (220, 18)]:
        odraw.ellipse(
            [W - r - 60, -r + 140, W + r - 60, r + 140],
            fill=(*ACCENT, alpha),
        )
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # Marca de agua: ícono de Zentiq grande y muy tenue, abajo a la derecha
    icon = Image.open(ICON_PATH).convert("RGBA")
    icon_size = 620
    icon = icon.resize((icon_size, icon_size), Image.LANCZOS)
    alpha = icon.split()[3].point(lambda p: int(p * 0.05))
    icon.putalpha(alpha)
    img = img.convert("RGBA")
    img.alpha_composite(icon, (W - icon_size + 160, H - icon_size + 160))
    img = img.convert("RGB")

    draw = ImageDraw.Draw(img)
    margin = 90

    # Tag / categoría
    tag_font = load_font(28, "Bold")
    tag_text = tag.upper()
    tag_w = draw.textlength(tag_text, font=tag_font)
    pad_x, pad_y = 22, 12
    draw.rounded_rectangle(
        [margin, 90, margin + tag_w + pad_x * 2, 90 + 28 + pad_y * 2],
        radius=100, fill=ACCENT
    )
    draw.text((margin + pad_x, 90 + pad_y - 2), tag_text, font=tag_font, fill=WHITE)

    # Headline
    headline_font = load_font(64, "Bold")
    max_width = W - margin * 2
    lines = wrap_text(draw, headline, headline_font, max_width)
    y = 220
    line_height = 76
    for line in lines:
        x = margin
        words = line.split(" ")
        for word in words:
            clean = word.strip(".,:;!?").lower()
            color = ACCENT if clean in [w.lower() for w in accent_words] else WHITE
            draw.text((x, y), word, font=headline_font, fill=color)
            x += draw.textlength(word + " ", font=headline_font)
        y += line_height

    y += 20
    draw.line([(margin, y), (margin + 90, y)], fill=ACCENT, width=5)
    y += 40

    # Subtexto
    sub_font = load_font(34, "Regular")
    sub_lines = wrap_text(draw, subtext, sub_font, max_width)
    for line in sub_lines[:5]:
        draw.text((margin, y), line, font=sub_font, fill=MUTED)
        y += 46

    # Footer
    footer_font = load_font(30, "Bold")
    draw.text((margin, H - 110), "zentiq", font=footer_font, fill=WHITE)
    footer_sub_font = load_font(24, "Regular")
    draw.text((margin, H - 70), "Consultoría de BI e IA · zentiq.com.co", font=footer_sub_font, fill=MUTED)

    img.save(out_path, "PNG")
    print("Guardado en", out_path)


if __name__ == "__main__":
    make_card(
        tag="Automatización",
        headline="Tu WhatsApp puede responder solo, mientras tú atiendes el negocio.",
        subtext="Un flujo automático simple ya resuelve horarios, catálogo y pedidos básicos — sin que se te vaya ni un cliente por no contestar a tiempo.",
        out_path=os.path.join(BASE_DIR, "output", "post-ejemplo.png"),
        accent_words=["solo,", "solo"],
    )
