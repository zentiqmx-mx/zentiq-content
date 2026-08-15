# Zentiq — Contenido para redes sociales

Repo de soporte para la rutina diaria de generación de posts (LinkedIn/Facebook).

## Contenido

- `gen_post_card.py` — genera la tarjeta visual de marca (1080x1080 PNG)
- `fonts/Inter.ttf` — tipografía variable (Inter, open source, OFL license)
- `brand/` — assets de marca de Zentiq
- `output/` — imágenes generadas (no versionadas, se regeneran cada corrida)

## Uso

```
pip install -r requirements.txt
python3 gen_post_card.py
```

Edita el bloque `if __name__ == "__main__":` al final de `gen_post_card.py`
con el `tag`, `headline`, `subtext` y `accent_words` del post del día.
