import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";

const ADMIN_CODE = "728022";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

  try {
    const { code, action, payload } = await req.json();
    if (code !== ADMIN_CODE) return json({ error: "رمز الحماية غير صحيح" }, 401);

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    if (action === "list") {
      const { data, error } = await supabase
        .from("snippets")
        .select("*")
        .order("created_at", { ascending: false });
      if (error) throw error;
      return json({ data });
    }

    if (action === "stats") {
      const { data, error } = await supabase
        .from("snippets")
        .select("views,likes,published");
      if (error) throw error;
      const total = data?.length || 0;
      const published = data?.filter((r) => r.published).length || 0;
      const views = data?.reduce((a, r) => a + (r.views || 0), 0) || 0;
      const likes = data?.reduce((a, r) => a + (r.likes || 0), 0) || 0;
      return json({ data: { total, published, drafts: total - published, views, likes } });
    }

    if (action === "insert") {
      const { data, error } = await supabase.from("snippets").insert(payload).select().single();
      if (error) throw error;
      return json({ data });
    }

    if (action === "update") {
      const { id, ...rest } = payload;
      const { data, error } = await supabase
        .from("snippets")
        .update(rest)
        .eq("id", id)
        .select()
        .single();
      if (error) throw error;
      return json({ data });
    }

    if (action === "togglePublished") {
      const { data: row, error: e1 } = await supabase
        .from("snippets")
        .select("published")
        .eq("id", payload.id)
        .single();
      if (e1) throw e1;
      const { error } = await supabase
        .from("snippets")
        .update({ published: !row.published })
        .eq("id", payload.id);
      if (error) throw error;
      return json({ ok: true, published: !row.published });
    }

    if (action === "resetCounters") {
      const { error } = await supabase
        .from("snippets")
        .update({ views: 0, likes: 0 })
        .eq("id", payload.id);
      if (error) throw error;
      return json({ ok: true });
    }

    if (action === "delete") {
      const { error } = await supabase.from("snippets").delete().eq("id", payload.id);
      if (error) throw error;
      return json({ ok: true });
    }

    if (action === "upload") {
      const bytes = Uint8Array.from(atob(payload.base64), (c) => c.charCodeAt(0));
      const path = `${Date.now()}-${payload.fileName}`;
      const { error } = await supabase.storage
        .from("snippet-files")
        .upload(path, bytes, { contentType: payload.contentType, upsert: false });
      if (error) throw error;
      const { data: pub } = supabase.storage.from("snippet-files").getPublicUrl(path);
      return json({ url: pub.publicUrl, path });
    }

    return json({ error: "إجراء غير معروف" }, 400);
  } catch (e) {
    return json({ error: (e as Error).message }, 500);
  }
});
