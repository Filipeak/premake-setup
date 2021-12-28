@echo off
pushd ..\
call premake-setup\bin\premake5.exe vs2022
popd
pause