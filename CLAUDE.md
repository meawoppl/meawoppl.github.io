# Astro Personal Website - meawoppl.github.io

Astro-based personal website with hack.css theme, hosted on GitHub Pages.

## Project Structure

- `src/pages/` - Astro page routes
- `src/layouts/` - Page layouts (Default, Post, Portfolio, PortfolioNav)
- `src/components/` - Reusable components (Head, Navigation, Footer, GithubRibbon)
- `src/content/posts/` - Blog posts (markdown with `title` and `date` frontmatter)
- `src/content/portfolio/` - Portfolio items (markdown with `name`, `date`, `thumb` frontmatter)
- `src/content/press/` - Press mentions (markdown with `text`, `date`, `sitetitle`, `siteurl` frontmatter)
- `src/content/config.ts` - Content collection schemas (Zod)
- `src/styles/main.scss` - Consolidated stylesheet
- `public/` - Static assets (images, resume, favicon)
- `public/media-list/` - Standalone static media-tracking subsite served at `/media-list/` (plain HTML/CSS/JS, no Astro build)
- `scripts/media-list/` - `validate.py` + JSON schemas for the media-list data

## Development Commands

- `npm install` - Install dependencies (needed on fresh clone)
- `npm run dev` - Run local development server
- `npm run build` - Build site for production (outputs to `dist/`)
- `npm run preview` - Preview production build locally

## Content Management

- Blog posts go in `src/content/posts/` as `YYYY-MM-DD-slug.md`
- Required post frontmatter: `title`, `date`
- Portfolio items go in `src/content/portfolio/` with frontmatter: `name`, `date`, `thumb`
- Press mentions go in `src/content/press/` with frontmatter: `text`, `date`, `sitetitle`, `siteurl`
- Images go in `public/images/` subdirectories
- Portfolio thumbnails reference images via `thumb` path (leading `/` is handled by `thumbUrl()` helper)

## Media List Subsite

- Static site under `public/media-list/`; served verbatim by Astro at `/media-list/` (linked from the top nav)
- Hand-edited data lives in `public/media-list/data/` (`media.json`, `recommenders.json`); the JS fetches it at runtime
- Categories: book, movie, tv, series, game, topic, music, podcast, article, other. Status: done, in-progress, queued
- `recommended_by` entries must match a `recommenders.json` initial (or use the `Rando(name)` escape hatch)
- Validate with `python scripts/media-list/validate.py` (schema check + recommender cross-refs + duplicate-title check); CI runs it via `.github/workflows/validate-media-list.yml`

## Writing Style

See [docs/writing-style.md](docs/writing-style.md) for a detailed analysis of the blog's voice and tone. Key traits: conversational and direct, dry humor, concrete numbers over vague claims, em dashes for asides, short declarative punchlines after longer explanations, profanity used deliberately for emphasis, generous with credit, opinionated without hedging. When drafting or editing blog posts, match this voice.

## Deployment

- GitHub Actions deploys on push to master
- Workflow: `.github/workflows/deploy.yml`
- GitHub Pages source must be set to "GitHub Actions" in repo settings
