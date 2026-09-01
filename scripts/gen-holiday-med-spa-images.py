#!/usr/bin/env python3
"""
Generate images for holiday-season-marketing-med-spa-guide
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
SLUG = 'holiday-season-marketing-med-spa-guide'
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
    gemini_key = os.environ.get('GEMINI_API_KEY')
    if not gemini_key:
        print('  No GEMINI_API_KEY available, skipping nano-banana-pro')
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
    "An upscale medical spa reception area elegantly decorated for the holiday season. "
    "Tasteful white and gold holiday decor — eucalyptus garland, white LED fairy lights, "
    "orchids, and small gold-accented ornaments on the reception desk. A stylish female "
    "receptionist in crisp white scrubs smiles warmly at a patient arriving for a holiday "
    "treatment appointment. The spa interior is bright and luxurious — marble surfaces, "
    "modern lighting, a clean minimalist aesthetic with festive yet understated holiday touches. "
    "Gift card display stand visible near the reception desk. "
    "Photorealistic, warm and inviting atmosphere, no text overlays, high-end medical spa."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1.5', quality='high', size='1536x1024')
if not hero_data:
    print('gpt-image-1.5 failed, trying gpt-image-1 high...')
    hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if hero_data:
    path = IMAGES_DIR / 'hero.png'
    path.write_bytes(hero_data)
    print(f'✅ Hero saved: hero.png ({len(hero_data)//1024}KB)')
else:
    print('❌ Hero generation failed')

# ── Inline 1: Holiday marketing calendar / timeline ─────────────────────────
generate_with_fallback(
    "Clean, elegant infographic-style illustration of a med spa holiday marketing calendar. "
    "Shows three months in a linear timeline: October (pumpkin icon, fall skin refresh), "
    "November (autumn leaf, gift card launch, Black Friday promo), December (snowflake, "
    "party prep, last-minute booking). Each month has small icons representing: email campaign, "
    "SMS blast, social media post, gift card. Soft gold, white, and deep green color palette "
    "matching luxury medical aesthetics. Modern flat design with elegant typography placeholders. "
    "No real brand logos, no photorealistic elements — clean vector illustration style.",
    'inline-1.png'
)

# ── Inline 2: Aesthetic injector showing holiday gift card options to patient ─
generate_with_fallback(
    "Warm professional scene inside a beautifully decorated med spa treatment room during the "
    "holiday season. A female aesthetic nurse or injector in white scrubs holds an elegant "
    "gift card packaging display and shows available holiday treatment packages on an iPad "
    "to a happy female patient seated in a comfortable treatment chair. "
    "Subtle holiday decorations in the background — white LED lights, eucalyptus garland. "
    "Warm, inviting lighting. Both women are smiling and engaged. "
    "Photorealistic, upscale medical aesthetic setting. No text overlays.",
    'inline-2.png'
)

# ── Inline 3: Holiday gift card display at med spa front desk ─────────────────
generate_with_fallback(
    "Elegant med spa front desk display featuring holiday gift cards and packaged treatment "
    "bundles. Beautiful gift card holders in gold and white, small elegant gift boxes tied "
    "with ribbon, a digital display screen showing holiday specials in soft gold text. "
    "Marble desk surface, fresh white orchids, and tasteful holiday greenery in background. "
    "Warm ambient lighting creating a luxurious, gift-giving atmosphere. "
    "Photorealistic high-end med spa environment. No specific brand logos.",
    'inline-3.png'
)

print('\n✅ All images generated.')
