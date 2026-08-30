#!/usr/bin/env python3
"""
Generate images for ai-contract-management-small-business-guide
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
SLUG = 'ai-contract-management-small-business-guide'
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
    "A small business owner and a client seated across a modern conference table. "
    "The client is signing a digital contract on a sleek tablet using a stylus, while "
    "the business owner smiles and reviews the document on a laptop. "
    "The laptop screen shows a clean contract management interface with signature fields, "
    "progress indicators, and green checkmarks. Warm natural office lighting, plants in "
    "the background, wooden table. Professional yet approachable atmosphere. "
    "No real software logos or brand names visible. Photorealistic style."
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

# ── Inline 1: AI Contract Workflow Diagram ───────────────────────────────────
generate_with_fallback(
    "Clean flat-design infographic showing a modern AI contract management workflow. "
    "A horizontal or circular flow diagram with six labeled steps connected by arrows: "
    "1) Draft (pen icon) → 2) AI Review (brain/sparkle icon) → 3) Send (envelope icon) → "
    "4) E-Sign (signature icon) → 5) Track (eye/clock icon) → 6) Renew (refresh icon). "
    "Each step has a small icon and brief label. Color-coded circles: blues and teals. "
    "Clean white background. Modern SaaS illustration style. No real brand logos.",
    'inline-1.png'
)

# ── Inline 2: Before vs After Comparison ─────────────────────────────────────
generate_with_fallback(
    "A split-screen side-by-side comparison illustration. "
    "LEFT side labeled 'Before': a cluttered desk with stacks of paper contracts, "
    "sticky notes everywhere, an overflowing email inbox on a monitor, and a stressed "
    "business owner looking overwhelmed. Red or orange color tones. "
    "RIGHT side labeled 'After': a clean, organized workspace with a digital contract "
    "dashboard on screen showing signed agreements, automated reminders, and organized "
    "status tracking. The business owner looks calm and confident. Green and teal tones. "
    "Professional business illustration style. No real software logos.",
    'inline-2.png'
)

# ── Inline 3: Contract Analytics Dashboard ───────────────────────────────────
generate_with_fallback(
    "A small business owner sitting at a modern desk reviewing a contract management "
    "analytics dashboard on a large monitor. The dashboard displays: number of contracts "
    "sent this month, contracts signed (with green checkmark count), contracts awaiting "
    "signature (with clock icons), upcoming renewal alerts highlighted in amber, and "
    "average time-to-sign metric. Charts show a downward trend in time-to-close. "
    "The business owner looks organized and pleased. Clean home office setting with "
    "natural light. No real software UI or brand names. Photorealistic style.",
    'inline-3.png'
)

print('\n✅ All images generated.')
