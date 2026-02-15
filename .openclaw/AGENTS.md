# AGENTS.md — Monsoft Web Agent

You are a specialized web development agent for the Monsoft Solutions marketing website.

## Project

- **Repo:** Monsoft-Solutions/monsoftsolutions.com
- **Stack:** Astro 5, Tailwind CSS v4, GSAP, TypeScript
- **Deployment:** Vercel (primary), Docker/Dokploy (alt)
- **Live:** https://monsoftsolutions.com

## Your Job

Build, improve, and maintain the Monsoft Solutions website. You understand:

- Astro 5 components, layouts, content collections
- Tailwind CSS v4 utility-first styling
- SEO best practices (meta, structured data, sitemap)
- The blog system (markdown + Zod frontmatter validation)
- GSAP animations and Intersection Observer patterns

## Key Files

- `CLAUDE.md` — Project commands and architecture
- `HOMEPAGE_IMPROVEMENT_PLAN.md` — Pending homepage improvements
- `SERVICES_IMPROVEMENT_PLAN.md` — Pending service page improvements
- `docs/` — Blog system docs, image guidelines, competition research

## Commands

```bash
npm run dev          # Dev server (localhost:4321)
npm run build        # Build static site
npm run preview      # Preview production build
npm run check        # Type-check .astro files
npm run lint:fix     # Lint + auto-fix
npm run format       # Format all files
```

## Conventions

- Components in `src/components/`, pages in `src/pages/`
- Blog posts in `src/data/blog/{slug}/index.md`
- Images on Vercel Blob (not local)
- Use `.reveal` class + `data-animate` for scroll animations
- Responsive breakpoints: 1024px, 768px, 640px
- Always run `npm run check` and `npm run build` before committing

## Image Guidelines

- Real people in professional settings, NOT abstract/futuristic tech
- Warm, approachable photography
- Target audience: aesthetic clinic professionals, local business owners
- Optimize for web (<200KB), use WebP with fallback

## Git

- Main branch: `main`
- Create feature branches for changes
- Run pre-push checks before pushing (check + typecheck + build)
