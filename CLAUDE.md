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

## Deployment

- GitHub Actions deploys on push to master
- Workflow: `.github/workflows/deploy.yml`
- GitHub Pages source must be set to "GitHub Actions" in repo settings
