import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
  }),
});

const portfolio = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/portfolio' }),
  schema: z.object({
    name: z.string(),
    date: z.coerce.date(),
    startdate: z.coerce.date().optional(),
    thumb: z.string(),
  }),
});

const press = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/press' }),
  schema: z.object({
    text: z.string(),
    date: z.coerce.date(),
    sitetitle: z.string(),
    siteurl: z.string(),
  }),
});

export const collections = { posts, portfolio, press };
