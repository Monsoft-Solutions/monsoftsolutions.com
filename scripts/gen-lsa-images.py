#!/usr/bin/env python3
"""
Generate images for google-local-services-ads-guide
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
SLUG = 'google-local-services-ads-guide'
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
        with urllib.request.urlopen(req, timeout=120) as resp:
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
        import urllib.parse
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key={gemini_key}'
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'responseModalities': ['IMAGE', 'TEXT']}
        }).encode()
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            parts = data.get('candidates', [{}])[0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    img_bytes = base64.b64decode(part['inlineData']['data'])
                    path = IMAGES_DIR / filename
                    path.write_bytes(img_bytes)
                    print(f'  ✓ nano-banana-pro saved {filename} ({len(img_bytes):,} bytes)')
                    return True
        print('  nano-banana-pro: no image in response')
        return False
    except Exception as e:
        print(f'  nano-banana-pro failed: {e}')
        return False


def save_image(data, filename):
    path = IMAGES_DIR / filename
    path.write_bytes(data)
    print(f'  ✓ Saved {filename} ({len(data):,} bytes)')


# ---- HERO ----
print('\n=== Generating hero (gpt-image-1.5, high, 1536x1024) ===')
hero_prompt = (
    "A professional local service business owner — a friendly plumber in a clean uniform — "
    "looking at a laptop in his well-organized office. The laptop screen shows Google search "
    "results with Google Local Services Ads at the very top, including a prominent green "
    "'Google Guaranteed' badge next to his company listing. Warm, bright, professional office "
    "environment with business branding elements in the background. Photorealistic, natural "
    "lighting, no text overlaid on the real-world environment."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if hero_data:
    save_image(hero_data, 'hero.png')
else:
    print('  Hero generation failed')

# ---- INLINE 1 ----
print('\n=== Generating inline-1 (nano-banana-pro / gpt-image-1 fallback) ===')
inline1_prompt = (
    "Clean infographic diagram showing the three sections of a Google local search results page "
    "from top to bottom: Section 1 labeled 'Local Services Ads' with green Google Guaranteed "
    "badge icons, Section 2 labeled 'Google Ads' (pay-per-click), and Section 3 labeled "
    "'Organic Results / Google Maps'. Each section has a distinct color (green, blue, white). "
    "Simple, professional marketing infographic style on a light background, easy to read."
)
if not try_nano_banana(inline1_prompt, 'inline-1.png'):
    print('  Falling back to gpt-image-1...')
    inline1_data = generate_openai(inline1_prompt, model='gpt-image-1', quality='medium', size='1024x1024')
    if inline1_data:
        save_image(inline1_data, 'inline-1.png')
    else:
        print('  inline-1 generation failed')

# ---- INLINE 2 ----
print('\n=== Generating inline-2 (nano-banana-pro / gpt-image-1 fallback) ===')
inline2_prompt = (
    "A local service business owner sitting at a desk in a modern home office, smiling at a "
    "computer screen showing a Google Local Services Ads dashboard with verified status, star "
    "ratings, lead count metrics, and a green checkmark badge. Warm, professional, authentic "
    "small business atmosphere. No illegible small text — just clean UI elements on the screen."
)
if not try_nano_banana(inline2_prompt, 'inline-2.png'):
    print('  Falling back to gpt-image-1...')
    inline2_data = generate_openai(inline2_prompt, model='gpt-image-1', quality='medium', size='1024x1024')
    if inline2_data:
        save_image(inline2_data, 'inline-2.png')
    else:
        print('  inline-2 generation failed')

# ---- INLINE 3 ----
print('\n=== Generating inline-3 (nano-banana-pro / gpt-image-1 fallback) ===')
inline3_prompt = (
    "A split-screen infographic comparing two local service businesses in Google search results. "
    "Left side shows a business WITHOUT Google Local Services Ads — buried in results with no "
    "badge, fewer reviews. Right side shows the SAME business WITH Google Guaranteed badge at "
    "the top of results with 4.9 stars and 87 reviews. Arrow pointing right with 'More Calls' "
    "label. Clean, professional marketing visual with green accent colors."
)
if not try_nano_banana(inline3_prompt, 'inline-3.png'):
    print('  Falling back to gpt-image-1...')
    inline3_data = generate_openai(inline3_prompt, model='gpt-image-1', quality='medium', size='1024x1024')
    if inline3_data:
        save_image(inline3_data, 'inline-3.png')
    else:
        print('  inline-3 generation failed')

print('\n=== All images done ===')
for f in sorted(IMAGES_DIR.glob('*.png')):
    print(f'  {f.name}: {f.stat().st_size:,} bytes')
