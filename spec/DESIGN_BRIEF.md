# Design brief - Happy Tails stay planner

Goal: it should feel like **the Happy Tails front desk on a calm morning**, not like an AI product.
A pet parent should land on it and think "this is the resort's own site", not "this is a chatbot".

This brief is **look and feel only**. It deliberately says nothing about how prices are qualified,
what is refused, or how eligibility is shown. Those are behaviours, and v1 must reveal them unaided
(see the rule at the bottom).

## Brand (extracted from happytailspetresorttx.com, 11 Nov 2026)
| Token | Value | Use |
|---|---|---|
| Primary | `#527C8E` slate teal | Buttons, heading accents, active states |
| Secondary | `#51768D` | Hover, secondary buttons |
| Accent | `#4A0D66` deep plum | **Sparingly**: one highlight at most per screen |
| Text | `#393B3C` | Body text |
| Link | `#044F59` | Links |
| Background | `#FFFFFF`, warm off-white surfaces | Page and cards |
| Body font | **DM Sans** | Everything readable |
| Heading font | **BBH Hegarty** (the site's display face); fall back to DM Sans bold if unavailable | Page title, the plan's title |
| Corners | 10 px cards; **pill** buttons (fully rounded) | Matches the site's buttons |
| Logo | Site header logo (see `branding-raw.json`) | Top left |
| Photos | The site's own photos of dogs and suites | Hero and suite thumbnails. No stock, no AI-generated images |

Source: `branding-raw.json` (firecrawl branding extraction; confidence 0.92).

## Layout
- **First screen**: logo, one warm line of welcome, and four clear starting points: **Boarding,
  Daycare, Grooming, Training** (cats included under Boarding). The text input is present but
  secondary. The page invites a choice, not a blank chat.
- **The stay plan is the hero.** Once there is a result, it is the largest element on the page:
  a card titled with the pet's name (e.g. "Biscuit's stay"), dates, the suite with its photo, the
  itemised lines, and the total, with one clear next-step button.
- The conversation is **supporting**: short replies near the input, not a wall of chat bubbles.
- **Mobile first**: on a phone the plan stacks cleanly and the total stays visible.

## Feel
- Warm, calm, trustworthy. Generous white space. One photo is better than three icons.
- Practical: prices and dates are easy to scan; numbers right-aligned in tables.
- Copy in the site's voice: friendly, plain, a little playful.

## Do not
- Gradients, glows, glassmorphism, neon, or the generic purple-blue "AI" palette
- Sparkle icons, robot or assistant avatars, "AI assistant" labels, "How can I help you today?"
- Emoji anywhere
- Chat bubbles as the main element of the page
- Stock or AI-generated pet images
- More than one accent colour per screen

## Footer - REMOVED by owner decision, 11 Nov 2026 (see runs/v1/BUILDER_LOG.md entry 9). No send-step disclosure either (entry 11).
~~Footer (required)~~
Small, muted text: *"Unofficial demo built from Happy Tails Pet Resort's public website.
Not affiliated with or endorsed by Happy Tails Pet Resort."*

## Accessibility
Text contrast at least WCAG AA. Never convey meaning by colour alone; always pair it with a word.
Buttons at least 44 px tall on mobile.

---

## The rule that protects the experiment
This brief goes into **v1** and stays **identical in v2**. If testing shows the page needs a
behaviour-driven visual (for example a "pending assessment" label on a price line), that is
added in v2 **as a logged change tied to a failing test**, never as general polish. Everything
else about the design is held constant, so the before/after measures behaviour only.
