# Blog Writing Skill

This document defines the guidelines for creating SEO-optimized, engaging blog posts for Monsoft Solutions.

**Related Documents:**

- [BLOG-TOPICS.md](./BLOG-TOPICS.md) — Topic clusters, content gaps, and audience segmentation
- [TARGET_AUDIENCE.md](./TARGET_AUDIENCE.md) — Detailed audience profiles and messaging guidelines

---

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
title: 'Your Compelling Title Here' # Max 70 chars
description: 'A compelling meta description' # Max 160 chars
pubDate: 2026-01-31
author: 'Monsoft Solutions'
category: 'AI & Automation' # See allowed categories
tags: ['AI', 'Automation', 'Business'] # 3-5 relevant tags
featured: false # true for hero placement
draft: false # true to hide from prod
readingTime: '7 min read'
heroImage: './images/hero.jpg'
heroImageAlt: 'Descriptive alt text for the hero image'
---
```

### Allowed Categories

- AI & Automation
- Web Development
- Business Growth
- Technology Trends
- Case Studies
- Guides & Tutorials
- Local Business
- Medical & Aesthetics

---

## E-E-A-T Guidelines for YMYL Content

Medical and aesthetics content is classified as YMYL (Your Money or Your Life) by Google. These topics require higher E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) standards.

### Experience

- Include real implementation stories and case studies
- Reference specific client outcomes (with permission)
- Share practical lessons learned from actual deployments
- Use first-hand examples: "In our work with aesthetic practices, we've found..."

### Expertise

- Use correct medical/industry terminology
- Cite current industry standards and best practices
- Reference authoritative sources (HIPAA.gov, industry associations)
- Include expert quotes when available
- Author bio should highlight relevant credentials

### Authoritativeness

- Link to primary sources (official documentation, regulations)
- Reference industry publications and research
- Include client testimonials where appropriate
- Cite specific metrics and outcomes

### Trustworthiness

- Include accurate, up-to-date information
- Add appropriate disclaimers for medical/legal topics
- Display "Last Updated" dates on evergreen content
- Be transparent about limitations and when to seek professional advice
- Never make unsubstantiated claims

### YMYL Content Checklist

Before publishing medical/aesthetics content:

- [ ] All medical claims are accurate and sourced
- [ ] HIPAA references are current and correct
- [ ] Appropriate disclaimers included
- [ ] No misleading health/safety claims
- [ ] Expert sources cited where applicable
- [ ] Content reviewed for accuracy
- [ ] "Last updated" date included

---

## Featured Snippet Optimization

Optimize content structure to capture featured snippets and AI Overviews.

### Direct Answer Opening

For posts targeting question-based queries, provide a 40-60 word direct answer in the opening paragraph. This increases chances of appearing in featured snippets.

**Example (for "What is HIPAA-compliant marketing?"):**

> HIPAA-compliant marketing is the practice of promoting healthcare services while protecting patient health information (PHI). It requires obtaining proper consent before using patient data, securing all marketing systems, training staff on privacy requirements, and ensuring third-party tools meet HIPAA standards. Violations can result in fines up to $1.5 million per incident.

### Definition Blocks

For "What is..." queries, use a clear definition format:

```markdown
## What Is [Term]?

**[Term]** is [concise definition in 1-2 sentences]. [Additional context in 1-2 sentences explaining why it matters to the reader.]
```

### List Format for How-To Queries

For "How to..." queries, use numbered steps that could be extracted:

```markdown
## How to [Achieve Result]

1. **Step Name** — Brief description of what to do
2. **Step Name** — Brief description of what to do
3. **Step Name** — Brief description of what to do
```

### Comparison Tables

For "vs" queries, use clear comparison tables:

```markdown
| Feature       | Option A    | Option B    |
| ------------- | ----------- | ----------- |
| Key Feature 1 | Description | Description |
| Key Feature 2 | Description | Description |
| Best For      | Use case    | Use case    |
```

### FAQ Section Format

Include an FAQ section with 40-60 word answers for FAQ schema:

```markdown
## Frequently Asked Questions

### [Question in natural language]?

[40-60 word answer that directly addresses the question. Include the key information upfront, then provide brief supporting context.]

### [Next question]?

[40-60 word answer...]
```

---

## Audience-Specific Messaging

Tailor language and examples to the target audience. See [TARGET_AUDIENCE.md](./TARGET_AUDIENCE.md) for complete profiles.

### Aesthetics & Plastic Surgery Audience

**Language to Use:**

- Patients (not customers)
- Consultations (not appointments)
- Procedures (not services)
- Practice (not business)
- HIPAA, compliance, PHI
- Conversion, booking rate, cost per acquisition

**Pain Points to Address:**

- Leads falling through due to slow response times
- Competition from larger practices with bigger budgets
- Skepticism from past agency disappointments
- No time for marketing while focused on patient care

**Proof Points That Resonate:**

- Specific metrics: "+67% consultation bookings," "+340% website traffic"
- HIPAA compliance explicitly addressed
- Industry-specific case studies
- ROI framed in patient lifetime value

**Example Phrasing:**

- ✅ "Capture after-hours patient inquiries automatically"
- ✅ "HIPAA-compliant automation for your practice"
- ❌ "Get more customers with our chatbot"
- ❌ "Boost your business leads"

### Local Small Business Audience

**Language to Use:**

- Customers (not patients)
- Leads, bookings, jobs, calls
- Clients (for professional services)
- Revenue, time saved, hours back

**Pain Points to Address:**

- Missed calls going to competitors
- Drowning in admin work instead of billable hours
- Invisible in "near me" searches
- Not tech-savvy but willing to try proven solutions
- Can't afford enterprise technology

**Proof Points That Resonate:**

- Time saved: "10+ hours per week"
- Revenue impact: "3x more leads"
- Simplicity: "If you can use a smartphone..."
- Local success stories

**Example Phrasing:**

- ✅ "Never miss a call again—even while you're on a job"
- ✅ "Simple automation that works while you work"
- ❌ "Optimize your patient communication workflow"
- ❌ "Enterprise-grade AI solutions"

---

## Local SEO Integration Guidelines

Incorporate local signals naturally for Southwest Florida market positioning.

### Location Mentions

When relevant to the content, include:

- **Primary:** Southwest Florida, SWFL
- **Cities:** Naples, Fort Myers, Cape Coral, Bonita Springs, Estero
- **Regional context:** "Florida's Gulf Coast," "Lee and Collier County"

**Natural integration examples:**

- "Local businesses in Naples and Fort Myers are discovering..."
- "For SWFL service companies, seasonal fluctuations..."
- "Whether you're in Cape Coral or Bonita Springs..."

### Regional Context

Reference local factors when applicable:

- **Seasonality:** Snowbird season (Nov-Apr), hurricane season, summer slowdowns
- **Local industries:** Tourism, real estate, construction, healthcare
- **Community aspects:** Local events, regional business associations

### Local Search Phrases

For posts targeting local queries, include variations:

- "[Service] in [City]"
- "[Service] near me"
- "[City] [industry] [solution]"
- "Southwest Florida [topic]"

### Schema Recommendations

When writing about local business strategies, recommend readers implement:

- LocalBusiness schema
- Service schema with areaServed
- FAQ schema for common local queries
- Review schema for testimonials

---

## Internal Linking Strategy

Every post must include strategic internal links to build site authority and guide readers.

### Required Links Per Post

| Link Type           | Minimum | Purpose                                   |
| ------------------- | ------- | ----------------------------------------- |
| Internal blog links | 2-3     | Related content, keep readers on site     |
| Service page link   | 1       | Connect content to commercial pages       |
| Contact page link   | 1       | Clear path to conversion (usually in CTA) |

### Topic Cluster Linking Rules

1. **Cluster → Pillar:** Every cluster post MUST link to its pillar post
2. **Pillar → Clusters:** Pillar posts should link to all related cluster posts
3. **Cross-cluster:** Link between clusters when topics naturally overlap

### Service Page Mapping

| Blog Category        | Primary Service Page     |
| -------------------- | ------------------------ |
| AI & Automation      | /services/automation     |
| Medical & Aesthetics | /services/aesthetics     |
| Local Business       | /services/local-business |
| Web Development      | /services                |
| Business Growth      | /services (or specific)  |

### Link Placement Best Practices

- Link within the first 2-3 paragraphs when natural
- Use descriptive anchor text (not "click here")
- Link to related posts in the body, not just at the end
- CTA section should link to contact page

**Example anchor text:**

- ✅ "Learn more about [automating patient communication](/blog/patient-communication-automation)"
- ✅ "Our [automation services](/services/automation) can help..."
- ❌ "Click here for more"
- ❌ "[Link](/services)"

---

## Topic Cluster Awareness

Before writing, determine the post's role in the content cluster.

### Pre-Writing Checklist

1. **Post type:** Is this a pillar (2,500-4,000 words) or cluster (1,200-2,000 words)?
2. **Cluster assignment:** What pillar does this cluster post support?
3. **Related content:** What other cluster posts exist in this topic area?
4. **Link planning:** Plan internal links before writing

### Pillar Post Requirements

- Comprehensive coverage of the topic (2,500-4,000 words)
- Links to all related cluster posts
- Serves as the definitive resource on the topic
- Targets broader, high-volume keywords
- Updated regularly as new cluster content is added

### Cluster Post Requirements

- Focused coverage of a specific subtopic (1,200-2,000 words)
- MUST link to the pillar post (required)
- Targets specific, long-tail keywords
- References pillar for broader context

---

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

---

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

---

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

---

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

---

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

---

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

---

## Example Post Outline

```markdown
---
title: 'How to Automate Customer Follow-ups Without Losing the Personal Touch'
description: 'Learn the exact automation strategies that help businesses maintain relationships while saving 10+ hours per week on follow-ups.'
pubDate: 2026-02-01
category: 'AI & Automation'
tags: ['Automation', 'Customer Relations', 'Email', 'CRM']
readingTime: '8 min read'
heroImage: './images/hero.jpg'
heroImageAlt: 'Business owner reviewing automated email sequences on laptop'
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

---

## Quality Checklist

Before publishing, verify ALL items:

### Content Quality

- [ ] Title is compelling and under 70 chars
- [ ] Description is valuable and under 160 chars
- [ ] Opening hooks the reader immediately
- [ ] Content delivers on title's promise
- [ ] Grammar and spelling checked
- [ ] Reads well on mobile (short paragraphs)

### Visual Elements

- [ ] 2-3 inline images with alt text
- [ ] Hero image is high quality and relevant
- [ ] All images optimized for web

### Links & Navigation

- [ ] All links work
- [ ] Internal links to related content (2-3 minimum)
- [ ] Service page link included
- [ ] Clear call-to-action at the end
- [ ] Contact page linked in CTA

### Featured Snippet Optimization

- [ ] Direct answer in opening (for question-based posts)
- [ ] List format for how-to content
- [ ] Comparison tables where applicable
- [ ] FAQ section with 40-60 word answers

### E-E-A-T Compliance (for YMYL content)

- [ ] Medical/legal claims are accurate and sourced
- [ ] Appropriate disclaimers included
- [ ] Expert sources cited
- [ ] "Last updated" date included

### Topic Cluster Links

- [ ] Cluster posts link to pillar
- [ ] Pillar posts link to clusters
- [ ] Cross-cluster links where relevant

### Audience Tone Check

- [ ] Language matches target audience (see Audience-Specific Messaging)
- [ ] Pain points addressed are relevant to audience
- [ ] Examples resonate with reader's industry
