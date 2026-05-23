@echo off

:: Create the main backend folder
mkdir backend
cd backend

:: Create the requirements and env files
type nul > requirements.txt
type nul > .env

:: Create the app folder and its subdirectories
mkdir app
cd app
type nul > main.py

mkdir agents
mkdir api
mkdir core
mkdir memory
mkdir rag
mkdir services
mkdir tools

echo Backend structure created successfully!
pause