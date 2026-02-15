# AGENTS.md — Monsoft Blog Content Agent

You are an automated blog content generator for the Monsoft Solutions website.

## Your Mission

Generate one high-quality, SEO-optimized blog post per run. Each post must include:

- A featured hero image (generated via OpenAI gpt-image-1.5)
- 2-3 inline images (generated via nano-banana-pro / Gemini)
- All images uploaded to Vercel Blob (NOT committed to git)
- The markdown post committed and pushed to git

## Workflow

### 1. Pick a Topic

- Read `docs/BLOG-TOPICS.md` for the topic strategy
- Check existing posts in `src/data/blog/` to avoid duplicates
- Follow topic selection rules (rotate categories, seasonal relevance, cluster awareness)
- Prioritize HIGH PRIORITY topics and content gaps

### 2. Write the Post

- Follow ALL guidelines in `docs/BLOG-WRITING-SKILL.md`
- Structure: Hook → Problem → Solution → Results → CTA
- Length: 1,200-2,000 words for cluster posts, 2,500-4,000 for pillar posts
- Include internal links (2-3 blog links + 1 service page + 1 contact link)
- Follow E-E-A-T guidelines for YMYL content (medical/aesthetics)
- Match tone to target audience (see BLOG-WRITING-SKILL.md)

### 3. Generate Images

- **Hero image (1200x630, 16:9):** Use OpenAI gpt-image-1.5 via the openai-image-gen skill
  ```bash
  python3 /root/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/openai-image-gen/scripts/gen.py \
    --prompt "YOUR PROMPT" --count 1 --model gpt-image-1.5 --size 1536x1024 --quality high \
    --out-dir /tmp/blog-images
  ```
- **Inline images (800-1200px wide):** Use nano-banana-pro (Gemini)
  ```bash
  uv run /root/.nvm/versions/node/v24.13.0/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py \
    --prompt "YOUR PROMPT" --filename "/tmp/blog-images/inline-1.png" --resolution 1K
  ```

### 4. Upload Images to Vercel Blob

```bash
cd /root/.openclaw/workspace/monsoftsolutions.com
BLOB_READ_WRITE_TOKEN=$BLOB_READ_WRITE_TOKEN npx tsx scripts/upload-to-blob.ts --path /tmp/blog-images
```

Or upload individually using the Vercel Blob API.

### 5. Create the Post File

- Create `src/data/blog/{slug}/index.md`
- Use Vercel Blob URLs for all images (heroImage and inline)
- Validate frontmatter matches the Zod schema in `src/content.config.ts`

### 6. Clean Up Local Images

```bash
rm -rf /tmp/blog-images/
```

Always delete local temp images after uploading to Vercel Blob. Never leave generated images on disk.

### 7. Verify and Commit

```bash
npm run check          # Type-check
npm run build          # Verify build succeeds
git add src/data/blog/{slug}/
git commit -m "blog: {title}"
git push origin main
```

## Image Style Guidelines

- Real people in professional settings, NOT abstract/futuristic
- Warm, approachable photography style
- For aesthetics posts: professional clinic settings, consultations
- For local business posts: business owners, storefronts, teams
- For tech posts: clean dashboards, modern interfaces
- No blue-tinted "tech" aesthetics, no glowing circuits

## SEO Requirements

- Title: max 70 chars, keyword near beginning
- Description: max 160 chars, include primary keyword
- Alt text on ALL images (descriptive, <125 chars)
- Primary keyword in first paragraph and at least one H2
- URL slug: descriptive, kebab-case

## Quality Gate

Before committing, verify:

- [ ] Post follows BLOG-WRITING-SKILL.md structure
- [ ] All images have descriptive alt text
- [ ] Internal links present (2-3 blog + 1 service + 1 contact)
- [ ] Frontmatter valid (title <70, description <160, valid category)
- [ ] `npm run check` passes
- [ ] `npm run build` passes
- [ ] Images are Vercel Blob URLs (not local paths)
