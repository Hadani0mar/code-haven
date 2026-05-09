# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**منصتي** is an Arabic-language code-sharing platform for HTML/CSS/JS snippets. The platform team publishes snippets via a password-protected admin panel; any visitor can browse, copy, or download them without registration.

## Commands

```bash
npm run dev        # Start dev server on port 8080
npm run build      # Production build
npm run lint       # ESLint
npm run test       # Run tests once (Vitest)
npm run test:watch # Run tests in watch mode
```

Run a single test file:
```bash
npx vitest run src/path/to/file.test.ts
```

## Architecture

### Pages & Routing

Two pages, defined in `src/App.tsx`:
- `/` → `src/pages/Index.tsx` — public landing page assembled from `src/components/site/` sections
- `/admin` → `src/pages/Admin.tsx` — password-protected admin dashboard (no Supabase Auth; see below)

### Admin Authentication

The admin panel authenticates via a hardcoded passcode checked inside the `admin-snippets` Supabase Edge Function (`supabase/functions/admin-snippets/index.ts`). The code is stored in `localStorage` under the key `admin_code` and sent with every admin request as `{ code, action, payload }`. There is no JWT or session — just the shared secret.

### Data Flow

**Public reads** — the frontend calls Supabase directly using the anon key:
- `supabase.from("snippets").select(...)` with `.eq("published", true)` (RLS enforces this)
- `supabase.rpc("increment_snippet_views", { snippet_id })` / `increment_snippet_likes` to update counters

**Admin writes** — all mutations go through the `admin-snippets` Edge Function which uses the service role key (bypassing RLS):
- Actions: `list`, `stats`, `insert`, `update`, `delete`, `togglePublished`, `resetCounters`, `upload`
- File uploads are base64-encoded in the browser and decoded in the edge function, then stored in the `snippet-files` storage bucket

### Database Schema

Single primary table: `public.snippets`
- `language`: `"HTML" | "CSS" | "JS"` (stored as TEXT)
- `published`: boolean — only published snippets are visible to anonymous users
- `views`: incremented on copy/download (not page view)
- `likes`: one like per browser session, tracked via `localStorage` key `liked_snippets`
- `file_url` / `file_name`: optional attached file from the `snippet-files` storage bucket; a snippet has either `code` (inline text) or a file, or both

The `user_roles` table and `has_role()` function exist in the schema but are not used by the current frontend — they are legacy from a previous auth approach.

### Supabase Integration

- Client singleton: `src/integrations/supabase/client.ts` — import as `import { supabase } from "@/integrations/supabase/client"`
- TypeScript types auto-generated in `src/integrations/supabase/types.ts` — do not edit manually
- Edge function lives at `supabase/functions/admin-snippets/index.ts` (Deno runtime)
- Env vars required: `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`

## UI Conventions

### Component Libraries

- **shadcn/ui** components live in `src/components/ui/` — add new ones with `npx shadcn@latest add <component>`
- **Site-specific** sections live in `src/components/site/`
- Path alias `@/` maps to `src/`

### Styling

- Tailwind with CSS variable-based theming defined in `src/index.css`
- Custom color tokens beyond the shadcn defaults: `cta` (red call-to-action), `success` (green), `primary-glow` (lighter blue)
- Custom utility classes: `shadow-elegant`, `shadow-card-soft`, `shadow-glow`, `transition-smooth`, `bg-gradient-hero`, `dot-pattern`
- Custom animations: `animate-fade-up`, `animate-float`
- Font: **Cairo** (Arabic UI), **JetBrains Mono** (code blocks)
- The UI is Arabic/RTL — text content is in Arabic; code display blocks use `dir="ltr"`

### Button Variants

`Button` accepts a `variant="cta"` prop (red action button) in addition to standard shadcn variants.

## Testing

Tests use Vitest + jsdom + `@testing-library/react`. Setup file: `src/test/setup.ts`. Test files follow the pattern `src/**/*.{test,spec}.{ts,tsx}`.
