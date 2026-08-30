#!/usr/bin/env python3
"""
Generate images for iv-therapy-marketing-med-spa-guide
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
SLUG = 'iv-therapy-marketing-med-spa-guide'
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
        print('  No Gemini API key available, skipping nano-banana-pro')
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
    "A luxurious med spa IV therapy lounge featuring a relaxed, well-dressed woman in her 40s "
    "reclining in a plush white treatment chair receiving an IV vitamin drip. The room has soft "
    "amber and white lighting, modern decor with natural wood accents, fresh eucalyptus, and a "
    "serene spa atmosphere. An IV bag hanging from a sleek chrome stand is visible. The patient "
    "looks calm and pampered, wearing comfortable clothing, reading a magazine. A friendly "
    "medical professional in clean scrubs checks the IV nearby. Bright, airy, upscale wellness "
    "center aesthetic. Natural light from large windows. No text overlays. Photorealistic, "
    "high-end medical wellness experience."
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

# ── Inline 1: IV therapy service menu / treatment types ─────────────────────
generate_with_fallback(
    "Clean, professional infographic-style illustration showing 4 popular IV therapy drip types "
    "in a medical spa context. Each panel shows an icon and name: Immunity Boost (shield + "
    "vitamin C), Athletic Recovery (lightning bolt + electrolytes), Beauty Glow (sparkle + "
    "glutathione), and Energy Recharge (battery + B vitamins). Soft teal and gold color palette "
    "with a luxury spa aesthetic. Modern flat design with minimal text labels only. "
    "Clean white background with subtle gradient. Medical wellness branding. "
    "No real pharmaceutical logos or brand names.",
    'inline-1.png'
)

# ── Inline 2: Med spa owner reviewing IV therapy marketing analytics ──────────
generate_with_fallback(
    "Professional med spa owner or marketing manager sitting at a modern desk reviewing "
    "marketing analytics on a sleek laptop. The screen shows graphs with upward trends: "
    "new IV therapy bookings increasing month over month, social media engagement metrics, "
    "and Google search visibility. Modern, bright office space with plants and natural light. "
    "Clean, professional aesthetic. The person looks satisfied and confident. "
    "Medical wellness industry setting. No real software logos. Photorealistic.",
    'inline-2.png'
)

# ── Inline 3: Social media content creation for IV therapy ────────────────────
generate_with_fallback(
    "A behind-the-scenes scene of a med spa creating social media content for their IV therapy "
    "service. A content creator photographs an aesthetically arranged IV drip setup with fresh "
    "citrus slices, green leaves, and a stylish IV bag on a marble surface. Clean flat-lay "
    "photography setup with ring light. Modern, Instagram-worthy aesthetic. "
    "Warm natural tones, luxury wellness brand feel. "
    "No real product logos. Professional content creation for wellness brand. Photorealistic.",
    'inline-3.png'
)

print('\n✅ All images generated.')
