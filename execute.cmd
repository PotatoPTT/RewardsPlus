@echo off
call .\.venv\Scripts\python.exe Rewards.py -l pt-BR -g BR
timeout /t 5 > nul
pause