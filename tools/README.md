# Setup Command Sequence

```bash
# Create project directory
mkdir mediterrania_orchestrator
cd mediterrania_orchestrator

# Create tools directory and add initialization script
mkdir tools
# Create init_project.py in tools directory and add the script content

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Run initialization script
python tools/init_project.py

# Install requirements
pip install -r requirements.txt

# Install package in development mode
pip install -e .

# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Optional: Connect to remote repository
git remote add origin https://github.com/yourusername/mediterrania_orchestrator.git
git branch -M main
git push -u origin main
```
