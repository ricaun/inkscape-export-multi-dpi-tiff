@echo off
setlocal

rem Set the folder and output ZIP file paths using relative paths
set "source_folder=..\export_multi_page_tiff\*"
set "zip_file=\Release\export_multi_page_tiff.zip"
set "md5_file=%zip_file%.md5"

rem Delete the existing Release directory and its contents, if it exists
if exist "%~dp0\Release" (
    echo Deleting existing Release directory...
    rmdir /S /Q "%~dp0\Release"
)

rem Ensure the destination folder for the zip file exists
echo Creating new Release directory...
mkdir "%~dp0\Release"

rem Create ZIP file with the files inside the source folder (without the folder itself)
echo Creating ZIP file...
powershell -Command "Compress-Archive -Path '%source_folder%' -DestinationPath '%~dp0%zip_file%'"
if %errorlevel% neq 0 (
    echo Failed to create ZIP file.
    exit /b %errorlevel%
)

rem Generate MD5 hash of the ZIP file
echo Generating MD5 hash...
certutil -hashfile "%~dp0%zip_file%" MD5 > "%~dp0%md5_file%"
if %errorlevel% neq 0 (
    echo Failed to generate MD5 hash.
    exit /b %errorlevel%
)

echo ZIP file and MD5 hash created successfully in the Release folder.
endlocal
