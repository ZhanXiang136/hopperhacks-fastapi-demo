Step 1: Create the Virtual Environment
Windows: powershell
python -m venv .venv
py -m venv .venv

macOS / Linux: bash
python3 -m venv .venv

Step 2: Activate the Virtual Environment 
Windows (Command Prompt): powershell
.venv\Scripts\activate.bat
.venv\Scripts\Activate.ps1

macOS / Linux (Bash/Zsh): bash
source .venv/bin/activate

Step 3: Install packages
pip install fastapi
pip intall uvicorn
pip install requests (for testing purposes)
pip install Jinja2 (for HTML pages)

Step 4: Run uvicorn
uvicorn main:app --reload (runs port 8000 by default)

