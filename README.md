# gait-stim (MVP)

MVP-пайплайн для экспериментов с замкнутым контуром стимуляции походки:
две "камеры" (Control/Experimental) → pose (YOLO stub) → kinematics/Ψ (пока вручную) → параметры стимуляции (4+ каналов) + EMG placeholder.

## Install (Windows)

```powershell
python -m venv .venv
# если PowerShell ругается на activate:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

.\.venv\Scripts\activate
pip install -U pip
pip install -e .
