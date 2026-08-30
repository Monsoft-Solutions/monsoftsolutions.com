#!/usr/bin/env python3
"""
Generate images for seasonal-promotions-aesthetic-practices-guide
Uses gpt-image-1 (high quality for hero, medium for inline)
Then uploads to Vercel Blob
"""

import os
import json
import base64
import urllib.request
import urllib.parse
import subprocess
import sys
from pathlib import Path

OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')
SLUG = 'seasonal-promotions-aesthetic-practices-guide'
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
    resp = urllib.request.urlopen(req, timeout=120)
    data = json.loads(resp.read())
    
    # gpt-image-1 returns b64_json
    img_b64 = data['data'][0]['b64_json']
    return base64.b64decode(img_b64)


def upload_to_blob(local_path, blob_path):
    """Upload file to Vercel Blob via REST API"""
    with open(local_path, 'rb') as f:
        file_data = f.read()
    
    content_type = 'image/png'
    
    # Use Vercel Blob REST API PUT
    url = f'https://blob.vercel-storage.com/{blob_path}'
    headers = {
        'Authorization': f'Bearer {BLOB_TOKEN}',
        'Content-Type': content_type,
        'x-content-type': content_type,
        'x-add-random-suffix': 'false',
        'x-cache-control-max-age': '31536000',
    }
    
    req = urllib.request.Request(url, data=file_data, headers=headers, method='PUT')
    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read())
    return result.get('url', '')


# Image prompts
IMAGES = [
    {
        'file': 'hero.png',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'Elegant med spa reception area beautifully decorated for a seasonal promotion. '
            'A stylish display shows summer skincare specials and limited-time offers. '
            'Soft warm lighting, luxury aesthetic clinic environment, modern clean design. '
            'A welcoming esthetician in white coat stands ready. '
            'Promotional signage and a tablet showing appointment booking system. '
            'Professional medical spa atmosphere, no text overlays.'
        )
    },
    {
        'file': 'inline-1.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Flat design infographic showing a 4-season promotion calendar for an aesthetic practice. '
            'Spring, summer, fall, winter sections with icons for different treatments. '
            'Professional blue, teal, and gold color palette. '
            'Clean modern business diagram style, no text labels needed.'
        )
    },
    {
        'file': 'inline-2.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Split image showing before-and-after seasonal email campaigns for a med spa. '
            'Left side: disorganized generic promotions on laptop screen. '
            'Right side: elegant branded seasonal promotion displayed on phone. '
            'Clean design, professional marketing aesthetic, focused on email campaigns. '
            'Luxury spa color palette, soft lighting.'
        )
    },
    {
        'file': 'inline-3.png',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Happy med spa patient reviewing a seasonal loyalty rewards offer on a tablet. '
            'Modern aesthetic clinic waiting area, patient smiling at promotional offer. '
            'Professional medical spa environment, warm and welcoming atmosphere. '
            'Summer seasonal theme with subtle skin treatment visuals in background. '
            'No text overlays, photorealistic style.'
        )
    },
]

print('🎨 Generating images for seasonal-promotions-aesthetic-practices-guide...\n')

blob_urls = {}

for img in IMAGES:
    filename = img['file']
    local_path = IMAGES_DIR / filename
    blob_key = f'blog/{SLUG}/{filename}'
    
    print(f'[1/2] Generating {filename} (quality={img["quality"]}, size={img["size"]})...')
    try:
        img_bytes = generate_image_openai(img['prompt'], img['quality'], img['size'])
        local_path.write_bytes(img_bytes)
        print(f'      ✅ Generated {len(img_bytes):,} bytes → {local_path}')
    except Exception as e:
        print(f'      ❌ Generation failed: {e}')
        sys.exit(1)
    
    print(f'[2/2] Uploading to Blob: {blob_key}...')
    try:
        url = upload_to_blob(local_path, blob_key)
        blob_urls[filename] = url
        print(f'      ✅ Blob URL: {url}')
    except Exception as e:
        print(f'      ❌ Upload failed: {e}')
        # Try the npm script as fallback
        print(f'      ⚠️  Will use npm upload script later')
        blob_urls[filename] = None
    
    print()

# Print summary
print('\n' + '='*60)
print('📋 Image URLs:')
for filename, url in blob_urls.items():
    print(f'  {filename}: {url}')
print('='*60)

# Save manifest
manifest_path = IMAGES_DIR / 'blob-manifest.json'
manifest_path.write_text(json.dumps(blob_urls, indent=2))
print(f'\n💾 Manifest saved to {manifest_path}')
