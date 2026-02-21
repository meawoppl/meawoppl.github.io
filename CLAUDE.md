# Astro Personal Website - meawoppl.github.io

Astro-based personal website with hack.css theme, hosted on GitHub Pages.

## Project Structure

- `src/pages/` - Astro page routes
- `src/layouts/` - Page layouts (Default, Post, Portfolio, PortfolioNav)
- `src/components/` - Reusable components (Head, Navigation, Footer, GithubRibbon)
- `src/content/posts/` - Blog posts (markdown with `title` and `date` frontmatter)
- `src/content/portfolio/` - Portfolio items (markdown with `name`, `date`, `thumb` frontmatter)
- `src/content/press/` - Press mentions (markdown with `text`, `date`, `sitetitle`, `siteurl` frontmatter)
- `src/styles/main.scss` - Consolidated stylesheet
- `public/` - Static assets (images, resume, favicon)

## Development Commands

- `npm run dev` - Run local development server
- `npm run build` - Build site for production
- `npm run preview` - Preview production build locally

## Content Management

- Blog posts go in `src/content/posts/` as `slug.md` (no date prefix needed)
- Required frontmatter: `title`, `date`
- Portfolio items go in `src/content/portfolio/`
- Press mentions go in `src/content/press/`
- Images go in `public/images/` subdirectories

## Deployment

- GitHub Actions deploys on push to master
- Workflow: `.github/workflows/deploy.yml`
- GitHub Pages source must be set to "GitHub Actions" in repo settings
