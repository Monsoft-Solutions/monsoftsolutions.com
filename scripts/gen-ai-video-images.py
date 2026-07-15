#!/usr/bin/env python3
"""
Generate images for ai-video-creation-small-business-guide
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
SLUG = 'ai-video-creation-small-business-guide'
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
    "A small business owner — a confident woman in her early 40s — sitting at a sleek modern "
    "desk, smiling as she watches an AI-generated video preview playing on a large monitor. "
    "The screen shows a polished marketing video with smooth transitions and professional text "
    "overlays. On a secondary tablet screen, an AI video editor interface is visible with "
    "timeline, scene thumbnails, and a 'Generate Video' button. The workspace is bright, "
    "contemporary, and inviting — warm lighting, minimal decor. "
    "Photorealistic, professional photography style, no visible text in the real environment."
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
    "A clean, modern infographic comparing three types of AI video creation tools for small "
    "business marketing. Three sections arranged horizontally: Section 1 labeled 'Text-to-Video' "
    "with a film clapper icon and examples (Sora, Runway, Kling). Section 2 labeled 'AI Avatars' "
    "with a person silhouette icon and examples (HeyGen, Synthesia). Section 3 labeled 'AI Editors' "
    "with a timeline/scissors icon and examples (Pictory, InVideo). Each section has a distinct "
    "color (blue, purple, teal). Clean white background, professional SaaS-style infographic design. "
    "Minimal text, icon-driven visual."
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
    "A smartphone held in hand showing a polished AI-generated marketing video for a local "
    "small business — a med spa or boutique service business. The video on screen shows a "
    "beautiful product/service showcase with smooth transitions, professional lighting, and "
    "a branded color scheme. The background is softly blurred (a modern office or cafe). "
    "The image conveys: this professional-looking video was created easily with AI. "
    "Photorealistic, editorial photography style, vibrant colors."
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
    "A split-screen marketing comparison image. Left side: traditional video production — "
    "a stressed business owner surrounded by camera equipment, lighting rigs, a film crew, "
    "stacks of invoices, and a '$5,000+' price tag label. Right side: modern AI video creation — "
    "the same business owner relaxed and smiling at a laptop with an AI video interface, "
    "a clock showing '20 min' and a '$0' or 'Free' badge. Clean professional design, slight "
    "comic-style infographic feel. Clear before/after contrast. Labels 'Before' and 'After AI'."
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
