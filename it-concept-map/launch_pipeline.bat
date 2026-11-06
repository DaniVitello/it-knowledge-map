@echo off
cd "C:\Users\DGVit\Proyectos\IT Career\it-concept-map"
call .venv\Scripts\activate.bat
echo Starting overnight monitor...
start /B python overnight_monitor.py > overnight_monitor.log 2>&1
echo Starting pipeline...
python run_all_areas.py > run_all_areas.log 2>&1
echo Pipeline finished. Starting post-batch eval...
python eval_concept.py --all > eval_results.log 2>&1
echo All done.
