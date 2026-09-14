#!/usr/bin/env python3
"""
Generate images for black-friday-cyber-monday-small-business-guide
Hero: gpt-image-1.5 high quality 1536x1024
Inline 1-3: nano-banana-pro (Gemini) with gpt-image-1 fallback
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
SLUG = 'black-friday-cyber-monday-small-business-guide'
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
    """Try nano-banana-pro (Gemini); return True on success."""
    gemini_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
    if not gemini_key:
        print('  No Gemini key available')
        return False
    try:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-preview-image-generation:generateContent?key={gemini_key}'
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
    "A cheerful small business owner in a cozy boutique shop decorated with Black Friday sale "
    "signs, warm autumn decor — orange and gold leaves, subtle holiday warmth. The owner stands "
    "confidently behind a counter with a laptop open showing a marketing campaign dashboard with "
    "upward revenue charts. Sale tags hang from product displays in the background. The atmosphere "
    "is festive, energetic, and optimistic. Soft natural lighting with warm amber tones. "
    "Professional photography style. No text on screen or overlays. No brand logos."
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

# ── Inline 1: 10-Week BFCM countdown timeline / planning calendar ─────────────
generate_with_fallback(
    "A clean, visually appealing infographic-style illustration showing a 10-week marketing "
    "countdown calendar. Four distinct phases shown as colored horizontal bands or milestone "
    "icons: Phase 1 Strategy (weeks 1-3, amber), Phase 2 List Building (weeks 4-6, teal), "
    "Phase 3 Pre-Launch (weeks 7-9, deep orange), Phase 4 Launch and Cyber Monday (week 10, "
    "bold red/gold). Each phase has small icons — calendar, email envelope, megaphone, shopping "
    "cart. Modern flat design illustration, professional color scheme, no real text needed "
    "except minimal phase labels. Holiday sale countdown energy.",
    'inline-1.png'
)

# ── Inline 2: Email and SMS campaign for BFCM ──────────────────────────────
generate_with_fallback(
    "A small business owner working at a laptop in a cozy autumn-decorated home office, "
    "composing a Black Friday email campaign. The laptop screen shows an email marketing "
    "platform with campaign statistics — open rates, click rates, subscriber count. "
    "A smartphone on the desk shows an SMS marketing notification preview. "
    "Autumn decor: small pumpkins, warm candlelight, leaves on the windowsill. "
    "Professional and inviting atmosphere. No real brand logos. Photorealistic style. "
    "Warm amber and teal color tones. No text overlays.",
    'inline-2.png'
)

# ── Inline 3: Local small business BFCM in-store event / customer excitement ───
generate_with_fallback(
    "An excited crowd of shoppers entering a warmly lit local boutique shop decorated for "
    "a Black Friday sale event. Festive window displays, tasteful sale signage in the window, "
    "happy customers browsing products. Staff members assist customers with warm smiles. "
    "The atmosphere is busy, festive, and celebratory. Autumn-to-holiday transition decor. "
    "Street view from slightly outside looking in through the inviting storefront window. "
    "Professional photography style, vibrant and energetic. No specific brand names visible.",
    'inline-3.png'
)

print('\n✅ All images generated.')
