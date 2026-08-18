import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gen_post_card import make_card, BASE_DIR

make_card(
    tag="Detrás de cámaras",
    headline="Un emoji roto nos enseñó algo sobre nuestro propio generador de posts",
    subtext="Así fue el bug que encontramos armando el sistema que genera estas mismas imágenes.",
    out_path=os.path.join(BASE_DIR, "output", "2026-08-18-post.png"),
    accent_words=["emoji", "generador"],
)
