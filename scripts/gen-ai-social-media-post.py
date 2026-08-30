#!/usr/bin/env python3
"""
Generate images for ai-social-media-content-creation-guide
Uses gpt-image-1 (high quality for hero, medium for inline)
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
SLUG = 'ai-social-media-content-creation-guide'
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
            'A small business owner or marketing professional working at a modern desk, '
            'surrounded by multiple screens showing AI-powered social media dashboards with '
            'auto-generated content, scheduling calendars, and analytics charts. '
            'Bright, vibrant social media posts visible on screens for platforms like Instagram, '
            'LinkedIn, and Facebook. Professional, clean modern office. Technology, creativity, '
            'and productivity theme. Photorealistic, warm lighting, no text overlays.'
        )
    },
    {
        'file': 'inline-1.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Flat design infographic showing the AI content creation workflow: '
            'a circular or linear diagram with icons for input (brand guidelines, topic), '
            'AI generation (robot brain icon), content output (social posts, captions, images), '
            'and scheduling/publishing. Clean professional tech design, blue and purple color palette. '
            'Modern business infographic style, no text needed.'
        )
    },
    {
        'file': 'inline-2.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Side-by-side comparison showing a stressed small business owner manually creating '
            'social media posts (left side, cluttered desk, handwritten notes) versus a relaxed '
            'entrepreneur reviewing AI-generated content on a laptop (right side, clean modern setup). '
            'Split composition, professional illustration style, warm and inviting atmosphere. '
            'No text overlays needed.'
        )
    },
    {
        'file': 'inline-3.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Analytics dashboard showing social media performance metrics — engagement charts, '
            'follower growth graphs, post performance heatmaps, and content calendar grid. '
            'Displayed on a modern laptop or tablet. Clean data visualization style, '
            'blue and green color palette, professional business analytics theme. '
            'No specific text needed, focus on visual data elements.'
        )
    },
]

print(f'🎨 Generating images for {SLUG}...\n')

blob_urls = {}

for i, img in enumerate(IMAGES, 1):
    filename = img['file']
    local_path = IMAGES_DIR / filename
    blob_key = f'blog/{SLUG}/{filename}'
    
    print(f'[{i}/{len(IMAGES)}] Generating {filename} (quality={img["quality"]}, size={img["size"]})...')
    img_bytes = generate_image_openai(img['prompt'], img['quality'], img['size'])
    local_path.write_bytes(img_bytes)
    print(f'      ✅ Generated {len(img_bytes):,} bytes → {local_path}')
    
    print(f'       Uploading to Blob: {blob_key}...')
    url = upload_to_blob(local_path, blob_key)
    blob_urls[filename] = url
    print(f'      ✅ Blob URL: {url}')
    print()

print('\n' + '='*60)
print('📋 Image URLs:')
for filename, url in blob_urls.items():
    print(f'  {filename}: {url}')
print('='*60)

manifest_path = IMAGES_DIR / 'blob-manifest.json'
manifest_path.write_text(json.dumps(blob_urls, indent=2))
print(f'\n💾 Manifest saved to {manifest_path}')
