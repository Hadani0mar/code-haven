-- Roles enum and table
CREATE TYPE public.app_role AS ENUM ('admin', 'user');

CREATE TABLE public.user_roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  role public.app_role NOT NULL DEFAULT 'user',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (user_id, role)
);

ALTER TABLE public.user_roles ENABLE ROW LEVEL SECURITY;

-- Security definer to avoid recursive RLS
CREATE OR REPLACE FUNCTION public.has_role(_user_id UUID, _role public.app_role)
RETURNS BOOLEAN
LANGUAGE SQL
STABLE
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT EXISTS (
    SELECT 1 FROM public.user_roles
    WHERE user_id = _user_id AND role = _role
  )
$$;

CREATE POLICY "Users can view their own roles"
  ON public.user_roles FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

CREATE POLICY "Admins can view all roles"
  ON public.user_roles FOR SELECT
  TO authenticated
  USING (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins manage roles"
  ON public.user_roles FOR ALL
  TO authenticated
  USING (public.has_role(auth.uid(), 'admin'))
  WITH CHECK (public.has_role(auth.uid(), 'admin'));

-- Updated-at helper
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
SET search_path = public
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- Snippets table
CREATE TABLE public.snippets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  description TEXT,
  language TEXT NOT NULL,
  category TEXT,
  code TEXT,
  file_url TEXT,
  file_name TEXT,
  author_name TEXT NOT NULL DEFAULT 'منصتي',
  views INTEGER NOT NULL DEFAULT 0,
  likes INTEGER NOT NULL DEFAULT 0,
  published BOOLEAN NOT NULL DEFAULT true,
  created_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE public.snippets ENABLE ROW LEVEL SECURITY;

-- Public can read published snippets (no login required)
CREATE POLICY "Anyone can view published snippets"
  ON public.snippets FOR SELECT
  USING (published = true);

CREATE POLICY "Admins can view all snippets"
  ON public.snippets FOR SELECT
  TO authenticated
  USING (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can insert snippets"
  ON public.snippets FOR INSERT
  TO authenticated
  WITH CHECK (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can update snippets"
  ON public.snippets FOR UPDATE
  TO authenticated
  USING (public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can delete snippets"
  ON public.snippets FOR DELETE
  TO authenticated
  USING (public.has_role(auth.uid(), 'admin'));

CREATE TRIGGER update_snippets_updated_at
  BEFORE UPDATE ON public.snippets
  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE INDEX idx_snippets_language ON public.snippets(language);
CREATE INDEX idx_snippets_published_created ON public.snippets(published, created_at DESC);

-- Storage bucket for snippet files
INSERT INTO storage.buckets (id, name, public)
VALUES ('snippet-files', 'snippet-files', true);

CREATE POLICY "Public can read snippet files"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'snippet-files');

CREATE POLICY "Admins can upload snippet files"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (bucket_id = 'snippet-files' AND public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can update snippet files"
  ON storage.objects FOR UPDATE
  TO authenticated
  USING (bucket_id = 'snippet-files' AND public.has_role(auth.uid(), 'admin'));

CREATE POLICY "Admins can delete snippet files"
  ON storage.objects FOR DELETE
  TO authenticated
  USING (bucket_id = 'snippet-files' AND public.has_role(auth.uid(), 'admin'));