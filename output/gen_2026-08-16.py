import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_post_card import make_card, BASE_DIR

make_card(
    tag="Automatización",
    headline="El primer paso para automatizar tu WhatsApp no es un bot",
    subtext="Antes de automatizar todo, identifica las preguntas que más te repiten los clientes. Ahí está el mayor ahorro de tiempo.",
    out_path=os.path.join(BASE_DIR, "output", "2026-08-16-post.png"),
    accent_words=["whatsapp", "bot"],
)
