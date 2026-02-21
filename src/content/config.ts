import { defineCollection, z } from 'astro:content';

const posts = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
  }),
});

const portfolio = defineCollection({
  type: 'content',
  schema: z.object({
    name: z.string(),
    date: z.coerce.date(),
    startdate: z.coerce.date().optional(),
    thumb: z.string(),
  }),
});

const press = defineCollection({
  type: 'content',
  schema: z.object({
    text: z.string(),
    date: z.coerce.date(),
    sitetitle: z.string(),
    siteurl: z.string(),
  }),
});

export const collections = { posts, portfolio, press };
