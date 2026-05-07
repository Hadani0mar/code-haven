
CREATE OR REPLACE FUNCTION public.increment_snippet_views(snippet_id uuid)
RETURNS void
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  UPDATE public.snippets SET views = views + 1 WHERE id = snippet_id AND published = true;
$$;

CREATE OR REPLACE FUNCTION public.increment_snippet_likes(snippet_id uuid)
RETURNS void
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  UPDATE public.snippets SET likes = likes + 1 WHERE id = snippet_id AND published = true;
$$;

GRANT EXECUTE ON FUNCTION public.increment_snippet_views(uuid) TO anon, authenticated;
GRANT EXECUTE ON FUNCTION public.increment_snippet_likes(uuid) TO anon, authenticated;
