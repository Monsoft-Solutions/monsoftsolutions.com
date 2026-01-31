# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monsoft Solutions marketing website - a fully static Astro 5 site for a B2B company serving plastic surgery clinics and local businesses. The site showcases AI automation, development services, and SaaS products.

**Live URL:** https://monsoftsolutions.com
**Deployment:** Vercel (primary), Docker/Dokploy (alternative)

## Commands

```bash
npm run dev          # Start dev server at localhost:4321
npm run build        # Build static site to ./dist/
npm run preview      # Preview production build locally
npm run check        # Type-check .astro files
npm run typecheck    # Type-check TypeScript files
npm run lint         # Run ESLint
npm run lint:fix     # Run ESLint with auto-fix
npm run format       # Format all files with Prettier
npm run format:check # Check formatting without changes
```

### Git Hooks

- **Pre-commit:** Runs lint-staged (ESLint + Prettier on staged files only)
- **Pre-push:** Runs `astro check`, `typecheck`, and `build` for full validation

## Architecture

### Tech Stack

- **Framework:** Astro 5.17 (static output, no SSR)
- **Styling:** Tailwind CSS v4 via `@tailwindcss/vite` plugin
- **Animations:** GSAP for complex sequences, CSS/Intersection Observer for scroll reveals
- **Content:** Astro Content Collections with Zod validation
- **Integrations:** n8n webhooks (contact form), Vercel Blob (image storage)

### Key Directories

```
src/
├── pages/           # File-based routing (.astro files)
├── components/      # Reusable Astro components
├── layouts/         # Layout.astro (main), BlogPost.astro
├── data/blog/       # Blog posts as markdown with frontmatter
├── styles/global.css # Tailwind imports + custom utilities
└── content.config.ts # Blog collection schema
```

### Blog Content Structure

Posts live in `src/data/blog/{slug}/index.md` with images stored on Vercel Blob (not locally). Required frontmatter:

- `title` (max 70 chars), `description` (max 160 chars), `pubDate`, `category`

Categories: AI & Automation, Web Development, Business Growth, Technology Trends, Case Studies, Guides & Tutorials, Local Business, Medical & Aesthetics

### Environment Variables

```bash
PUBLIC_N8N_WEBHOOK_URL  # Contact form POST endpoint (client-side)
BLOB_READ_WRITE_TOKEN   # Vercel Blob for image uploads
```

## Patterns

### Animation System

- `.reveal` class + Intersection Observer for scroll-triggered animations
- `data-animate="fade-up"` and `data-delay="0.2"` attributes for orchestration
- GSAP timelines in Hero component for complex sequences

### Component Structure

Astro components use scoped `<style>` tags and `<script>` blocks for client-side JS. Responsive breakpoints: 1024px, 768px, 640px.

### Image Guidelines (from HOMEPAGE_IMPROVEMENT_PLAN.md)

- Use real people in professional settings, not futuristic/abstract tech imagery
- Target audience: aesthetic clinic professionals, local business owners
- Warm, approachable photography over blue-tinted "tech" aesthetics

## Sitemap Configuration

Defined in `astro.config.mjs` with priority/frequency hints:

- Homepage: priority 1.0, daily
- Services pages: priority 0.9, weekly
- About/Contact: priority 0.8, monthly
