# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

조코의 장-나물-밥 (Joko's Jang-Namul-Bap) is a static HTML website showcasing Korean traditional recipes for fermented sauces (장), vegetable side dishes (나물), and rice dishes (밥). The site includes vegan and halal substitution guides.

## Architecture

### Static Site with Client-Side Includes

This project uses vanilla HTML/CSS/JavaScript without a build process. The key architectural pattern is a **partial include system** implemented in `assets/js/includes.js`:

- Pages use `data-include` attributes to load shared components (header, footer)
- Each page specifies a `data-root-path` (e.g., ".", "..", "../..") to resolve relative URLs correctly from any nesting level
- The `includes.js` script loads partials via fetch and updates `data-root-href` and `data-root-src` attributes to correct paths

### Root Path Resolution Pattern

For nested pages (e.g., `recipes/jang/doenjang-jjigae.html`):
- Set `data-root-path="../.."` on the `<body>` element
- Include partials with `<div data-include="../../partials/header.html" data-root-path="../.."></div>`
- In partials, mark links/images with `data-root-href` or `data-root-src` instead of `href`/`src`
- The script resolves these to correct paths based on the page's nesting level

Example from `partials/header.html`:
```html
<a href="index.html" data-root-href="index.html">홈</a>
```

When loaded from `recipes/jang/doenjang-jjigae.html` (data-root-path="../.."), this becomes `href="../../index.html"`.

### Directory Structure

```
codex_Joko/
├── index.html, about.html          # Top-level pages
├── recipes/
│   ├── index.html                  # Recipe hub
│   ├── jang/                       # Fermented sauce recipes
│   ├── namul/                      # Vegetable side dishes
│   └── rice/                       # Rice dishes
├── guides/                         # Vegan/halal and ingredient guides
├── partials/                       # Reusable header/footer
└── assets/
    ├── css/style.css               # Single stylesheet for entire site
    ├── js/includes.js              # Partial include loader
    └── img/                        # Images (logo/, recipes/, ingredients/)
```

## Development Commands

### Serving the Site Locally

Since this is a static site, use any local web server. The `includes.js` fetch calls require an HTTP server (not `file://`):

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (if http-server is installed)
npx http-server -p 8000

# PHP
php -S localhost:8000
```

Then visit `http://localhost:8000/index.html`

### Testing

No formal test suite. Manually verify:
- All pages load without 404s in browser console
- Navigation links work correctly from all nesting levels
- Images display properly
- Accessibility: skip links, ARIA labels, semantic HTML

## Styling Conventions

- **CSS Custom Properties**: All colors and theme values in `:root` variables
- **BEM-like Naming**: Class names like `.recipe-detail`, `.recipe-detail-grid`, `.category-tag`
- **Responsive Design**: Grid layouts adapt to mobile (check `@media` queries in `style.css`)
- **Accessibility**: Use semantic HTML, ARIA labels (`aria-labelledby`, `aria-label`), and skip links

## Adding New Recipes

1. Create a new HTML file in the appropriate category folder (e.g., `recipes/jang/new-recipe.html`)
2. Copy structure from existing recipe (e.g., `doenjang-jjigae.html`)
3. Update `data-root-path` based on nesting level (from `recipes/jang/`, use `../..`)
4. Include header/footer partials with matching `data-root-path`
5. Add recipe card to category index (e.g., `recipes/jang/index.html`)
6. Optionally feature on homepage (`index.html`)

## Image Management

Images are organized by type in `assets/img/`:
- `logo/` - Site branding (joko-logo.svg)
- `recipes/` - Recipe photos (e.g., doenjang-jjigae.jpg)
- `ingredients/` - Ingredient reference images

When adding images, use descriptive filenames matching recipe slugs and provide meaningful `alt` text.

## Important Files

- `assets/js/includes.js` - Controls partial loading and path resolution (critical for navigation)
- `assets/css/style.css` - Single source of truth for all styling
- `partials/header.html`, `partials/footer.html` - Shared site chrome
- `README.md` - Korean language project overview
