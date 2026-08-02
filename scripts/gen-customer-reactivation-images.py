#!/usr/bin/env python3
"""
Generate images for customer-reactivation-automation-local-business
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
SLUG = 'customer-reactivation-automation-local-business'
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
    "A confident small business owner — a woman in her 40s — sits at a clean desk in her "
    "Florida shop, looking at a laptop screen displaying a CRM dashboard with customer "
    "win-back campaign analytics: colorful charts, customer segments, re-engagement metrics. "
    "She has a warm, hopeful expression, like she just discovered something valuable. "
    "Bright, warm office with plants and natural light. Professional photography style. "
    "Modern, clean aesthetic. No text overlays on the image."
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

# ── Inline 1: Win-back sequence workflow ─────────────────────────────────────
generate_with_fallback(
    "Clean, modern flat-design illustration of an automated customer win-back email and SMS "
    "sequence workflow. The diagram shows a timeline with 5 steps: a friendly check-in "
    "message, a value reminder, an incentive offer, a last-chance nudge, and a clean exit "
    "message. Each step is represented by an icon (envelope, gift, clock, handshake). "
    "Color scheme: blue, teal, and white. Professional infographic style. No real brand logos.",
    'inline-1.png'
)

# ── Inline 2: CRM dashboard with customer segments ───────────────────────────
generate_with_fallback(
    "A laptop screen showing a professional CRM customer segmentation dashboard. The interface "
    "displays groups of lapsed customers organized by recency and value: high-value recent, "
    "high-value older, standard recent. Clean data tables with customer names blurred for "
    "privacy. Charts showing re-engagement rates and campaign performance metrics. "
    "Blue and white color scheme, modern SaaS UI. Hands on keyboard in frame. "
    "Professional business context. No text readable. No real brand logos.",
    'inline-2.png'
)

# ── Inline 3: Revenue comparison chart ───────────────────────────────────────
generate_with_fallback(
    "Professional business infographic showing a bar chart comparison between the high cost "
    "of new customer acquisition versus the lower cost and higher ROI of customer reactivation. "
    "Two contrasting bars: one tall red/orange bar labeled 'New Customer' and one shorter "
    "green bar labeled 'Win-Back' with a much higher ROI arrow pointing upward. "
    "Clean, modern flat design, business presentation style. Light background. "
    "Dollar signs and percentage symbols as accents. Professional color palette.",
    'inline-3.png'
)

print('\n✅ All images generated.')
