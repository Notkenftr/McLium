@echo off

cd /d ../../../aoko/

if exist build (
    rmdir /s /q build
)

cmake -S . -B build
cmake --build build -j

:wait_loop
if not exist build\aoko.so (
    timeout /t 1 /nobreak >nul
    goto wait_loop
)

timeout /t 1 /nobreak >nul

move /Y build\aoko.so ..\libs\