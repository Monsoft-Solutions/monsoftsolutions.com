#!/usr/bin/env python3
"""
Generate images for sustainable-technology-small-business-guide
Hero: gpt-image-1 high quality 1536x1024 (gpt-image-1.5 used for hero if available)
Inline 1-3: gpt-image-1 medium quality 1024x1024
(nano-banana-pro/Gemini API not available — GOOGLE_API_KEY is invalid for Gemini)
Then uploads to Vercel Blob (vwy1t1uzxwusskun store)
"""

import os
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
SLUG = 'sustainable-technology-small-business-guide'
IMAGES_DIR = Path(f'src/data/blog/{SLUG}/images')

IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def generate_image_openai(prompt, model='gpt-image-1', quality='medium', size='1024x1024'):
    """Generate image via OpenAI"""
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
        resp = urllib.request.urlopen(req, timeout=180)
        data = json.loads(resp.read())
        img_b64 = data['data'][0]['b64_json']
        return base64.b64decode(img_b64)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'OpenAI API error {e.code}: {body[:400]}')


def upload_to_blob(local_path, blob_path):
    """Upload file to Vercel Blob via API"""
    url = f'https://blob.vercel-storage.com/{blob_path}'
    with open(local_path, 'rb') as f:
        file_data = f.read()
    headers = {
        'Authorization': f'Bearer {BLOB_TOKEN}',
        'Content-Type': 'image/png',
        'x-content-type': 'image/png',
        'x-allow-overwrite': 'true',
    }
    req = urllib.request.Request(url, data=file_data, headers=headers, method='PUT')
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read())
        return data.get('url', url)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'Blob upload error {e.code}: {body[:400]}')


def save_image(img_bytes, filename):
    path = IMAGES_DIR / filename
    path.write_bytes(img_bytes)
    print(f'  Saved: {path} ({len(img_bytes):,} bytes)')
    return path


images = [
    {
        'filename': 'hero.png',
        'model': 'gpt-image-1',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'A modern small business office scene showing sustainable technology practices: '
            'a business owner at a standing desk with an energy-efficient laptop and LED lighting, '
            'solar panels visible through the window, a paperless digital workflow on screen, '
            'potted plants throughout the bright airy workspace, recycling bins for e-waste '
            'nearby. Clean minimalist aesthetic, professional photography style, natural light. '
            'No text or logos.'
        ),
    },
    {
        'filename': 'inline-1.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Infographic-style illustration showing energy-efficient business technology: '
            'Energy Star certified laptop, LED smart bulbs, smart power strip, and server rack '
            'with green leaf icons indicating low energy use. Clean flat design with green and '
            'blue color palette on white background, professional business illustration style. '
            'No text labels.'
        ),
    },
    {
        'filename': 'inline-2.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Split illustration comparing traditional paper-heavy office (stacks of paper, '
            'filing cabinets, printer running) on the left with a modern paperless digital '
            'office (tablets, cloud storage icons, digital signatures) on the right. '
            'Clean professional business illustration with green checkmarks on the digital side, '
            'soft blue and green tones. No text.'
        ),
    },
    {
        'filename': 'inline-3.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A small business storefront window display showing a "Green Business" certification '
            'badge and eco-friendly technology symbols: solar panel icon, recycling symbol, '
            'leaf/energy star icons. Customers walking by are drawn to the window. '
            'Warm inviting atmosphere, modern retail aesthetic. Professional photography style. '
            'No specific text on the signs.'
        ),
    },
]

print(f'Generating {len(images)} images for {SLUG}...\n')

blob_urls = {}

for img in images:
    print(f"Generating {img['filename']} ({img['model']} {img['quality']} {img['size']})...")
    try:
        img_bytes = generate_image_openai(
            prompt=img['prompt'],
            model=img['model'],
            quality=img['quality'],
            size=img['size'],
        )
        local_path = save_image(img_bytes, img['filename'])

        # Upload to Vercel Blob
        blob_path = f'blog/{SLUG}/{img["filename"]}'
        print(f'  Uploading to Blob: {blob_path}...')
        blob_url = upload_to_blob(local_path, blob_path)
        blob_urls[img['filename']] = blob_url
        print(f'  Blob URL: {blob_url}')
    except Exception as e:
        print(f'  ERROR: {e}')

print('\n=== BLOB URLs ===')
for fname, url in blob_urls.items():
    print(f'{fname}: {url}')
