# Configuration and Integration Guide

Complete setup and integration guide for the Codified Lemma Utility (CLU).

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Procedures](#installation-procedures)
3. [Configuration Options](#configuration-options)
4. [Integration Scenarios](#integration-scenarios)
5. [Advanced Setup](#advanced-setup)
6. [Deployment](#deployment)
7. [Backup and Maintenance](#backup-and-maintenance)
8. [Performance Tuning](#performance-tuning)

---

## System Requirements

### Minimum Requirements
- **Python Version**: 3.7 or higher
- **Operating System**: Linux, macOS, Windows
- **Disk Space**: 10 MB (minimal installation)
- **RAM**: 512 MB
- **Dependencies**: None (uses only Python standard library)

### Recommended Requirements
- **Python Version**: 3.9 or higher
- **Disk Space**: 100 MB (for large collections)
- **RAM**: 1 GB
- **Text Editor**: VS Code, PyCharm, or similar with Python support

### Compatibility
- ✅ Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)
- ✅ macOS (10.15+)
- ✅ Windows (10, 11)
- ✅ Works in virtual environments
- ✅ Compatible with Jupyter notebooks

---

## Installation Procedures

### Method 1: Basic Installation (Recommended for Most Users)

#### Step 1: Download Files
```bash
# Create project directory
mkdir clu_project
cd clu_project

# Download clu.py
curl -O https://github.com/suboksy/clu/blob/main/clu.py

# Or manually copy clu.py to this directory
```

#### Step 2: Verify Installation
```bash
# Check Python version
python --version
# Should show Python 3.7 or higher

# Test the utility
python clu.py --stats
```

#### Step 3: Create Initial Data
```bash
# Run the demo to create sample data
python clu.py

# This creates lemmas.json with sample data
```

### Method 2: Virtual Environment Installation (Recommended for Developers)

#### Step 1: Create Virtual Environment
```bash
# Create directory
mkdir clu_project
cd clu_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### Step 2: Install and Configure
```bash
# Copy clu.py to project directory
cp /path/to/clu.py .

# Verify it works
python clu.py --stats

# Deactivate when done (optional)
deactivate
```

### Method 3: System-wide Installation

#### Step 1: Copy to Python Scripts Directory
```bash
# Find Python scripts directory
python -c "import sys; print(sys.prefix)"

# Copy clu.py to scripts directory (Linux/macOS)
sudo cp clu.py /usr/local/bin/

# Make executable
sudo chmod +x /usr/local/bin/clu.py

# Add shebang to top of clu.py if not present:
# #!/usr/bin/env python3
```

#### Step 2: Use from Anywhere
```bash
# Now you can run from any directory
clu.py --stats
```

### Method 4: Integration as Python Module

#### Step 1: Create Package Structure
```bash
mkdir -p my_project/clu
touch my_project/clu/__init__.py
cp clu.py my_project/clu/
```

#### Step 2: Update `__init__.py`
```python
# my_project/clu/__init__.py
from .clu import CodedLemmaUtility

__all__ = ['CodedLemmaUtility']
__version__ = '1.0.0'
```

#### Step 3: Use in Your Project
```python
# In your scripts
from clu import CodedLemmaUtility

clu = CodedLemmaUtility()
```

---

## Configuration Options

### Data File Location

#### Default Configuration
```python
# Uses lemmas.json in current directory
clu = CodedLemmaUtility()
```

#### Custom Location
```python
# Specify custom file path
clu = CodedLemmaUtility('~/Documents/my_lemmas.json')

# Use environment variable
import os
data_file = os.getenv('CLU_DATA_FILE', 'lemmas.json')
clu = CodedLemmaUtility(data_file)
```

#### Multiple Collections
```python
# Separate collections for different subjects
algebra = CodedLemmaUtility('algebra_lemmas.json')
geometry = CodedLemmaUtility('geometry_lemmas.json')
analysis = CodedLemmaUtility('analysis_lemmas.json')
```

### Environment Variables

Create a `.env` file in your project:

```bash
# .env file
CLU_DATA_FILE=/home/user/lemmas/main.json
CLU_BACKUP_DIR=/home/user/lemmas/backups
CLU_EXPORT_DIR=/home/user/lemmas/exports
```

Load in Python:
```python
import os
from dotenv import load_dotenv  # pip install python-dotenv

load_dotenv()

clu = CodedLemmaUtility(os.getenv('CLU_DATA_FILE'))
```

### Configuration File

Create `clu_config.json`:

```json
{
  "data_file": "lemmas.json",
  "backup_enabled": true,
  "backup_directory": "./backups",
  "auto_save": true,
  "default_category": "general",
  "default_export_format": "markdown"
}
```

Load configuration:
```python
import json

def load_config(config_file='clu_config.json'):
    with open(config_file) as f:
        return json.load(f)

config = load_config()
clu = CodedLemmaUtility(config['data_file'])
```

---

## Integration Scenarios

### Scenario 1: Jupyter Notebook Integration

#### Setup
```python
# In notebook cell
%load_ext autoreload
%autoreload 2

import sys
sys.path.append('/path/to/clu')

from clu import CodedLemmaUtility

# Initialize
clu = CodedLemmaUtility('notebook_lemmas.json')
```

#### Interactive Usage
```python
# Add lemma in one cell
code = clu.add_lemma(
    "Pythagorean theorem: a² + b² = c²",
    category="geometry",
    tags=["triangle", "fundamental"]
)

# Search in another cell
results = clu.search(tags=["geometry"])
for c, lemma in results.items():
    print(f"{c}: {lemma['statement']}")

# Export
clu.export_all('markdown', 'notebook_lemmas.md')
```

### Scenario 2: Web Application Integration (Flask)

#### Setup Flask App
```python
# app.py
from flask import Flask, request, jsonify
from clu import CodedLemmaUtility

app = Flask(__name__)
clu = CodedLemmaUtility('web_lemmas.json')

@app.route('/lemmas', methods=['GET'])
def get_lemmas():
    return jsonify(clu.list_all())

@app.route('/lemmas', methods=['POST'])
def add_lemma():
    data = request.json
    code = clu.add_lemma(
        statement=data['statement'],
        proof=data.get('proof'),
        tags=data.get('tags', []),
        category=data.get('category')
    )
    return jsonify({'code': code}), 201

@app.route('/lemmas/<code>', methods=['GET'])
def get_lemma(code):
    lemma = clu.get_lemma(code)
    if lemma:
        return jsonify({code: lemma})
    return jsonify({'error': 'Not found'}), 404

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    results = clu.search(
        query=data.get('query'),
        tags=data.get('tags'),
        category=data.get('category')
    )
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
```

#### Run the Server
```bash
pip install flask
python app.py
```

### Scenario 3: Command-Line Tool Integration

#### Create CLI Wrapper Script
```python
#!/usr/bin/env python3
# clu_cli.py

import argparse
import sys
from clu import CodedLemmaUtility

def main():
    parser = argparse.ArgumentParser(description='CLU Command Line Interface')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a lemma')
    add_parser.add_argument('statement', help='Lemma statement')
    add_parser.add_argument('--proof', help='Proof')
    add_parser.add_argument('--tags', nargs='+', help='Tags')
    add_parser.add_argument('--category', help='Category')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search lemmas')
    search_parser.add_argument('--query', help='Search query')
    search_parser.add_argument('--tags', nargs='+', help='Tags')
    search_parser.add_argument('--category', help='Category')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all lemmas')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export lemmas')
    export_parser.add_argument('format', choices=['text', 'markdown', 'latex', 'json'])
    export_parser.add_argument('--output', help='Output file')
    
    args = parser.parse_args()
    clu = CodedLemmaUtility()
    
    if args.command == 'add':
        code = clu.add_lemma(
            args.statement,
            proof=args.proof,
            tags=args.tags,
            category=args.category
        )
        print(f"Added: {code}")
    
    elif args.command == 'search':
        results = clu.search(
            query=args.query,
            tags=args.tags,
            category=args.category
        )
        for code, lemma in results.items():
            print(f"{code}: {lemma['statement']}")
    
    elif args.command == 'list':
        for code, statement in clu.list_all().items():
            print(f"{code}: {statement}")
    
    elif args.command == 'export':
        clu.export_all(args.format, args.output)
        if args.output:
            print(f"Exported to {args.output}")

if __name__ == '__main__':
    main()
```

#### Usage
```bash
chmod +x clu_cli.py

./clu_cli.py add "Test lemma" --tags test basic --category testing
./clu_cli.py search --tags test
./clu_cli.py export markdown --output output.md
```

### Scenario 4: Git Integration for Version Control

#### Setup
```bash
# Initialize git repository
git init

# Create .gitignore
cat > .gitignore << EOF
*.pyc
__pycache__/
venv/
.env
*.bak
EOF

# Add files
git add clu.py lemmas.json README.md CONFIG.md .gitignore
git commit -m "Initial commit"
```

#### Workflow
```bash
# Before making changes
git pull origin main

# Make changes to lemmas
python -c "from clu import CodedLemmaUtility; clu = CodedLemmaUtility(); clu.add_lemma('New lemma')"

# Commit changes
git add lemmas.json
git commit -m "Added new lemma"
git push origin main
```

### Scenario 5: Automated Backup System

#### Create Backup Script
```python
# backup_clu.py
import shutil
import os
from datetime import datetime
from clu import CodedLemmaUtility

def backup_lemmas(data_file='lemmas.json', backup_dir='backups'):
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create timestamped backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'lemmas_{timestamp}.json')
    
    # Copy data file
    if os.path.exists(data_file):
        shutil.copy2(data_file, backup_file)
        print(f"Backup created: {backup_file}")
        
        # Export to markdown as well
        clu = CodedLemmaUtility(data_file)
        md_file = os.path.join(backup_dir, f'lemmas_{timestamp}.md')
        clu.export_all('markdown', md_file)
        print(f"Markdown export: {md_file}")
        
        return backup_file
    else:
        print(f"Data file not found: {data_file}")
        return None

if __name__ == '__main__':
    backup_lemmas()
```

#### Automate with Cron (Linux/macOS)
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd /path/to/clu && python backup_clu.py
```

#### Automate with Task Scheduler (Windows)
```batch
REM Create batch file: backup_clu.bat
@echo off
cd C:\path\to\clu
python backup_clu.py
```

Then create a scheduled task in Task Scheduler to run this batch file.

---

## Advanced Setup

### Multi-User Setup

#### Shared Storage
```python
# config.py
import os

# Use shared network location
SHARED_BASE = '/mnt/shared/clu'
USER = os.getenv('USER')

class MultiUserCLU:
    def __init__(self):
        # User-specific collection
        user_file = os.path.join(SHARED_BASE, 'users', f'{USER}.json')
        self.personal = CodedLemmaUtility(user_file)
        
        # Shared collection (read-only for most users)
        shared_file = os.path.join(SHARED_BASE, 'shared', 'lemmas.json')
        self.shared = CodedLemmaUtility(shared_file)
    
    def search_all(self, **kwargs):
        # Search both collections
        personal_results = self.personal.search(**kwargs)
        shared_results = self.shared.search(**kwargs)
        return {**shared_results, **personal_results}
```

### Database Integration

#### SQLite Backend (Advanced)
```python
# clu_db.py - Extended version with SQLite
import sqlite3
import json
from clu import CodedLemmaUtility

class CLUDatabase:
    def __init__(self, db_file='lemmas.db'):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS lemmas (
                code TEXT PRIMARY KEY,
                statement TEXT NOT NULL,
                proof TEXT,
                category TEXT,
                notes TEXT,
                tags TEXT,
                dependencies TEXT,
                created TEXT,
                modified TEXT
            )
        ''')
        self.conn.commit()
    
    def import_from_json(self, json_file):
        clu = CodedLemmaUtility(json_file)
        for code, lemma in clu.lemmas.items():
            self.conn.execute('''
                INSERT OR REPLACE INTO lemmas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                code,
                lemma['statement'],
                lemma['proof'],
                lemma['category'],
                lemma['notes'],
                json.dumps(lemma['tags']),
                json.dumps(lemma['dependencies']),
                lemma['created'],
                lemma['modified']
            ))
        self.conn.commit()
    
    def full_text_search(self, query):
        cursor = self.conn.execute('''
            SELECT code, statement FROM lemmas
            WHERE statement LIKE ? OR proof LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        return cursor.fetchall()
```

### Plugin System

#### Create Plugin Interface
```python
# clu_plugins.py

class CLUPlugin:
    """Base class for CLU plugins"""
    
    def on_lemma_added(self, code, lemma):
        """Called when a lemma is added"""
        pass
    
    def on_lemma_updated(self, code, lemma):
        """Called when a lemma is updated"""
        pass
    
    def on_search(self, query, results):
        """Called after a search"""
        pass

# Example: Notification plugin
class NotificationPlugin(CLUPlugin):
    def on_lemma_added(self, code, lemma):
        print(f"📝 New lemma added: {code}")
    
    def on_lemma_updated(self, code, lemma):
        print(f"✏️  Lemma updated: {code}")

# Example: Statistics plugin
class StatsPlugin(CLUPlugin):
    def __init__(self):
        self.add_count = 0
        self.search_count = 0
    
    def on_lemma_added(self, code, lemma):
        self.add_count += 1
    
    def on_search(self, query, results):
        self.search_count += 1
    
    def report(self):
        print(f"Lemmas added: {self.add_count}")
        print(f"Searches performed: {self.search_count}")
```

---

## Deployment

### Production Deployment Checklist

- [ ] Use absolute paths for data files
- [ ] Set up automated backups
- [ ] Configure proper file permissions
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Document deployment procedures
- [ ] Create rollback plan
- [ ] Test backup restoration
- [ ] Configure environment variables
- [ ] Set up version control

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY clu.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /data

ENV CLU_DATA_FILE=/data/lemmas.json

CMD ["python", "clu.py", "--stats"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  clu:
    build: .
    volumes:
      - ./data:/data
    environment:
      - CLU_DATA_FILE=/data/lemmas.json
```

#### Deploy
```bash
docker-compose up -d
docker-compose exec clu python clu.py --stats
```

---

## Backup and Maintenance

### Backup Strategy

#### Daily Automated Backups
```python
# daily_backup.py
from backup_clu import backup_lemmas
import os
from datetime import datetime, timedelta

def cleanup_old_backups(backup_dir='backups', days=30):
    """Remove backups older than specified days"""
    cutoff = datetime.now() - timedelta(days=days)
    
    for filename in os.listdir(backup_dir):
        filepath = os.path.join(backup_dir, filename)
        if os.path.isfile(filepath):
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime < cutoff:
                os.remove(filepath)
                print(f"Removed old backup: {filename}")

if __name__ == '__main__':
    backup_lemmas()
    cleanup_old_backups()
```

### Maintenance Tasks

#### Weekly Health Check
```python
# health_check.py
from clu import CodedLemmaUtility
import json

def health_check(data_file='lemmas.json'):
    print("=== CLU Health Check ===\n")
    
    # Check file exists
    import os
    if not os.path.exists(data_file):
        print("❌ Data file not found")
        return False
    
    print(f"✅ Data file exists: {data_file}")
    
    # Check JSON validity
    try:
        with open(data_file) as f:
            data = json.load(f)
        print("✅ JSON is valid")
    except json.JSONDecodeError as e:
        print(f"❌ JSON is invalid: {e}")
        return False
    
    # Load with CLU
    try:
        clu = CodedLemmaUtility(data_file)
        stats = clu.get_statistics()
        print(f"✅ CLU loaded successfully")
        print(f"   Total lemmas: {stats['total_lemmas']}")
        print(f"   With proofs: {stats['with_proof']}")
    except Exception as e:
        print(f"❌ CLU load failed: {e}")
        return False
    
    # Check for orphaned dependencies
    orphans = []
    for code, lemma in clu.lemmas.items():
        for dep in lemma['dependencies']:
            if dep not in clu.lemmas:
                orphans.append((code, dep))
    
    if orphans:
        print(f"⚠️  Orphaned dependencies found: {len(orphans)}")
        for code, dep in orphans[:5]:
            print(f"   {code} -> {dep} (missing)")
    else:
        print("✅ No orphaned dependencies")
    
    print("\n=== Health Check Complete ===")
    return True

if __name__ == '__main__':
    health_check()
```

---

## Performance Tuning

### Large Collections (1000+ Lemmas)

#### Indexing Strategy
```python
# clu_indexed.py - Performance optimization for large collections
from clu import CodedLemmaUtility
from collections import defaultdict

class IndexedCLU(CodedLemmaUtility):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rebuild_indexes()
    
    def rebuild_indexes(self):
        """Build search indexes"""
        self.tag_index = defaultdict(set)
        self.category_index = defaultdict(set)
        
        for code, lemma in self.lemmas.items():
            # Index tags
            for tag in lemma['tags']:
                self.tag_index[tag].add(code)
            
            # Index category
            self.category_index[lemma['category']].add(code)
    
    def search_by_tag(self, tag):
        """Fast tag lookup using index"""
        codes = self.tag_index.get(tag, set())
        return {code: self.lemmas[code] for code in codes}
    
    def add_lemma(self, *args, **kwargs):
        """Override to update indexes"""
        code = super().add_lemma(*args, **kwargs)
        lemma = self.lemmas[code]
        
        for tag in lemma['tags']:
            self.tag_index[tag].add(code)
        self.category_index[lemma['category']].add(code)
        
        return code
```

### Memory Optimization

For very large collections, consider lazy loading:

```python
# clu_lazy.py
import json

class LazyCLU:
    """Lazy-loading version for very large collections"""
    
    def __init__(self, data_file):
        self.data_file = data_file
        self._index = self._build_index()
    
    def _build_index(self):
        """Build lightweight index without loading all data"""
        with open(self.data_file) as f:
            data = json.load(f)
        return {code: None for code in data['lemmas'].keys()}
    
    def get_lemma(self, code):
        """Load lemma on demand"""
        with open(self.data_file) as f:
            data = json.load(f)
        return data['lemmas'].get(code)
```

---

## Troubleshooting Integration Issues

### Common Integration Problems

**Problem**: Import errors
```
Solution: Ensure clu.py is in Python path or use absolute imports
export PYTHONPATH=/path/to/clu:$PYTHONPATH
```

**Problem**: File permission errors
```
Solution: Check file permissions and ownership
chmod 644 lemmas.json
chown user:group lemmas.json
```

**Problem**: Concurrent access issues
```
Solution: Implement file locking for multi-user access
Use the fcntl module on Unix or msvcrt on Windows
```

**Problem**: Large file performance
```
Solution: Use IndexedCLU or LazyCLU for large collections
Consider migrating to database backend
```

---

## Summary

The CLU system is highly flexible and can be integrated into various workflows:

1. **Standalone use**: Simple Python scripts
2. **Notebook integration**: Jupyter notebooks for interactive work
3. **Web applications**: REST APIs with Flask/Django
4. **Command-line tools**: CLI wrappers for automation
5. **Version control**: Git integration for collaboration
6. **Enterprise deployment**: Docker containers with automated backups

Choose the integration method that best fits the needs and scale.
