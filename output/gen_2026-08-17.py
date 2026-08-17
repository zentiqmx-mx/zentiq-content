import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_post_card import make_card, BASE_DIR

make_card(
    tag="Dato curioso",
    headline="El primer 'bug' informático fue, literalmente, un insecto real",
    subtext="En 1947 encontraron una polilla atorada en un relé y así nació la palabra 'bug' en programación.",
    out_path=os.path.join(BASE_DIR, "output", "2026-08-17-post.png"),
    accent_words=["bug", "insecto"],
)
