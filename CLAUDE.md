# Jekyll Personal Website - meawoppl.github.io

This is a Jekyll-based personal website using the hackcss theme, hosted on GitHub Pages.

## Project Structure

- Jekyll static site generator with hackcss theme
- Portfolio items in `_portfolio/` collection 
- Press mentions in `_press/` collection
- Images organized in `/images/` with project-specific subdirectories
- Resume in LaTeX format in `/resume/`

## Development Commands

- `bundle exec jekyll serve` - Run local development server
- `bundle exec jekyll build` - Build site for production
- `./build-push.sh` - Build site and push to GitHub Pages (uses git add . pattern)

## Content Management

- Portfolio items are markdown files in `_portfolio/` with front matter
- Press mentions are markdown files in `_press/` with front matter
- Blog posts are markdown files in `_posts/` following Jekyll naming convention: `YYYY-MM-DD-title.md`
- Images should be placed in appropriate subdirectories under `/images/`
- Resume updates require editing `MatthewGoodman.tex` and recompiling to PDF

### Blog Posts

- Create posts in `_posts/` directory
- File naming: `YYYY-MM-DD-post-title.md`
- Required front matter: `title`, `date`, `layout: post`
- Posts automatically appear on `/blog.html` in reverse chronological order

## Site Configuration

- Main config in `_config.yml`
- Theme mode set to "standard" (options: dark, standard, markdown)
- Navigation defined in config file
- Social links configured for GitHub, Facebook, Twitter, Twitch

## Deployment

- Hosted on GitHub Pages
- Auto-deploys from master branch
- Custom domain: meawoppl.github.io

## Important Notes

- Uses Ruby/Jekyll with Bundler for dependency management
- Following user's git workflow: individual file adds, not `git add -A`
- Branch naming: prefix with "meawoppl/" and use dashes for spaces