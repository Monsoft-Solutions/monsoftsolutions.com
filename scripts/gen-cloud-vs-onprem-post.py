#!/usr/bin/env python3
"""
Generate images for cloud-vs-on-premise-software-guide
Uses gpt-image-1 (gpt-image-1.5 equivalent — model='gpt-image-1')
Hero: high quality 1536x1024, Inline: medium quality 1024x1024
Then uploads to Vercel Blob
"""

import os
import json
import base64
import urllib.request
import urllib.error
import sys
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
SLUG = 'cloud-vs-on-premise-software-guide'
IMAGES_DIR = Path(f'src/data/blog/{SLUG}/images')

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def generate_image_openai(prompt, quality='medium', size='1024x1024'):
    """Generate an image via OpenAI gpt-image-1"""
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
        raise Exception(f'OpenAI API error {e.code}: {body[:300]}')


def upload_to_blob(local_path, blob_path):
    """Upload file to Vercel Blob via REST API"""
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
        raise Exception(f'Blob upload error {e.code}: {body[:300]}')


IMAGES = [
    {
        'file': 'hero.png',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'A split-screen visual comparison between cloud computing and on-premise server infrastructure. '
            'Left side shows a glowing cloud symbol with data flowing through digital networks and modern '
            'office workers using laptops and tablets wirelessly. Right side shows physical server racks '
            'in a data center with IT professionals managing hardware. Clean, professional, technology-forward '
            'business aesthetic with blue and white color palette. Wide landscape format.'
        ),
    },
    {
        'file': 'inline-1.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A professional business infographic-style visualization comparing total cost of ownership '
            'between cloud software subscription and on-premise server purchase. Show upward trending '
            'cost bars with dollar signs and a scale or balance graphic. Clean flat design with blue '
            'and green accent colors, modern business aesthetic, white background.'
        ),
    },
    {
        'file': 'inline-2.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A small business owner sitting at a modern desk, looking confident while working on a laptop. '
            'On the screen, there is a dashboard showing cloud software interface with uptime graphs and '
            'security shields. The office is bright, organized, with Southwest Florida coastal feel — '
            'natural light, plants, professional but approachable setting.'
        ),
    },
    {
        'file': 'inline-3.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'A clear decision-making flowchart illustration for small businesses choosing between cloud '
            'and on-premise software. Shows branching paths with checkmarks and decision boxes. '
            'Business icons for different industries — medical, retail, service businesses. '
            'Modern flat design style, professional blue and white color scheme.'
        ),
    },
]


def main():
    if not OPENAI_KEY:
        print('❌ OPENAI_API_KEY not set')
        sys.exit(1)
    if not BLOB_TOKEN:
        print('❌ BLOB_READ_WRITE_TOKEN not set')
        sys.exit(1)

    manifest = {}

    for img in IMAGES:
        local_path = IMAGES_DIR / img['file']
        blob_path = f'blog/{SLUG}/{img["file"]}'

        print(f'\n📸 Generating {img["file"]} (quality={img["quality"]}, size={img["size"]})...')
        try:
            img_data = generate_image_openai(img['prompt'], quality=img['quality'], size=img['size'])
            with open(local_path, 'wb') as f:
                f.write(img_data)
            print(f'   ✅ Saved to {local_path} ({len(img_data):,} bytes)')
        except Exception as e:
            print(f'   ❌ Generation failed: {e}')
            sys.exit(1)

        print(f'   ☁️  Uploading to Vercel Blob as {blob_path}...')
        try:
            blob_url = upload_to_blob(local_path, blob_path)
            manifest[blob_path] = blob_url
            print(f'   ✅ URL: {blob_url}')
        except Exception as e:
            print(f'   ❌ Upload failed: {e}')
            sys.exit(1)

    # Write manifest
    manifest_path = Path(f'src/data/blog/{SLUG}/blob-manifest.json')
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f'\n📄 Manifest written to {manifest_path}')

    print('\n✅ All done! URL mapping:')
    for k, v in manifest.items():
        print(f'  {k} → {v}')


if __name__ == '__main__':
    main()
