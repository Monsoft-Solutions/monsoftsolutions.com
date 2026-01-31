# Blog Writing Skill

This document defines the guidelines for creating SEO-optimized, engaging blog posts for Monsoft Solutions.

## Blog Post Structure

Every blog post should follow this structure:

```
src/data/blog/
├── post-slug/
│   ├── index.md          # The blog post content
│   └── images/           # Post-specific images
│       ├── hero.jpg      # Featured image (1200x630)
│       ├── inline-1.jpg  # First inline image
│       ├── inline-2.jpg  # Second inline image
│       └── inline-3.jpg  # Third inline image (optional)
```

## Frontmatter Template

```yaml
---
title: "Your Compelling Title Here"           # Max 70 chars
description: "A compelling meta description"  # Max 160 chars
pubDate: 2026-01-31
author: "Monsoft Solutions"
category: "AI & Automation"                   # See allowed categories
tags: ["AI", "Automation", "Business"]        # 3-5 relevant tags
featured: false                                # true for hero placement
draft: false                                   # true to hide from prod
readingTime: "7 min read"
heroImage: "./images/hero.jpg"
heroImageAlt: "Descriptive alt text for the hero image"
---
```

### Allowed Categories
- AI & Automation
- Web Development
- Business Growth
- Technology Trends
- Case Studies
- Guides & Tutorials

## Title Guidelines

### SEO-Optimized Titles
- Include primary keyword near the beginning
- 50-70 characters (displays fully in search results)
- Use power words: "Ultimate", "Complete", "Proven", "Essential"
- Include numbers when relevant: "7 Ways...", "2026 Guide"

**Formula Options:**
1. `How to [Achieve Result] with [Method/Tool]`
2. `[Number] [Adjective] Ways to [Achieve Result]`
3. `The Complete Guide to [Topic] in [Year]`
4. `[Topic]: What [Audience] Needs to Know`
5. `Why [Common Belief] Is Wrong (And What to Do Instead)`

**Examples:**
- ✅ "How AI Automation Can Save Your Small Business 20+ Hours Per Week"
- ✅ "5 SEO Strategies That Actually Work for Local Businesses in 2026"
- ❌ "AI and Automation" (too vague)
- ❌ "A Comprehensive and Detailed Analysis of..." (too long)

## Description Guidelines

The meta description appears in search results and social shares.

- 140-160 characters
- Include primary keyword naturally
- Clear value proposition
- Call-to-action implied

**Examples:**
- ✅ "Discover practical AI automation strategies that small businesses are using right now to eliminate repetitive tasks and focus on growth."
- ❌ "This blog post discusses AI automation." (no value proposition)

## Content Structure

### Opening (First 100 words)
- Hook the reader immediately
- State the problem or opportunity
- Preview the value they'll get
- Include primary keyword naturally

**Opening Patterns:**
1. **Problem-Agitate-Solution**: State problem → amplify pain → hint at solution
2. **Surprising Statistic**: Lead with a compelling data point
3. **Direct Address**: "If you're [audience], you know [pain point]"
4. **Contrarian**: Challenge conventional wisdom

### Body Structure

Use H2 headings for main sections, H3 for subsections:

```markdown
## Main Topic 1
Introduction to this section...

![Relevant image with descriptive alt text](./images/inline-1.jpg)

### Subtopic 1.1
Details...

### Subtopic 1.2
More details...

## Main Topic 2
Continue the narrative...

![Another relevant image](./images/inline-2.jpg)

## Main Topic 3
Final major section...
```

### Content Guidelines

**Paragraph Length:**
- 2-4 sentences per paragraph
- One idea per paragraph
- Short paragraphs for mobile readability

**Sentence Structure:**
- Vary sentence length
- Active voice preferred
- Avoid jargon without explanation

**Engagement Elements:**
- Use bullet points for lists (3-7 items)
- Include numbered steps for processes
- Add blockquotes for emphasis or expert quotes
- Bold key terms and takeaways

### Closing
- Summarize key points
- Clear call-to-action
- Link to related content or contact page

## Image Requirements

### Hero Image (Required)
- **Size**: 1200×630px (16:9 ratio)
- **Purpose**: Sets the tone, used in social sharing
- **Style**: Professional, relevant to topic
- **File**: `./images/hero.jpg`

### Inline Images (2-3 per post)
- **Size**: 800-1200px wide
- **Purpose**: Illustrate concepts, break up text
- **Placement**: After introducing a concept, before detailed explanation
- **Types**:
  - Diagrams and flowcharts
  - Screenshots with annotations
  - Data visualizations
  - Relevant stock photography

### Image Alt Text
Write alt text that:
- Describes what's in the image
- Includes relevant keywords naturally
- Provides context for screen readers
- Is under 125 characters

**Examples:**
- ✅ "Dashboard showing automated email workflow with 4 connected steps"
- ✅ "Bar chart comparing manual vs automated task completion times"
- ❌ "Image" or "Screenshot"
- ❌ "AI automation workflow dashboard showing the process"

## SEO Checklist

### On-Page SEO
- [ ] Primary keyword in title (first half preferred)
- [ ] Primary keyword in first paragraph
- [ ] Primary keyword in at least one H2
- [ ] Secondary keywords distributed naturally
- [ ] Meta description includes primary keyword
- [ ] Alt text on all images
- [ ] Internal links to 2-3 related pages
- [ ] External links to 1-2 authoritative sources

### Technical SEO
- [ ] URL slug is descriptive and keyword-rich
- [ ] Title under 70 characters
- [ ] Description under 160 characters
- [ ] Hero image is optimized (under 500KB)
- [ ] All images have alt text

### Readability
- [ ] Short paragraphs (2-4 sentences)
- [ ] Subheadings every 300 words
- [ ] Bullet points for lists
- [ ] No walls of text
- [ ] Clear, jargon-free language

## Engagement Best Practices

### Hook Readers
- Strong opening sentence
- Promise specific value
- Address reader directly ("you")

### Keep Readers
- Subheadings that preview content
- Visual breaks (images, lists, quotes)
- Progressive disclosure of information
- Maintain momentum toward conclusion

### Convert Readers
- Clear call-to-action at end
- Link to contact/services page
- Suggest related posts

## Voice and Tone

Monsoft Solutions blog voice:
- **Authoritative but approachable**: Expert knowledge, conversational delivery
- **Practical over theoretical**: Focus on actionable insights
- **Direct and concise**: No fluff, respect reader's time
- **Optimistic but realistic**: Solutions-focused, acknowledging challenges

**Do:**
- Use "you" and "your"
- Include specific examples
- Share real data when available
- Admit when something is complex

**Don't:**
- Use excessive jargon
- Make unsupported claims
- Write in passive voice (mostly)
- Pad content with filler

## Example Post Outline

```markdown
---
title: "How to Automate Customer Follow-ups Without Losing the Personal Touch"
description: "Learn the exact automation strategies that help businesses maintain relationships while saving 10+ hours per week on follow-ups."
pubDate: 2026-02-01
category: "AI & Automation"
tags: ["Automation", "Customer Relations", "Email", "CRM"]
readingTime: "8 min read"
heroImage: "./images/hero.jpg"
heroImageAlt: "Business owner reviewing automated email sequences on laptop"
---

[Opening Hook - 50 words]
The problem with follow-up automation...

## The Follow-up Problem Most Businesses Face
[200-300 words]
Stats, pain points, why it matters

![Diagram showing typical follow-up workflow](./images/inline-1.jpg)

## The Automation Framework That Works
[400-500 words]
Your solution/methodology

### Step 1: Map Your Customer Journey
Details...

### Step 2: Identify Automation Points
Details...

### Step 3: Build Personal Triggers
Details...

![Screenshot of automation workflow](./images/inline-2.jpg)

## Real Results: What to Expect
[200-300 words]
Case study, data, outcomes

## Getting Started This Week
[150-200 words]
Actionable next steps

---

[CTA - 50 words]
Link to contact, related resources
```

## Quality Checklist

Before publishing:

- [ ] Title is compelling and under 70 chars
- [ ] Description is valuable and under 160 chars
- [ ] Opening hooks the reader immediately
- [ ] Content delivers on title's promise
- [ ] 2-3 inline images with alt text
- [ ] Hero image is high quality and relevant
- [ ] All links work
- [ ] Grammar and spelling checked
- [ ] Reads well on mobile (short paragraphs)
- [ ] Clear call-to-action at the end
- [ ] Internal links to related content
