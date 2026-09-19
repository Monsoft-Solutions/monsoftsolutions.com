#!/usr/bin/env python3
"""
Generate images for skin-tightening-marketing-med-spa-guide
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
SLUG = 'skin-tightening-marketing-med-spa-guide'
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
                    print(f'  nano-banana-pro: {filename} ({len(img_data)//1024}KB)')
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
    print(f'\n-> Generating {filename}...')
    print('  Trying nano-banana-pro...')
    if try_nano_banana(prompt, filename):
        return True
    print('  Falling back to gpt-image-1...')
    data = generate_openai(prompt, model='gpt-image-1', quality='medium', size=size)
    if data:
        path = IMAGES_DIR / filename
        path.write_bytes(data)
        print(f'  gpt-image-1 fallback: {filename} ({len(data)//1024}KB)')
        return True
    print(f'  FAILED: {filename}')
    return False


# Hero image (gpt-image-1.5, high quality, 1536x1024)
print('\n=== Generating hero image with gpt-image-1.5 ===')
hero_prompt = (
    "A professional aesthetician in a modern, upscale medical spa performing a non-invasive "
    "skin tightening treatment on a relaxed female patient in her late 40s. The aesthetician "
    "holds a sleek ultrasound or radiofrequency device handpiece gently against the patient's "
    "jawline and neck area. The room features soft white and sage green tones, professional "
    "clinical lighting, and elegant spa decor with marble accents. The patient appears "
    "comfortable and relaxed in a treatment chair. The atmosphere is luxurious and clinical. "
    "Professional medical spa photography style. No text overlays. No brand logos."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1.5', quality='high', size='1536x1024')
if not hero_data:
    print('gpt-image-1.5 failed, trying gpt-image-1 high...')
    hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if hero_data:
    path = IMAGES_DIR / 'hero.png'
    path.write_bytes(hero_data)
    print(f'Hero saved: hero.png ({len(hero_data)//1024}KB)')
else:
    print('Hero generation FAILED')

# Inline 1: Skin tightening treatment comparison / technology illustration
generate_with_fallback(
    "A clean, modern medical infographic-style illustration showing three non-invasive skin "
    "tightening technology icons side by side: focused ultrasound waves, monopolar "
    "radiofrequency energy, and combination energy pulses. Each technology depicted with "
    "simple diagrams showing energy penetrating skin layers with upward arrows indicating "
    "lifting and tightening effects. Soft clinical color palette of blue, white, and sage "
    "green. No readable text labels. Modern medical aesthetic illustration style. No brand logos.",
    'inline-1.png'
)

# Inline 2: Before/after concept - patient looking refreshed
generate_with_fallback(
    "A confident, radiant woman in her early 50s with visibly lifted and tightened skin "
    "around her jawline and neck, examining her profile in a large illuminated vanity mirror "
    "in a luxurious medical spa. She is smiling with genuine satisfaction. Bright, clean spa "
    "environment with soft warm lighting and elegant decor. No text overlays. Professional "
    "beauty and medical spa photography style.",
    'inline-2.png'
)

# Inline 3: Med spa owner reviewing marketing analytics dashboard
generate_with_fallback(
    "A professional med spa marketing manager reviewing skin tightening treatment booking "
    "analytics on a sleek laptop at a modern reception desk in an upscale aesthetic practice. "
    "The screen displays a calendar with bookings, patient return rate charts, and upward "
    "trending revenue graphs. Elegant office environment with marble accents and professional "
    "lighting. Clean modern business aesthetic. No text overlays. No brand logos.",
    'inline-3.png'
)

print('\nAll images generated.')
