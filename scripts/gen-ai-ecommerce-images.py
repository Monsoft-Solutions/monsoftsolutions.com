#!/usr/bin/env python3
"""
Generate images for ai-ecommerce-small-business-guide
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
SLUG = 'ai-ecommerce-small-business-guide'
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
    "A confident small business owner smiling at a dual-monitor setup in a modern home studio "
    "or boutique office. One screen shows an e-commerce store dashboard with sales charts, "
    "product listings, and order notifications. The other displays an AI analytics panel with "
    "recommendation algorithms and customer segments visualized. Packaged products are visible "
    "on shelves or a nearby table — clean, branded packaging. The atmosphere is bright, "
    "productive, and entrepreneurial. Natural daylight, professional photography style. "
    "No brand logos. No text overlays on screens."
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

# ── Inline 1: AI product recommendations / personalization dashboard ───────────
generate_with_fallback(
    "A clean flat-design illustration showing an AI-powered product recommendation engine "
    "in action. A stylized e-commerce product page on the left shows a customer browsing, "
    "while an AI system in the center analyzes browsing behavior, purchase history, and "
    "customer segments using connected nodes and data flows. On the right, personalized "
    "'Recommended for You' product cards appear. Arrows show the data flow from customer "
    "behavior through AI analysis to personalized recommendations. Modern teal and deep blue "
    "color palette with orange accents. Professional illustration style, no real text except "
    "minimal labels. Clean, tech-forward visual.",
    'inline-1.png'
)

# ── Inline 2: Abandoned cart recovery automation ───────────────────────────────
generate_with_fallback(
    "A small business owner at a laptop reviewing automated marketing campaign results, "
    "with a satisfied expression. The screen shows a cart abandonment recovery dashboard "
    "with email open rates, SMS recovery rates, and revenue recovered metrics displayed as "
    "upward-trending charts. A smartphone on the desk displays a preview of an abandoned "
    "cart email notification. The workspace is neat and modern — clean desk, soft afternoon "
    "light, a small plant. Professional photorealistic style, warm and productive atmosphere. "
    "No brand logos. No text overlays on screen.",
    'inline-2.png'
)

# ── Inline 3: AI visual search and product photography ────────────────────────
generate_with_fallback(
    "A modern e-commerce product photography setup with AI enhancement. A small table studio "
    "with a product (a nicely packaged item or cosmetic) under professional lighting. A "
    "tablet displays an AI photo editing interface with automated background removal and "
    "enhancement applied — showing before/after comparison of a product photo. The overall "
    "scene conveys technology making professional product photography accessible to small "
    "businesses. Clean white and light gray tones, minimalist setup, professional product "
    "photography aesthetic. No brand logos visible.",
    'inline-3.png'
)

print('\n✅ All images generated.')
