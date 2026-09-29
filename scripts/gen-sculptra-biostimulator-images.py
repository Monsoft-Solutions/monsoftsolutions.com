#!/usr/bin/env python3
"""
Generate images for sculptra-biostimulator-marketing-med-spa-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: nano-banana-pro (Gemini) with gpt-image-1 fallback 1024x1024
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
SLUG = 'sculptra-biostimulator-marketing-med-spa-guide'
IMAGES_DIR = Path(f'src/data/blog/{SLUG}/images')
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def generate_openai(prompt, model='gpt-image-1', quality='medium', size='1024x1024'):
    """Generate image via OpenAI images API."""
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'n': 1,
        'size': size,
        'quality': quality
    }).encode()
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read())
            b64 = data['data'][0]['b64_json']
            return base64.b64decode(b64)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  OpenAI error {e.code}: {body[:300]}')
        return None
    except Exception as e:
        print(f'  OpenAI exception: {e}')
        return None


def try_nano_banana(prompt, filename):
    """Try nano-banana-pro (Gemini imagen); return True on success."""
    gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if not gemini_key:
        print('  No Gemini key available')
        return False
    try:
        url = (
            'https://generativelanguage.googleapis.com/v1beta/models/'
            'gemini-2.0-flash-preview-image-generation:generateContent'
            f'?key={gemini_key}'
        )
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'responseModalities': ['TEXT', 'IMAGE']}
        }).encode()
        req = urllib.request.Request(url, data=payload, headers=headers)
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    img_data = base64.b64decode(part['inlineData']['data'])
                    path = IMAGES_DIR / filename
                    path.write_bytes(img_data)
                    print(f'  ✅ nano-banana-pro: {filename} ({len(img_data)//1024}KB)')
                    return True
        print('  nano-banana-pro: no image in response')
        return False
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f'  nano-banana-pro HTTP {e.code}: {body[:200]}')
        return False
    except Exception as e:
        print(f'  nano-banana-pro exception: {e}')
        return False


def generate_with_fallback(prompt, filename, size='1024x1024'):
    """Try nano-banana-pro first, fall back to gpt-image-1."""
    print(f'\n→ Generating {filename}...')
    print('  Trying nano-banana-pro...')
    if try_nano_banana(prompt, filename):
        return True
    print('  Falling back to gpt-image-1...')
    data = generate_openai(prompt, model='gpt-image-1', quality='medium', size=size)
    if data:
        path = IMAGES_DIR / filename
        path.write_bytes(data)
        print(f'  ✅ gpt-image-1 fallback: {filename} ({len(data)//1024}KB)')
        return True
    print(f'  ❌ Failed: {filename}')
    return False


# ── Hero image (gpt-image-1.5, high quality, 1536x1024) ─────────────────────
print('\n=== Generating hero image with gpt-image-1.5 ===')
hero_prompt = (
    "A professional medical aesthetician in an upscale, modern med spa consultation room "
    "presenting a transparent vial of Sculptra PLLA injectable filler to a female patient "
    "in her early 50s seated in a luxurious treatment chair. The provider wears a crisp "
    "white coat and holds the vial with care, explaining the treatment. The room features "
    "warm clinical lighting, elegant white walls, subtle botanical decor, and premium medical "
    "equipment on a clean countertop. The atmosphere is sophisticated yet warmly professional — "
    "trust-inspiring and calming. The patient appears engaged and interested. Lifestyle medical "
    "photography style, warm tones. No text overlays. No logos. No visible branded labels."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1.5', quality='high', size='1536x1024')
if not hero_data:
    print('gpt-image-1.5 failed, trying gpt-image-1...')
    hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if hero_data:
    path = IMAGES_DIR / 'hero.png'
    path.write_bytes(hero_data)
    print(f'✅ Hero saved: hero.png ({len(hero_data)//1024}KB)')
else:
    print('❌ Hero generation failed')


# ── Inline 1: GLP-1 facial volume loss & restoration concept ─────────────────
generate_with_fallback(
    "A clean, professional split-composition medical lifestyle image showing two elegant "
    "side-by-side scenes: on the left, a thoughtful woman in her late 40s gently touching "
    "her face in a mirror, examining subtle facial changes with a concerned but composed "
    "expression. On the right, the same woman looking radiant and confident, face fuller "
    "and more youthful, in an upscale medical consultation room beside a friendly provider. "
    "Soft warm clinical tones, subtle medical aesthetic with elegant spa decor. "
    "No text overlays. No logos. Professional lifestyle photography.",
    'inline-1.png'
)

# ── Inline 2: Patient consultation with biostimulator education ───────────────
generate_with_fallback(
    "A professional med spa consultation scene: a skilled female aesthetic provider in a "
    "white medical coat sitting across from a female patient in her 50s, both examining "
    "a sleek tablet showing a before-and-after photo timeline — demonstrating gradual facial "
    "volume restoration with biostimulator treatment results at 2 months, 4 months, and "
    "6 months. The room is bright, modern, and elegant with clean white surfaces, subtle "
    "green plants, and soft ambient lighting. The patient looks engaged and hopeful. "
    "Warm professional tones. No text overlays. No logos.",
    'inline-2.png'
)

# ── Inline 3: Happy patient with natural youthful results ─────────────────────
generate_with_fallback(
    "A confident, elegant woman in her mid-50s with naturally full and youthful facial "
    "contours, radiant skin and soft lifting, smiling warmly and looking into a beautifully "
    "lit mirror in a luxurious med spa treatment room. She looks refreshed and naturally "
    "beautiful — not overdone, not obviously 'filled.' The setting is upscale: white marble, "
    "soft warm lighting, fresh white orchids, and clean clinical surfaces. She appears "
    "genuinely pleased with her reflection. Aspirational lifestyle photography, warm natural "
    "tones. No text overlays. No logos.",
    'inline-3.png'
)

print('\n✅ All images generated.')
