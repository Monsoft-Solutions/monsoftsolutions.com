#!/usr/bin/env python3
"""
Generate images for ai-cybersecurity-small-business-guide
Hero: gpt-image-1 high quality 1536x1024
Inline 1-3: nano-banana-pro (Gemini) with gpt-image-1 fallback
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
SLUG = 'ai-cybersecurity-small-business-guide'
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


# ── Hero image (gpt-image-1 high quality, 1536x1024) ─────────────────────
print('\n=== Generating hero image with gpt-image-1 high ===')
hero_prompt = (
    "A small business owner at a modern desk reviewing an AI-powered cybersecurity dashboard "
    "on a large monitor. The screen shows real-time threat detection graphs, a green shield "
    "icon indicating protection status, and blocked threat notifications in a clean interface. "
    "The office is bright and professional — neutral tones, natural light from a window, a "
    "plant on the desk. The business owner looks confident and in control. The atmosphere "
    "conveys security, professionalism, and digital protection without fear or alarm. "
    "Photorealistic, high-quality commercial photography style. No brand logos. No text overlays."
)
hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='high', size='1536x1024')
if not hero_data:
    print('gpt-image-1 high failed, trying medium...')
    hero_data = generate_openai(hero_prompt, model='gpt-image-1', quality='medium', size='1536x1024')
if hero_data:
    path = IMAGES_DIR / 'hero.png'
    path.write_bytes(hero_data)
    print(f'✅ Hero saved: hero.png ({len(hero_data)//1024}KB)')
else:
    print('❌ Hero generation failed')

# ── Inline 1: Cybersecurity stack layers diagram ─────────────────────────────
generate_with_fallback(
    "A clean, modern flat-design infographic illustration showing the layers of a small business "
    "cybersecurity stack. Four vertical shield icons or layers arranged in a clean grid: "
    "1) Endpoint Protection (laptop icon with shield), 2) Email Security (envelope with lock), "
    "3) Identity and Access (key and fingerprint), 4) Backup and Recovery (cloud with arrow). "
    "Each layer has a subtle AI brain or circuit pattern indicating AI-powered features. "
    "Color palette: deep navy blue background with teal, white, and gold accents. "
    "Clean professional infographic style. Minimal text labels only. No brand logos.",
    'inline-1.png'
)

# ── Inline 2: MFA / identity setup scene ─────────────────────────────────────
generate_with_fallback(
    "A business owner in a modern office sitting at a desk, holding a smartphone showing "
    "a multi-factor authentication confirmation screen with an approval button. "
    "A laptop on the desk shows a secure login screen. The scene feels calm and empowering — "
    "this is a person in control of their digital security, not someone reacting to an emergency. "
    "Bright, professional office setting with natural light, neutral tones, minimal decor. "
    "Photorealistic photography style. No brand logos on devices. No text overlays on screens.",
    'inline-2.png'
)

# ── Inline 3: AI threat detection visualization ───────────────────────────────
generate_with_fallback(
    "A modern security operations concept visualization — a sleek AI security dashboard "
    "on a large monitor showing network activity graphs, a real-time threat map with "
    "flagged suspicious activity highlighted in amber/orange, and an AI system automatically "
    "blocking a phishing attempt (shown as a red email being intercepted by a shield). "
    "The overall color scheme is dark navy with bright teal and green indicators. "
    "The interface looks sophisticated but accessible — built for a business owner, not a "
    "security engineer. Clean, modern UI design style. No brand logos. No text overlays.",
    'inline-3.png'
)

print('\n✅ All images generated.')
