# Images Documentation

This document covers how to use images in the Monsoft Solutions website, with a focus on blog posts.

## Overview

Astro provides built-in image optimization through the `<Image />` component. Images are automatically:
- Optimized and compressed
- Converted to modern formats (WebP/AVIF)
- Lazy-loaded for performance
- Sized to prevent layout shift

## Image Locations

### Local Images (Recommended)

Store images in `src/` for automatic optimization:

```
src/
├── assets/
│   └── blog/           # Shared blog images
│       └── hero-default.jpg
├── data/
│   └── blog/
│       ├── my-post.md
│       └── images/     # Post-specific images
│           ├── hero.jpg
│           └── diagram.png
```

### Public Images (No Optimization)

Images in `public/` are served as-is without processing:

```
public/
└── images/
    └── og-default.jpg  # For external URLs, social sharing
```

## Blog Post Images

### Hero Image (Featured Image)

The hero image appears at the top of the blog post and is used for:
- Visual header on the post page
- Social sharing previews (Open Graph)
- Blog listing cards (if implemented)

**Frontmatter:**
```yaml
---
title: "My Post Title"
heroImage: "./images/hero.jpg"      # Relative to the .md file
heroImageAlt: "Description of image for accessibility"
---
```

**Specifications:**
| Property | Recommendation |
|----------|---------------|
| Dimensions | 1200×630px (16:9 for social) |
| Format | JPG or PNG (WebP auto-generated) |
| File size | Under 500KB before optimization |
| Aspect ratio | 16:9 preferred |

### Inline Images

Add images within your markdown content:

```markdown
## My Section

Here's an explanation with a visual:

![Diagram showing the automation flow](./images/automation-flow.png)

More text continues here...
```

**Best Practices:**
- Use descriptive alt text for accessibility
- Place images after introducing the concept
- Keep file sizes reasonable (under 300KB each)
- Use PNG for diagrams/screenshots, JPG for photos

### Image Placement Guidelines

For optimal reading experience:
1. **Hero image**: Always at the top (handled by layout)
2. **Section images**: After the section heading, before detailed text
3. **Supporting diagrams**: Immediately after the concept they illustrate
4. **Screenshots**: Inline with step-by-step instructions

## Using Images in Astro Components

### The Image Component

```astro
---
import { Image } from 'astro:assets';
import myImage from '../assets/my-image.jpg';
---

<Image 
  src={myImage} 
  alt="Description of the image"
  width={800}
  height={450}
/>
```

### Responsive Images

For responsive behavior, use `widths` and `sizes`:

```astro
<Image 
  src={heroImage} 
  alt="Hero image"
  widths={[640, 960, 1200, 1600]}
  sizes="(max-width: 768px) 100vw, 960px"
/>
```

### The Picture Component

For multiple formats with fallback:

```astro
---
import { Picture } from 'astro:assets';
import myImage from '../assets/my-image.jpg';
---

<Picture 
  src={myImage}
  formats={['avif', 'webp']}
  alt="Description"
/>
```

## Image Optimization

### Automatic Optimization

Astro automatically:
- Converts to WebP/AVIF when supported
- Generates multiple sizes for srcset
- Adds width/height to prevent CLS
- Lazy loads below-the-fold images

### Manual Optimization Tips

Before adding images:
1. Resize to maximum display size (no larger than 1600px wide)
2. Compress using tools like:
   - [Squoosh](https://squoosh.app/) (web-based)
   - [ImageOptim](https://imageoptim.com/) (Mac)
   - `sharp` CLI for batch processing
3. Use appropriate format:
   - **JPG**: Photos, complex images
   - **PNG**: Screenshots, diagrams, transparency
   - **SVG**: Icons, logos, simple graphics

## Accessibility

### Alt Text Guidelines

**Good alt text:**
- Describes the image content and purpose
- Is concise but complete (typically under 125 characters)
- Doesn't start with "Image of..." or "Picture of..."

**Examples:**
```markdown
<!-- Good -->
![Dashboard showing 40% increase in monthly revenue](./dashboard.png)

<!-- Bad -->
![Dashboard](./dashboard.png)
![Image of a dashboard](./dashboard.png)
```

**Decorative images:**
```markdown
<!-- For purely decorative images, use empty alt -->
![](./decorative-pattern.png)
```

## Remote Images

For external images, configure allowed domains in `astro.config.mjs`:

```javascript
export default defineConfig({
  image: {
    domains: ['images.unsplash.com', 'cdn.example.com'],
  }
});
```

Then use the full URL:
```astro
<Image 
  src="https://images.unsplash.com/photo-123" 
  alt="Description"
  width={800}
  height={600}
/>
```

## Common Issues

### Image Not Found
- Check the path is relative to the `.md` file location
- Ensure the file exists and filename matches exactly (case-sensitive)

### Image Not Optimized
- Verify image is in `src/`, not `public/`
- Check that the import path is correct

### Layout Shift
- Always include width and height, or use the Image component
- Use aspect-ratio CSS for dynamic content

## Resources

- [Astro Images Guide](https://docs.astro.build/en/guides/images/)
- [WebP Converter](https://squoosh.app/)
- [Alt Text Guidelines](https://www.w3.org/WAI/tutorials/images/)
