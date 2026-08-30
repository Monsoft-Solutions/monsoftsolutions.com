#!/usr/bin/env python3
"""
Generate images for website-maintenance-checklist-small-business
Hero: gpt-image-1 high quality 1536x1024
Inline 1-3: gpt-image-1 medium quality 1024x1024
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
SLUG = 'website-maintenance-checklist-small-business'
IMAGES_DIR = Path(f'src/data/blog/{SLUG}/images')

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def generate_image_openai(prompt, quality='medium', size='1024x1024'):
    """Generate image via OpenAI gpt-image-1"""
    url = 'https://api.openai.com/v1/images/generations'
    headers = {
        'Authorization': f'Bearer {OPENAI_KEY}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        'model': 'gpt-image-1',
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
    """Upload file to Vercel Blob via REST PUT"""
    with open(local_path, 'rb') as f:
        file_data = f.read()
    content_type = 'image/png'
    url = f'https://blob.vercel-storage.com/{blob_path}'
    headers = {
        'Authorization': f'Bearer {BLOB_TOKEN}',
        'Content-Type': content_type,
        'x-content-type': content_type,
        'x-add-random-suffix': 'false',
        'x-cache-control-max-age': '31536000',
    }
    req = urllib.request.Request(url, data=file_data, headers=headers, method='PUT')
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        result = json.loads(resp.read())
        return result.get('url', '')
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise Exception(f'Blob upload error {e.code}: {body[:400]}')


IMAGES = [
    {
        'file': 'hero.png',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'A focused small business owner sitting at a clean wooden desk reviewing a website maintenance '
            'checklist on a laptop screen. The laptop shows a website analytics dashboard with green uptime '
            'indicators and performance graphs. A coffee mug and notepad with checkmarks sit beside the laptop. '
            'Natural window light, modern home office or small business setting. Professional, warm, organized '
            'atmosphere. Wide landscape composition with blue and white color accents on the website interface.'
        ),
    },
    {
        'file': 'inline-1.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clean flat-design infographic showing a website maintenance schedule calendar. '
            'Four colored sections labeled Weekly, Monthly, Quarterly, and Annual with small '
            'icon checkboxes for tasks like security scans, backups, content updates, and plugin '
            'updates. Modern business style with blue, green, orange, and purple color coding. '
            'White background with rounded card design. Professional and easy to read.'
        ),
    },
    {
        'file': 'inline-2.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A professional illustration showing website security monitoring on a computer screen. '
            'The screen displays a security dashboard with a shield icon, SSL certificate green lock, '
            'uptime monitoring graph showing 99.9% uptime, and malware scan results showing "All Clear". '
            'Clean flat design with a blue and dark navy color scheme, glowing UI elements, modern '
            'tech aesthetic on a dark background.'
        ),
    },
    {
        'file': 'inline-3.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A side-by-side comparison visualization showing website performance improvement. '
            'Left side labeled "Neglected Website" shows slow load times with a red clock, broken '
            'links with X marks, outdated design elements. Right side labeled "Well-Maintained Website" '
            'shows fast loading green checkmarks, modern design, happy customer icon with 5 stars. '
            'Clean infographic style, professional business aesthetic, white background with clear '
            'visual contrast between the two sides.'
        ),
    },
]


def main():
    print(f'Generating {len(IMAGES)} images for {SLUG}...\n')
    results = {}

    for img in IMAGES:
        fname = img['file']
        local_path = IMAGES_DIR / fname
        blob_path = f'blog/{SLUG}/{fname}'

        print(f'[1/2] Generating {fname} (quality={img["quality"]}, size={img["size"]})...')
        try:
            img_bytes = generate_image_openai(img['prompt'], img['quality'], img['size'])
            with open(local_path, 'wb') as f:
                f.write(img_bytes)
            size_kb = len(img_bytes) / 1024
            print(f'      ✅ Saved {local_path} ({size_kb:.0f} KB)')
        except Exception as e:
            print(f'      ❌ Generation failed: {e}')
            continue

        print(f'[2/2] Uploading to Vercel Blob as {blob_path}...')
        try:
            url = upload_to_blob(local_path, blob_path)
            results[fname] = url
            print(f'      ✅ {url}')
        except Exception as e:
            print(f'      ❌ Upload failed: {e}')

        print()

    print('=' * 60)
    print('FINAL BLOB URLs:')
    for fname, url in results.items():
        print(f'  {fname}: {url}')
    print('=' * 60)


if __name__ == '__main__':
    main()
