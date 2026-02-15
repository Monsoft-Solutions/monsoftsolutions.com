# Website Style & UX Improvement Plan

> Generated: 2026-02-03 from visual audit (desktop + mobile screenshots) + source code analysis + audience profile review

---

## Executive Summary

The site has a **solid foundation** — clean Astro 5 static architecture, decent typography, and professional content structure. But the current execution has **critical mobile issues, conversion blockers, and visual identity problems** that undermine trust for our target audience (plastic surgery clinics + local small businesses in SW Florida).

**The site looks like a generic SaaS template. It should feel like a trusted partner who understands medical aesthetics and local business.**

---

## 🔴 Critical Issues (Fix Immediately)

### 1. Mobile Layout is Broken

**Problem:** Text overflows viewport on 390px width. Eyebrow text truncates ("AI-POWERED GROWTH FOR CLINICS & BUSIN..."), headlines clip, and body copy gets cut off. No CTA button is visible above the fold on mobile. This is a **conversion-killing bug** for the 60%+ of visitors on phones.

**Root Cause:** Hero section's `container-wide` padding + hero grid layout don't collapse cleanly at 390px. The eyebrow text with `text-transform: uppercase` + long text string overflows.

**Fix — `Hero.astro`:**

```css
/* Add/update in @media (max-width: 640px) block */
@media (max-width: 640px) {
  .hero {
    padding-top: 5rem;
    padding-bottom: 2rem;
  }

  .hero .container-wide {
    padding-inline: 1.25rem;
  }

  .eyebrow {
    font-size: 0.6875rem; /* Smaller to prevent overflow */
    letter-spacing: 0.03em; /* Tighter tracking */
    word-break: break-word;
  }

  .hero-title {
    font-size: clamp(1.75rem, 7vw, 2.25rem);
  }

  .hero-subtitle {
    font-size: 0.9375rem;
  }

  .hero-ctas {
    flex-direction: column;
    align-items: stretch;
    margin-bottom: 2rem;
  }

  .hero-ctas .btn {
    justify-content: center;
    padding: 1rem 1.5rem;
    font-size: 1rem;
  }

  .trust-indicators {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }

  .trust-item {
    flex: 1;
    min-width: 80px;
    align-items: center;
    text-align: center;
  }

  .trust-number,
  .trust-suffix {
    font-size: 1.375rem;
  }
}
```

**Fix — `global.css` container:**

```css
.container-wide {
  width: 100%;
  max-width: 1440px;
  margin-inline: auto;
  padding-inline: clamp(1.25rem, 5vw, 4rem); /* was 1.5rem minimum — too tight on 390px */
  box-sizing: border-box;
}
```

**Priority:** 🔴 P0 — Fix today
**Effort:** 1-2 hours

---

### 2. Stats Show "0%" on Page Load (Animation Bug)

**Problem:** The hero trust indicators show `0%` for all three metrics. The GSAP counter animation (`data-count`) only fires after DOMContentLoaded, but on slower connections or when GSAP loads async, visitors see zeros. This **destroys credibility** — literally showing "0% Traffic Increase."

**Root Cause:** `innerHTML` starts at `0` and GSAP animates to target, but if the animation hasn't triggered by the time a user sees it, they see zeros. Also, the counter starts counting at `delay: 0.8` which means for nearly a second the numbers show 0.

**Fix — `Hero.astro` markup:**

```html
<!-- Change initial display from 0 to the actual value as fallback -->
<span class="trust-number" data-count="340">340</span>
<span class="trust-suffix">%</span>
<span class="trust-label">Traffic Increase</span>
```

And in the GSAP script, set initial value to 0 only when animation starts:

```javascript
countElements.forEach((el) => {
  const target = parseInt(el.dataset.count || '0');
  // Only reset to 0 when we know GSAP is ready
  el.innerHTML = '0';
  gsap.to(el, {
    innerHTML: target,
    duration: 2,
    delay: 0.3, // Reduced from 0.8
    snap: { innerHTML: 1 },
    ease: 'power2.out',
    onUpdate: function () {
      el.innerHTML = Math.round(parseFloat(el.innerHTML)).toLocaleString();
    },
  });
});
```

**Priority:** 🔴 P0 — Fix today
**Effort:** 30 minutes

---

### 3. Images Have `opacity: 0` Default + No Fallback

**Problem:** In `global.css`, ALL images default to `opacity: 0` and only become visible when `.loaded` class is added via JS. If the image load event fires before the JS runs (cached images, fast connections), images stay invisible. The headless screenshot confirmed the hero image renders fine, but this is fragile.

**Fix — `global.css`:**

```css
/* Replace the current img rule */
img {
  opacity: 1; /* Safe default — always visible */
}

img[data-lazy] {
  opacity: 0;
  transition: opacity 0.5s ease;
}

img[data-lazy].loaded {
  opacity: 1;
}
```

Only apply the fade-in to explicitly opted-in images, not globally.

**Priority:** 🔴 P0
**Effort:** 30 minutes

---

## 🟠 High-Priority Improvements (This Week)

### 4. Add a Social Proof / Logo Bar

**Problem:** Zero social proof between the hero and services sections. No client logos, no "trusted by" bar, no third-party validation. For our skeptical audience (clinic owners burned by past agencies, small business owners cautious with budget), this is a big gap.

**Implementation — New component `SocialProof.astro`:**

```astro
---
// Social proof bar after Hero
---

<section class="social-proof">
  <div class="container-wide">
    <p class="proof-label">Trusted by clinics and businesses across Florida</p>
    <div class="proof-logos">
      <!-- Client logos here - use grayscale with hover color -->
      <img src="/images/logos/alluring.svg" alt="Alluring Plastic Surgery" />
      <!-- Add more as available -->
    </div>
    <div class="proof-stats">
      <span>🏆 340% avg. traffic increase</span>
      <span class="divider">·</span>
      <span>⭐ 4.9/5 client satisfaction</span>
      <span class="divider">·</span>
      <span>🕐 24/7 automated support</span>
    </div>
  </div>
</section>
```

Place in `index.astro` between `<Hero />` and `<Services />`.

**Priority:** 🟠 P1
**Effort:** 2-3 hours

---

### 5. Warm Up the Color Palette

**Problem:** The palette is pure neutral (grays + one blue accent). It reads as cold, generic SaaS — not warm/trustworthy for medical professionals or local business owners. The CLAUDE.md even notes: "Use real people, warm approachable photography over blue-tinted tech aesthetics" — but the CSS contradicts this.

**Implementation — Update CSS custom properties in `global.css`:**

```css
:root {
  /* Keep the neutrals but warm them slightly */
  --color-white: #fafaf8; /* was #fafafa — slight warm shift */
  --color-gray-50: #f7f6f4; /* warmer gray */

  /* Primary accent: shift from cold blue to a warmer, more trustworthy blue */
  --color-accent: #1e56cc; /* deeper, slightly warmer blue */
  --color-accent-light: #3370e0;

  /* NEW: Secondary warm accent for highlights and success states */
  --color-warm: #c47a3a; /* warm amber for premium/medical feel */
  --color-success: #1a8a5c; /* professional green, not neon */
}
```

Use `--color-warm` for:

- Pricing highlights
- "Premium" / "Most Popular" badges
- Testimonial quote marks
- Hover states on CTAs (subtle warm glow)

**Priority:** 🟠 P1
**Effort:** 2-3 hours (CSS variable changes cascade everywhere)

---

### 6. Improve CTA Hierarchy and Copy

**Problem:** The primary CTA says "See How It Works" — this is vague and passive. For a B2B audience, this doesn't create urgency. The secondary CTA "View Case Study" is actually higher-intent but gets less visual priority.

**Fix — Hero CTAs:**

```html
<!-- Swap the emphasis -->
<a href="/contact" class="btn btn-primary">
  Book a Free Strategy Call
  <svg>...</svg>
</a>
<a href="/services/aesthetics" class="btn btn-secondary"> See Our Results → </a>
```

**Fix — Bottom CTA section copy:**

Current: "Ready to build something intelligent?"
Better: "Ready to grow? Let's talk."

Current: "No sales pitch—just a conversation about what's possible."
Better: "15 minutes. No commitment. Just a clear plan for your business."

**Priority:** 🟠 P1
**Effort:** 1 hour

---

### 7. Products Section: Replace Abstract Shapes with Real Screenshots

**Problem:** The products visual area shows morphing colored blobs. This communicates nothing about what the products actually do. Screenshots/mockups would build 10x more credibility.

**Implementation:**

1. Take actual screenshots of Adfluens and Praxis Notes dashboards
2. Create device mockups (laptop frame or browser window)
3. For Loquent (coming soon), create a realistic UI mockup

Replace the `.product-visual` div with:

```html
<div class="product-visual">
  <picture>
    <source srcset="/images/products/adfluens-dashboard.webp" type="image/webp" />
    <img
      src="/images/products/adfluens-dashboard.png"
      alt="Adfluens dashboard showing social media management"
      loading="lazy"
    />
  </picture>
</div>
```

Style with a subtle device frame:

```css
.product-visual {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--color-gray-100);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.product-visual img {
  width: 100%;
  height: auto;
  display: block;
}
```

**Priority:** 🟠 P1
**Effort:** 3-4 hours (screenshot + optimize + implement)

---

## 🟡 Medium-Priority Improvements (This Sprint)

### 8. Add a Sticky Mobile CTA

**Problem:** On mobile, the main CTA scrolls away quickly and there's no persistent action available. Clinic owners browsing on their phone between patients need a frictionless way to take action at any scroll position.

**Implementation — `StickyCTA.astro` already exists!** Check if it's being used:

```astro
<!-- In index.astro, add: -->
<StickyCTA />
```

If it needs creation, implement a bottom-fixed bar (mobile only):

```css
.sticky-cta {
  display: none;
}

@media (max-width: 768px) {
  .sticky-cta {
    display: flex;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 0.75rem 1rem;
    background: rgba(250, 250, 248, 0.95);
    backdrop-filter: blur(12px);
    border-top: 1px solid var(--color-gray-100);
    z-index: 90;
    justify-content: center;
  }

  .sticky-cta a {
    flex: 1;
    max-width: 400px;
  }
}
```

**Priority:** 🟡 P2
**Effort:** 1-2 hours

---

### 9. Typography: Add a Display Font

**Problem:** Inter is used for both headings and body. While clean, it lacks personality and distinction between headline hierarchy and body text. Every SaaS site uses Inter — it's invisible.

**Recommendation:** Keep Inter for body, add a display font for `h1`/`h2`:

- **Option A:** `"DM Serif Display"` — Classic, medical/premium feel
- **Option B:** `"Fraunces"` — Warm, distinctive, modern serif
- **Option C:** `"Plus Jakarta Sans"` — Geometric, slightly more personality than Inter

Implementation (Option A — strongest for medical audience):

```css
:root {
  --font-display: 'DM Serif Display', Georgia, serif;
  --font-sans: 'Inter', system-ui, sans-serif;
}
```

Add to `Layout.astro` `<head>`:

```html
<link
  href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&display=swap"
  rel="stylesheet"
/>
```

This creates instant visual distinction: serif headlines (trust, premium) + sans body (clean, modern).

**Priority:** 🟡 P2
**Effort:** 2 hours

---

### 10. Improve the Industries Section with Stronger Visual Differentiation

**Problem:** Both industry cards look identical in structure. For our two very different audiences (high-ticket medical vs. local SMB), the visual treatment should immediately signal "this is for you."

**Implementation:**

- **Aesthetics card:** Add a subtle gradient overlay in warm tones (gold/amber). Include a small "🏥 Healthcare Specialized" badge.
- **Local Business card:** Add a subtle green/earth tone overlay. Include "📍 Southwest Florida" badge.

```css
.industry-card:first-child {
  border-top: 3px solid var(--color-warm, #c47a3a);
}

.industry-card:last-child {
  border-top: 3px solid var(--color-success, #1a8a5c);
}
```

**Priority:** 🟡 P2
**Effort:** 1-2 hours

---

### 11. Add Micro-Interactions and Polish

**Problem:** Hover states exist but are basic. The site lacks the small delightful interactions that signal quality craftsmanship — important for a company selling "premium" tech services.

**Additions:**

```css
/* Magnetic button effect for primary CTAs */
.btn-primary {
  transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow:
    0 4px 12px rgba(30, 86, 204, 0.3),
    0 0 0 1px rgba(30, 86, 204, 0.1);
}

.btn-primary:active {
  transform: translateY(0);
}

/* Card hover: subtle border glow */
.service-card:hover {
  border: 1px solid rgba(30, 86, 204, 0.15);
}

/* Link arrows that slide */
.service-link svg,
.industry-cta svg,
.product-link svg {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

**Priority:** 🟡 P2
**Effort:** 2-3 hours

---

## 🟢 Nice-to-Have (Next Sprint)

### 12. Add a Video Testimonial or Background Loop

Short 15-30s loop of: clinic environment → happy patient → dashboard results.
Place as hero background or as a dedicated section. Video converts 86% better than static for service businesses.

### 13. Add an FAQ Accordion on Homepage

Target audience questions:

- "How is this different from a regular marketing agency?"
- "Do I need to be tech-savvy?"
- "What if I already have a website?"
- "How quickly will I see results?"

### 14. Add Schema.org LocalBusiness Markup

Already has Organization schema. Add LocalBusiness + Service schemas for better local SEO rich results.

### 15. Performance: Preload Hero Image + Font

```html
<link rel="preload" href="/images/home/hero-main.webp" as="image" type="image/webp" />
<link
  rel="preload"
  href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600"
  as="style"
/>
```

### 16. Add a "How It Works" 3-Step Section

Simple process visualization:

1. **Discovery Call** (15 min, free) → 2. **Custom Strategy** (we build the plan) → 3. **Launch & Grow** (results in weeks, not months)

This reduces anxiety for the skeptical local business owner.

---

## Implementation Roadmap

| Phase                   | Items                                                          | Effort     | Timeline    |
| ----------------------- | -------------------------------------------------------------- | ---------- | ----------- |
| **Phase 0: Hotfix**     | #1 Mobile layout, #2 Stats bug, #3 Image opacity               | 2-3 hours  | Today       |
| **Phase 1: Conversion** | #4 Social proof, #6 CTA copy, #8 Sticky CTA                    | 4-5 hours  | This week   |
| **Phase 2: Identity**   | #5 Color warmth, #9 Display font, #10 Industry differentiation | 5-6 hours  | This week   |
| **Phase 3: Trust**      | #7 Product screenshots, #11 Micro-interactions                 | 5-6 hours  | Next week   |
| **Phase 4: Delight**    | #12-16 Video, FAQ, schema, perf, process section               | 8-10 hours | Next sprint |

---

## Success Metrics

After implementation, monitor:

| Metric                   | Current (est.) | Target |
| ------------------------ | -------------- | ------ |
| Mobile bounce rate       | ~65%           | <45%   |
| Time on page (homepage)  | ~30s           | >60s   |
| CTA click-through        | ~2%            | >5%    |
| Contact form submissions | baseline       | +40%   |
| Lighthouse mobile score  | ~75            | >90    |

---

## Design Principles (Going Forward)

1. **Warm over cold** — We're a partner, not a vendor. The design should feel like a handshake, not a pitch deck.
2. **Specific over generic** — Every section should make clinic owners or local business owners think "they get me."
3. **Proof over promise** — Show numbers, screenshots, and testimonials before making claims.
4. **Mobile-first, always** — Our audience checks between patients and between jobs. Mobile is the default.
5. **Fast over fancy** — Sub-2s load times beat flashy animations every time.
