#!/usr/bin/env python3
"""
Generate images for ai-customer-experience-personalization-guide
Hero: gpt-image-1.5 high quality 1536x1024
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
SLUG = 'ai-customer-experience-personalization-guide'
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
        'model': 'gpt-image-1.5',
        'quality': 'high',
        'size': '1536x1024',
        'prompt': (
            'A warm and professional small business scene: a business owner at a modern desk '
            'surrounded by multiple screens displaying personalized customer profiles, tailored '
            'email previews, and a friendly chat interface. Each screen shows a different customer '
            'receiving a customized message — one about a new appointment offer, another about a '
            'loyalty reward, another with a personalized product recommendation. Natural light fills '
            'the space, plants and warm wood tones create an inviting aesthetic. Photorealistic '
            'commercial photography style. No visible text or logos.'
        ),
    },
    {
        'filename': 'inline-1.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Clean flat design illustration showing multiple personalized customer journey paths: '
            'a central hub with an AI brain icon, with three distinct colored pathways flowing '
            'outward — one teal path going to a "new visitor" customer icon, one gold path to a '
            '"returning customer" icon, one purple path to a "VIP loyal customer" icon. Each '
            'customer receives a different personalized icon (gift box, calendar, star). '
            'Professional modern illustration style with a white background. No text labels.'
        ),
    },
    {
        'filename': 'inline-2.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Split-panel illustration comparing mass marketing vs AI personalization: '
            'Left panel in cool grey tones shows identical generic envelopes/messages going to '
            'a group of identical grey silhouette people; right panel in warm teal and gold shows '
            'uniquely decorated personalized message cards going to individual people with distinct '
            'characteristics — different ages, styles, interests shown through icons. Right panel '
            'has a warm glow effect. Clean modern flat design. No text.'
        ),
    },
    {
        'filename': 'inline-3.png',
        'model': 'gpt-image-1',
        'quality': 'medium',
        'size': '1024x1024',
        'prompt': (
            'Professional data dashboard illustration showing customer segmentation and personalization '
            'analytics: a clean UI with customer segment cards (icons showing "First Visit", '
            '"High Value", "At Risk", "Loyal"), performance bar charts, email open rate graphs, '
            'and conversion funnel visualization. Purple, blue, and white color scheme, modern SaaS '
            'dashboard aesthetic. Small AI sparkle/star icons near the metrics to indicate AI-driven '
            'insights. No readable text.'
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
        print(f'  ERROR generating {img["filename"]}: {e}')
        # Fallback to gpt-image-1 if gpt-image-1.5 fails
        if img['model'] == 'gpt-image-1.5':
            print(f'  Falling back to gpt-image-1 high...')
            try:
                img_bytes = generate_image_openai(
                    prompt=img['prompt'],
                    model='gpt-image-1',
                    quality='high',
                    size=img['size'],
                )
                local_path = save_image(img_bytes, img['filename'])
                blob_path = f'blog/{SLUG}/{img["filename"]}'
                print(f'  Uploading to Blob: {blob_path}...')
                blob_url = upload_to_blob(local_path, blob_path)
                blob_urls[img['filename']] = blob_url
                print(f'  Fallback Blob URL: {blob_url}')
            except Exception as e2:
                print(f'  Fallback also failed: {e2}')

print('\n=== BLOB URLs ===')
for fname, url in blob_urls.items():
    print(f'{fname}: {url}')
