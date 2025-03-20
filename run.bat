@echo off
move script.py python\python\python
cd python\python\python
python.exe script.py
cd ..
cd ..
cd ..
move python\python\python\script.py script.py