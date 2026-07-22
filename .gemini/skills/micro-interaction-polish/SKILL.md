---
name: micro-interaction-polish
description: Best practices for implementing subtle CSS/JS micro-animations, hover effects, button feedback, and entry animations.
---

# Micro-Interaction Polish Guidelines

Enhance interactive elements with lightweight, highly polished feedback animations:

1. **Button Hover & Click**:
```css
.btn {
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, background 0.2s ease;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px -4px rgba(99, 102, 241, 0.4);
}
.btn:active {
  transform: translateY(0) scale(0.98);
}
```

2. **Smooth Reveal Animation**:
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fadeInUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
```

3. **Reduced Motion**:
Always respect user motion preferences:
```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
