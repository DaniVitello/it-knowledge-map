// Health del chat (probe del frontend). No requiere secret.
export const handler = async (event: any) => {
  const cors = { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type", "Access-Control-Allow-Methods": "GET, OPTIONS" };
  if (event.httpMethod === "OPTIONS") return { statusCode: 204, headers: cors, body: "" };
  const keys = [process.env.GROQ_API_KEYS, process.env.GROK_KEY_1, process.env.GROK_KEY_2]
    .filter(Boolean).join(",").split(",").map((s: string) => s.trim()).filter(Boolean);
  return {
    statusCode: 200,
    headers: { ...cors, "Content-Type": "application/json" },
    body: JSON.stringify({
      status: "ok", version: "2.0.0", release_id: "2026-11-19-95e94e92",
      llm_disponible: keys.length > 0, auth_configured: false, require_auth: false,
    }),
  };
};
