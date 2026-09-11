---
name: viget-brand-guidelines
description: >-
  Defines Viget's brand identity including visual design, colors, typography,
  voice, tone, and copywriting rules. Use when creating designs, writing copy,
  building UI, generating presentations, or producing any visual or written
  content that should align with the Viget brand. Handles branding, corporate
  identity, visual identity, post-processing, styling, brand colors, typography,
  and visual formatting.
---

## Brand Guidelines

### Colors

**Logo Mark Colors:**

- Teal: `#1395BA` - The larger dot in the Viget logo mark
- Orange: `#F16C20` - The smaller dot in the Viget logo mark

**Primary Blues:**

- Blue (Primary CTA): `#135C92` - Buttons, primary call-to-action elements, links
- Dark Blue: `#054C81` - Footer CTA backgrounds, secondary blue surfaces
- Deep Blue: `#00365E` - Dark accent, icon fills
- Navy (Logo Text): `#092F40` - Viget wordmark color, deepest blue

**Neutrals:**

- Dark (Primary Text): `#282828` - Body text, headings, primary content
- Medium Gray: `#535353` - Secondary body text, descriptions
- Gray (Meta Text): `#757575` - Meta labels, captions, timestamps
- Light Gray (Borders): `#D4D4D4` - Borders, dividers, subtle outlines
- Off-White (Light BG): `#F9F9F9` - Alternating section backgrounds
- White: `#FFFFFF` - Primary backgrounds, text on dark surfaces

**Dark Surface Colors:**

- Slate: `#35454F` - Article hero backgrounds, pull-quote/lede text color
- Teal-Dark: `#2A4D57` - Featured content section backgrounds

**Usage Rules:**

- Use primary blue `#135C92` for interactive elements (buttons, links, CTAs)
- Use neutrals `#282828` through `#757575` for text hierarchy
- Reserve logo mark colors (teal and orange) for the logo only — not as general UI accents. Exception: in presentations, teal may accent dates and timeline markers.
- Dark surfaces use the slate/teal palette (`#35454F`, `#2A4D57`, `#054C81`) — never pure black
- Body text is always `#282828`, never `#000000`

### Typography

- **Font Family**: Geomanist is our official typeface. [Nunito Sans](https://fonts.google.com/specimen/Nunito+Sans) is our fallback when Geomanist isn't available, with system sans-serif as a last resort. For best results, install Geomanist locally.
- **One font family for all text** — headings, body, navigation, buttons, labels. No serif or secondary fonts (code blocks may use system monospace).

**Type Scale:**

| Style              | Size | Weight        | Line Height | Notes                              |
| ------------------ | ---- | ------------- | ----------- | ---------------------------------- |
| Display / Hero     | 80px | 300 (Light)   | 1.0         | Page titles, hero headings         |
| Page Title         | 72px | 300 (Light)   | 1.2         | Large section intros               |
| Section Heading    | 48px | 300 (Light)   | 1.2         | Service headings, feature titles   |
| Article Lede       | 36px | 300 (Light)   | 1.6         | Opening paragraph, color `#35454F` |
| Card Title         | 24px | 400 (Regular) | 1.4         | Work cards, article cards          |
| Body (Article)     | 20px | 400 (Regular) | 1.8         | Long-form article content          |
| Body (Page)        | 18px | 400 (Regular) | 1.6         | Page descriptions, intro text      |
| Base / Nav         | 16px | 400 (Regular) | 1.5         | Navigation, default text           |
| CTA Button (Large) | 18px | 400 (Regular) | —           | Primary page CTAs                  |
| CTA Button (Small) | 14px | 400 (Regular) | —           | Header nav CTA                     |
| Meta Label         | 12px | 400 (Regular) | 1.2         | Uppercase, letter-spacing 1.2px    |
| Section Label      | 16px | 400 (Regular) | 1.2         | Uppercase, letter-spacing 3.2px    |

**Key typographic rules:**

- Large headings (48px+) always use font-weight 300 (light). This creates Viget's signature elegant, airy heading style.
- Body text and smaller headings use font-weight 400 (regular).
- Bold (700) is used sparingly, primarily for newsletter signup headings and emphasis.
- Meta labels and section headers are uppercase with generous letter-spacing.
- Category tags use a `#` prefix (e.g., `#Code`, `#Strategy`, `#News & Culture`).

### Buttons and CTAs

- **Primary Button**: `#135C92` background, white text, `border-radius: 36px` (pill shape), 1px solid border matching background
- **Outline Button**: Transparent background, `#135C92` text and border, `border-radius: 36px`
- **Reversed Button** (on dark backgrounds): White background, `#054C81` text, `border-radius: 36px`
- **Button padding**: `10px 16px` (small) / `16px 24px` (large)
- Buttons never use font-weight bold. They are always weight 400.

### Links

- **Navigation links**: No underline, dark text (`#282828`)
- **Body content links**: Underlined, same color as surrounding body text
- **Category/tag links**: 12px uppercase with `#` prefix, no underline by default, underline on hover

### Layout and Spacing

- **Max container width**: ~1280px (screen-xl)
- **Content padding**: 24px (mobile) / 40px (tablet and up)
- **Section vertical padding**: 64px (mobile) / 80px (tablet) / 128px (desktop)
- **Design philosophy**: Generous whitespace, clean and minimal, content-forward
- **Grid layouts**: Used for work showcases, article cards, and service sections
- **Border style**: 1px solid `#D4D4D4` for dividers between content items

### Dark Sections

Viget uses dark-background sections for visual contrast:

- **Article featured area**: `#35454F` slate with white text
- **Content highlight sections**: `#2A4D57` teal-dark with white text
- **Footer CTA**: `#054C81` dark blue with white text
- On dark backgrounds, buttons become white with dark blue text (reversed)
- The logo and navigation text turn white on dark backgrounds

### Logo

The Viget logo consists of two elements:

1. **Logo mark**: Two overlapping circles — a larger teal (`#1395BA`) dot and a smaller orange (`#F16C20`) dot, positioned to the upper-left of the wordmark
2. **Wordmark**: "viget" set in Geomanist, colored `#092F40` (navy) on light backgrounds and white on dark backgrounds

The logo mark and wordmark always appear together. The mark sits to the left of the text. All lowercase for the wordmark.

If you are in a context where an SVG image can be used, here is the markup of the logo.

```
<svg xmlns="http://www.w3.org/2000/svg" width="144" height="49" fill="none">
  <path fill="#092F40" d="M71.22 9.83c0-.53.495-1.024 1.027-1.024h1.976c.532 0 1.027.493 1.027 1.024v21.637c0 .531-.495 1.025-1.027 1.025h-1.976c-.532 0-1.027-.494-1.027-1.025zm44.101-1.062c5.968 0 10.568 4.404 10.568 10.363 0 .379-.038 1.138-.113 1.518a1.01 1.01 0 0 1-1.028.949h-16.613c.228 3.795 3.497 7.06 8.022 7.06 2.395 0 4.22-.759 5.665-1.86.493-.38.798-.38 1.178-.037.417.378.874.834 1.292 1.214.495.418.646.796.114 1.404-1.14 1.29-4.181 3.15-8.098 3.15-6.881 0-12.165-5.39-12.165-11.88 0-6.415 4.562-11.88 11.444-11.88zm6.652 9.717c-.151-3.302-3.422-6.225-6.881-6.225-3.801 0-6.614 3-6.843 6.225zm21.252 11.274-1.634-1.634c-.115-.112-.532-.265-.952.078 0 0-.835.758-2.242.758-.988 0-1.787-.34-2.358-.948-.569-.608-.95-1.481-.95-2.544 0-.076 0-.113-.037-.152V12.07h6.006a1.02 1.02 0 0 0 1.027-1.025V9.83c0-.607-.419-1.024-1.027-1.024h-6.007V2.732c0-.531-.418-1.024-.988-1.024l-1.749.19c-.533.075-1.026.493-1.026 1.025v5.844h-2.852c-.608 0-1.026.419-1.026 1.026v1.215c0 .532.456 1.024 1.026 1.024h2.852v13.589h.037a7.2 7.2 0 0 0 1.065 3.569c.342.531 1.102 1.593 2.281 2.428 0 0 .038.039.076.039.571.341 1.787.872 3.688.872 1.977 0 3.65-.72 4.866-1.898a.7.7 0 0 0 .19-.455c-.076-.114-.153-.302-.266-.417M66.278 8.806h-2.396c-.494 0-.798.266-.95.607L55.48 27.065l-7.336-17.69c-.153-.302-.494-.607-.95-.607h-2.472c-.836 0-1.14.532-.836 1.252l.38.911L53.2 31.467c.19.494.571 1.025 1.14 1.025h2.205c.533 0 .951-.569 1.141-1.025l9.01-20.497.38-.91c.343-.722 0-1.254-.798-1.254m27.828 23.762h-7.945c-2.053 0-3.042-1.442-3.042-2.81 0-2.201 2.433-3.302 2.433-3.302s2.586 1.594 5.626 1.594c5.856 0 9.81-4.593 9.81-9.603 0-3.758-2.281-5.92-2.281-5.92l3.004-.836c.38-.037.607-.568.607-.948v-.95a1.043 1.043 0 0 0-1.065-1.062H90.761c-5.74 0-9.352 4.592-9.352 9.716 0 3.265 1.787 5.505 1.787 5.505s-3.688 2.162-3.688 6.338c0 3.416 2.585 4.859 4.029 5.239v.15c-.569.343-3.193 1.823-3.193 5.126 0 3.643 3.194 7.59 10.607 7.59 6.69 0 11.443-4.364 11.443-8.919 0-4.745-3.649-6.908-8.288-6.908M91.18 12.336c3.307 0 6.007 2.696 6.007 5.998s-2.698 5.997-6.006 5.997-6.007-2.694-6.007-5.997 2.698-5.998 6.005-5.998m-.267 32.53c-3.762 0-6.614-1.935-6.614-4.593 0-3.265 3.688-4.25 3.688-4.25h6.122c3.876 0 4.181 2.884 4.181 3.567.038 3.264-3.726 5.275-7.375 5.275zM70.916 2.354c0-1.328 1.026-2.353 2.32-2.353 1.33 0 2.357 1.025 2.357 2.353a2.337 2.337 0 0 1-2.357 2.316 2.327 2.327 0 0 1-2.32-2.316"/>
  <circle cx="12.062" cy="20.218" r="12.062" fill="#1395BA"/>
  <circle cx="28.412" cy="7.566" r="6.992" fill="#F16C20"/>
</svg>
```

## Voice and Tone

### Core Voice Attributes

- **Professional but approachable** — expert without being stuffy
- **Confident without boasting** — let the work speak, not superlatives
- **Concise and direct** — say it plainly, then stop
- **Action-oriented** — bias toward doing ("Let's get to work")
- **Proudly independent** — Viget has been independent since 1999 and values that identity
- **Craft-focused** — quality, thoughtfulness, and attention to detail matter

### Writing Style Rules

1. **Use active voice.** "We build products" not "Products are built by us."
2. **Be concise.** Short sentences. No filler words. Say what you mean.
3. **Lead with value.** Start with what matters to the reader, not the company.
4. **Avoid jargon and buzzwords.** Say "we build websites" not "we deliver digital transformation solutions."
5. **Use sentence case for headings.** Not Title Case. Exception: proper nouns and acronyms.
6. **Address the reader directly.** "You" and "your" over "users" and "clients" where appropriate.
7. **Contractions are fine.** "We're" over "We are." Keeps it human.
8. **No exclamation marks in headlines.** Reserve them for genuinely exciting moments, used sparingly.
9. **One idea per paragraph.** Let copy breathe. Whitespace is good.

### Headline Examples (Viget style)

- "Building a better digital world."
- "Building since 1999."
- "Have an unsolvable problem or audacious idea? Let's get to work"
- "What we're thinking about"

### Tone by Context

- **Marketing / Homepage**: Confident, warm, aspirational but grounded
- **Case Studies**: Results-focused, specific, let the work and outcomes lead
- **Blog Articles**: Knowledgeable, conversational, generous with insight
- **CTAs**: Direct and inviting — "Contact Us", "More Work", "Our Clients"
- **Meta / Labels**: Functional and minimal — uppercase, terse

## Technical Details

### Presentation and Document Styling

**Presentation typography differs from web.** Cover slides use a bold title + light subtitle pairing:

- **Cover slide titles**: font-weight 700 (bold), creating a strong visual anchor
- **Cover slide subtitles**: font-weight 300 (light), providing elegant contrast
- **Section divider headings**: font-weight 300 (light), white text on blue backgrounds
- **Content slide subheadings**: font-weight 400, colored in primary blue `#135C92` (not dark text)

This bold/light pairing is specific to presentations and differs from the website where all large headings use weight 300.

**Presentation surface colors:**

- **Section divider backgrounds**: Primary blue (`#135C92` or similar muted steel-blue)
- **Testimonial/quote backgrounds**: Pale teal tint (~`#E8F4F8`), a very light cool blue derived from the brand teal family
- **Data panel backgrounds**: Light blue-gray (~`#E8EEF2`), used behind tables and structured data
- **Image placeholder fallback**: Dark teal (~`#1E3A42` to `#243E47`), used when image areas have no photo

**Slide layout system (fractional grid):**

Viget presentations use a modular layout system based on fractional widths:

- **Cover slides**: Split Vertical (left text / right color block), Split Horizontal (top image / bottom text), Full Width Image, Full Width White
- **Section dividers**: Solid blue background, centered white text, circled numeral for section number
- **Content layouts**: 1/2 + 1/2, 1/3 + 2/3, 2/3 + 1/3 splits for text and image combinations
- **Multi-column**: 2-column, 3-column, and 4-column centered text or stats layouts
- **Device mockups**: Realistic device frames (desktop, laptop, tablet, phone) with drop shadows, arranged in overlapping cascading compositions

**Presentation footer pattern** (cover slides):

- Date line (small, regular weight)
- "Copyright Viget Labs, LLC" (very small, bold)
- Confidentiality notice (very small, regular weight, gray)
- Viget logo (bottom-center or bottom-right)

**Table design:**

- No visible cell borders or grid lines
- Row separation via alternating background tints (zebra striping) using light blue-gray bands
- Table headers: uppercase, bold, dark navy, with generous letter-spacing
- Generous cell padding for readability

### Photography and Imagery

- **Style**: Warm, natural lighting; no harsh flash. Candid and human-centered.
- **Subject matter**: Modern creative workspaces, architectural elements, people in professional settings
- **Motion blur**: Used as a stylistic device in hero imagery to convey dynamism
- **Client logos**: Always rendered in monochrome grayscale on logo grids to maintain visual consistency and prevent any single client's brand colors from dominating

### Data Visualization

When creating charts, graphs, or timelines:

- Use a **monochromatic blue-teal spectrum** — stay within the cool blue-teal family
- Suggested chart palette (light to dark): light sky blue (~`#A5DCE8`), bright cyan (~`#1CC7D0`), primary blue (`#135C92`), deep blue (`#00365E`)
- **No warm colors** (orange, red, yellow) in data visualizations
- Use the brand teal `#1395BA` for accent markers (e.g., "today" indicators on timelines)
- Timeline/Gantt bars use layered, overlapping color-coded segments
- Dotted lines to distinguish dynamic markers (like "today") from solid structural lines
