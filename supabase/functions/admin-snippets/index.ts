import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";

const ADMIN_CODE = "728022";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

  try {
    const body = await req.json();
    const { code, action, payload } = body;

    if (code !== ADMIN_CODE) {
      return new Response(JSON.stringify({ error: "رمز الحماية غير صحيح" }), {
        status: 401,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

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
      return new Response(JSON.stringify({ data }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (action === "insert") {
      const { data, error } = await supabase.from("snippets").insert(payload).select().single();
      if (error) throw error;
      return new Response(JSON.stringify({ data }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (action === "delete") {
      const { error } = await supabase.from("snippets").delete().eq("id", payload.id);
      if (error) throw error;
      return new Response(JSON.stringify({ ok: true }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    if (action === "upload") {
      // payload: { fileName, base64, contentType }
      const bytes = Uint8Array.from(atob(payload.base64), (c) => c.charCodeAt(0));
      const path = `${Date.now()}-${payload.fileName}`;
      const { error } = await supabase.storage
        .from("snippet-files")
        .upload(path, bytes, { contentType: payload.contentType, upsert: false });
      if (error) throw error;
      const { data: pub } = supabase.storage.from("snippet-files").getPublicUrl(path);
      return new Response(JSON.stringify({ url: pub.publicUrl, path }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(JSON.stringify({ error: "إجراء غير معروف" }), {
      status: 400,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (e) {
    return new Response(JSON.stringify({ error: (e as Error).message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
