#!/usr/bin/env python3
"""
Generate images for local-seo-aesthetic-practices-guide
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
SLUG = 'local-seo-aesthetic-practices-guide'
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
    "A polished, professional scene: an aesthetician or med spa manager in a modern, upscale "
    "medical spa reception area, reviewing a laptop showing a Google search results page with "
    "a map pack — the business appearing first in local search results with a 5-star rating. "
    "The reception area is elegant and welcoming, with soft lighting, neutral tones, and subtle "
    "medical spa decor. The professional looks confident and successful. A blurred Google Maps "
    "interface is visible on the laptop screen. "
    "Photorealistic, professional editorial photography style. No visible text in the real "
    "environment. Warm, aspirational mood."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1.5', quality='high', size='1536x1024')
if hero_data:
    save_image(hero_data, 'hero.png')
else:
    print('  gpt-image-1.5 failed, trying gpt-image-1...')
    hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
    if hero_data:
        save_image(hero_data, 'hero.png')
    else:
        print('  Hero generation failed')

# ---- INLINE 1 ----
print('\n=== Generating inline-1 (nano-banana-pro / gpt-image-1 fallback) ===')
inline1_prompt = (
    "A clean, professional infographic showing a Google search results page structure for a "
    "local aesthetic search query. Three stacked sections from top to bottom: "
    "1. 'Google Guaranteed / LSAs' section at the top with a green shield badge icon "
    "2. 'Google Map Pack' section in the middle showing 3 business listings with star ratings "
    "   and location pins on a mini map "
    "3. 'Organic Results' section at the bottom with website listing cards. "
    "Labels point to each section. Clean white background, blue and gold color scheme. "
    "Professional SaaS-style infographic. Medical/aesthetic industry feel."
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
    "A smartphone held in elegant hands (female aesthetician) showing a fully optimized "
    "Google Business Profile for a luxury med spa. The profile shows: a professional cover "
    "photo of a beautiful med spa interior, the business name, a 4.9-star rating with many "
    "reviews, a 'Book Now' button, hours, and the 'Medical Spa' category label. "
    "The background is softly blurred — a bright, upscale medical spa treatment room. "
    "Photorealistic, editorial photography style, vibrant but professional."
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
    "A modern business analytics dashboard on a laptop screen showing local SEO performance "
    "metrics for a medical spa or aesthetic practice. Dashboard displays: "
    "- A line graph trending upward labeled 'Local Search Impressions' "
    "- A bar chart showing 'Top Search Queries' with terms like botox, filler, med spa "
    "- A map with local ranking positions shown as numbered pins "
    "- Key metrics: 'Calls from Search: +47%', 'Direction Requests: +32%', 'Bookings: +28%' "
    "The laptop is on a clean desk in a modern med spa office. Professional, data-driven feel. "
    "Clean blue/teal color scheme with gold accents. Medical/professional aesthetic."
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
