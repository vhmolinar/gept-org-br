---
name: beautiful-ui-craft
description: Guidelines and instructions for creating simple, lightweight frontend code paired with world-class, elegant, and modern visual UI/UX design. Activate when building, editing, or styling user interfaces.
---

# Beautiful UI Craft & Design Guidelines

When creating or modifying frontend user interfaces, prioritize visual excellence and seamless UX while keeping code structure clean and straightforward.

## 1. Color Palette & Surface Aesthetics
- **Theme**: Prefer dark or high-contrast modern themes with deep slate/charcoal backgrounds (`#0b0f17`, `#0f172a`, `#18181b`).
- **Gradients**: Accent headers, borders, and buttons with subtle linear gradients (e.g. `linear-gradient(135deg, #6366f1, #a855f7)`).
- **Glassmorphism & Depth**: Use multi-layered translucent cards with `backdrop-filter: blur(12px)` and soft subtle borders (`1px solid rgba(255, 255, 255, 0.08)`).
- **Shadows**: Avoid harsh black drop shadows. Use soft, ambient, colored elevation shadows (`box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.15)`).

## 2. Typography & Hierarchy
- Use modern Google Fonts such as *Inter*, *Outfit*, or *Plus Jakarta Sans*.
- Enforce strict visual hierarchy: clear bold titles (`font-weight: 700`, `letter-spacing: -0.02em`), muted subheadings (`color: #94a3b8`), and easily scannable body text.
- Give text appropriate line-height (`1.6` for body text) and letter-spacing.

## 3. Micro-Interactions & State Feedback
- Add smooth transitions to all interactive elements (`transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1)`).
- **Hover States**: Apply subtle scale shifts (`transform: translateY(-2px)` or `scale(1.02)`) and glow/border highlights on hover.
- **Active Click States**: Provide tactile button feedback (`transform: scale(0.98)`).
- **Loading & Revealing**: Animate card entries with soft fade-in & slide-up keyframes.

## 4. Layout & Spacing
- Maintain generous whitespace and padding (`padding: 1.5rem` to `2.5rem`, `gap: 1.5rem`).
- Ensure responsive flexibility with fluid CSS Grid (`grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))`) or Flexbox.
- Keep call-to-action (CTA) buttons visually distinct and prioritized over secondary actions.
