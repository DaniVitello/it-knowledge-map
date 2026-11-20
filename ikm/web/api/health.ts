// Health del chat (probe del frontend) en Vercel.
export default async function handler(req: any, res: any) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") { res.status(204).end(); return; }
  const keys = [process.env.GROQ_API_KEYS, process.env.GROK_KEY_1, process.env.GROK_KEY_2]
    .filter(Boolean).join(",").split(",").map((s: string) => s.trim()).filter(Boolean);
  return res.status(200).json({
    status: "ok", version: "2.0.0", release_id: "2026-11-19-95e94e92",
    llm_disponible: keys.length > 0, auth_configured: false, require_auth: false,
  });
}
