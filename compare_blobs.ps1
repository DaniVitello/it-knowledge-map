
$pairs = @(
  @("it-concept-map/backend.py","it-concept-map/main/backend.py"),
  @("it-concept-map/runner.py","it-concept-map/main/runner.py"),
  @("it-concept-map/synthesis.py","it-concept-map/main/synthesis.py"),
  @("it-concept-map/writer.py","it-concept-map/main/writer.py"),
  @("it-concept-map/llm_groq.py","it-concept-map/main/llm_groq.py"),
  @("it-concept-map/cli.py","it-concept-map/main/cli.py"),
  @("it-concept-map/models.py","it-concept-map/main/models.py"),
  @("it-concept-map/registry.py","it-concept-map/main/registry.py"),
  @("it-concept-map/research.py","it-concept-map/main/research.py"),
  @("it-concept-map/state.py","it-concept-map/main/state.py"),
  @("it-concept-map/validation.py","it-concept-map/main/validation.py"),
  @("it-concept-map/areas.py","it-concept-map/main/areas.py"),
  @("it-concept-map/log.py","it-concept-map/main/log.py"),
  @("it-concept-map/pilot.py","it-concept-map/exe/pilot.py"),
  @("it-concept-map/run_pipeline.py","it-concept-map/exe/run_pipeline.py"),
  @("it-concept-map/run_all_areas.py","it-concept-map/exe/run_all_areas.py"),
  @("it-concept-map/run_area.py","it-concept-map/exe/run_area.py"),
  @("it-concept-map/run_missing.py","it-concept-map/exe/run_missing.py"),
  @("it-concept-map/run_pending.py","it-concept-map/exe/run_pending.py"),
  @("it-concept-map/retry_failed.py","it-concept-map/exe/retry_failed.py"),
  @("it-concept-map/eval_concept.py","it-concept-map/exe/eval_concept.py")
)
foreach ($p in $pairs) {
  $old = (git rev-parse "refs/backup/main:$($p[0])" 2>$null)
  $new = (git rev-parse "HEAD:$($p[1])" 2>$null)
  if ($old -and $new -and $old -eq $new) { Write-Output "OK   $($p[1])" }
  elseif ($old -and $new) { Write-Output "DIFF $($p[1]) old=$($old.Substring(0,7)) new=$($new.Substring(0,7))" }
  else { Write-Output "MISS $($p[0]) -> $($p[1])" }
}
