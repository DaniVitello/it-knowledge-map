
import os, json, csv, collections, datetime

base = r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map\workdir\concepts"
out_csv = r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map\workdir\audit.csv"
out_md = r"C:\Users\DGVit\Proyectos\IT Career\it-concept-map\workdir\audit_summary.md"

rows = []
status_counts = collections.Counter()
error_counts = collections.Counter()
phase_counts = collections.Counter()
total_runs = 0
durations = []

for d in sorted(os.listdir(base)):
    cdir = os.path.join(base, d)
    if not os.path.isdir(cdir): continue
    estado_path = os.path.join(cdir, "estado.json")
    events_path = os.path.join(cdir, "events.jsonl")
    estado = {}
    if os.path.exists(estado_path):
        try:
            with open(estado_path, encoding="utf-8") as f:
                estado = json.load(f)
        except Exception as e:
            estado = {"_error": str(e)}
    events = []
    if os.path.exists(events_path):
        with open(events_path, encoding="utf-8") as f:
            for line in f:
                line=line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except: pass

    status = estado.get("status", "?")
    status_counts[status] += 1
    created = estado.get("created_at")
    updated = estado.get("updated_at")
    retries = estado.get("retries", 0)
    phase_data = estado.get("phase_data", {}) or {}
    failed_phase = phase_data.get("failed_phase")
    failed_reason = phase_data.get("failed_reason")
    run_ids = set(e.get("run_id") for e in events if e.get("run_id"))
    total_runs += len(run_ids)
    for e in events:
        et = e.get("event")
        if et not in ("run_start","run_end","phase_done"):
            error_counts[et] += 1
    for e in events:
        if e.get("event") == "phase_done":
            phase_counts[e.get("phase")] += 1
    dur = None
    if created and updated:
        try:
            t0 = datetime.datetime.fromisoformat(created.replace("Z","+00:00"))
            t1 = datetime.datetime.fromisoformat(updated.replace("Z","+00:00"))
            dur = (t1-t0).total_seconds()
            durations.append(dur)
        except: pass

    rows.append({
        "concept_id": d,
        "status": status,
        "created_at": created,
        "updated_at": updated,
        "duration_s": round(dur,1) if dur is not None else "",
        "retries": retries,
        "failed_phase": failed_phase or "",
        "failed_reason": failed_reason or "",
        "runs": len(run_ids),
        "events": len(events),
    })

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

total = len(rows)
avg_dur = sum(durations)/len(durations) if durations else 0
md = []
md.append("# Auditoría del pipeline IT Career\n\n")
md.append(f"- Conceptos: {total}\n")
md.append(f"- Runs totales (sum de run_id únicos por concepto): {total_runs}\n")
md.append(f"- Duración promedio (created→updated): {avg_dur:.1f}s\n\n")
md.append("## Estados\n")
for k,v in status_counts.most_common():
    md.append(f"- {k}: {v}\n")
md.append("\n## Eventos no estándar (errores/reintentos)\n")
for k,v in error_counts.most_common():
    md.append(f"- {k}: {v}\n")
md.append("\n## Fases completadas (conteo)\n")
for k,v in phase_counts.most_common():
    md.append(f"- {k}: {v}\n")
md.append("\n## Conceptos con reintentos > 0\n")
retried = [r for r in rows if str(r["retries"]) not in ("", "0", "None")]
md.append(f"- Cantidad: {len(retried)}\n")
for r in retried[:20]:
    md.append(f"  - {r['concept_id']}: retries={r['retries']}, status={r['status']}\n")
md.append("\n## Conceptos con failed_phase\n")
failed = [r for r in rows if r["failed_phase"]]
md.append(f"- Cantidad: {len(failed)}\n")
for r in failed[:30]:
    md.append(f"  - {r['concept_id']}: phase={r['failed_phase']}, reason={r['failed_reason']}\n")

with open(out_md, "w", encoding="utf-8") as f:
    f.write("".join(md))

print("done", total, "concepts")
print("csv:", out_csv)
print("md:", out_md)
