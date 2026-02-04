# Codified Lemma Utility (CLU)

A comprehensive Python utility for managing mathematical lemmas, theorems, and proofs with persistence, advanced search capabilities, and multiple export formats.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
  - [Creating Lemmas](#creating-lemmas)
  - [Managing Dependencies](#managing-dependencies)
  - [Searching](#searching)
  - [Exporting](#exporting)
- [API Reference](#api-reference)
- [Command Line Interface](#command-line-interface)
- [Examples](#examples)
- [File Formats](#file-formats)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Overview

The Codified Lemma Utility (CLU) is designed to help mathematicians, researchers, and students organize and manage mathematical lemmas, theorems, and their proofs in a structured, searchable, and persistent manner.

Each lemma is assigned a unique code (e.g., `L1000`, `L1001`) and can include:
- A statement
- A proof
- Tags for categorization
- A category
- Notes
- Dependencies on other lemmas
- Metadata (creation/modification timestamps)

## Features

### Core Functionality
- **Automatic Code Generation**: Each lemma receives a unique identifier
- **Persistent Storage**: All data saved to JSON files
- **Dependency Tracking**: Link lemmas that depend on each other
- **Rich Metadata**: Track creation and modification times

### Search Capabilities
- **Text Search**: Search in statements, proofs, and notes
- **Regex Support**: Advanced pattern matching
- **Tag-based Search**: Find lemmas by tags
- **Category Filtering**: Filter by category
- **Proof Status**: Filter by presence/absence of proofs
- **Combined Filters**: Use multiple search criteria simultaneously

### Export Formats
- **Plain Text**: Simple, readable format
- **Markdown**: Perfect for documentation and GitHub
- **LaTeX**: Ready for academic papers
- **JSON**: Machine-readable format for data exchange

### Advanced Features
- **Dependency Chains**: Automatically trace all dependencies
- **Dependent Tracking**: Find which lemmas depend on a given lemma
- **Statistics**: Get insights about your lemma collection
- **Import/Export**: Share lemma collections
- **Update/Delete**: Modify or remove existing lemmas

## Installation

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only standard library)

### Setup

1. **Download the files**:
   ```bash
   # clone this repo
   git clone https://github.com/suboksy/clu.git
   ```

2. **Verify installation**:
   ```bash
   python clu.py --stats
   ```

3. **Optional: Create a virtual environment**:
   ```bash
   python -m venv clu_env
   source clu_env/bin/activate  # On Windows: clu_env\Scripts\activate
   ```

## Quick Start

### Basic Python Usage

```python
from clu import CodedLemmaUtility

# Initialize the utility
clu = CodedLemmaUtility()

# Add a lemma
code = clu.add_lemma(
    statement="For all integers n, n + 0 = n",
    proof="By the identity property of addition",
    tags=["arithmetic", "basic"],
    category="algebra"
)

print(f"Created lemma: {code}")

# Search for lemmas
results = clu.search(tags=["arithmetic"])
for code, lemma in results.items():
    print(f"{code}: {lemma['statement']}")

# Export to Markdown
markdown = clu.export_all('markdown', 'my_lemmas.md')
```

### Command Line Usage

```bash
# Show statistics
python clu.py --stats

# Export all lemmas to Markdown
python clu.py --export markdown --output lemmas.md

# Export to LaTeX
python clu.py --export latex --output lemmas.tex

# Use a different data file
python clu.py --file my_lemmas.json --stats
```

## Usage Guide

### Creating Lemmas

```python
# Basic lemma
code = clu.add_lemma(
    statement="The square of any real number is non-negative"
)

# Complete lemma with all fields
code = clu.add_lemma(
    statement="For all real x, x² ≥ 0",
    proof="For any real x, x² = x·x. The product of two numbers with "
          "the same sign is positive, and x and x have the same sign.",
    tags=["real_analysis", "inequality", "basic"],
    category="analysis",
    notes="Fundamental property used in many proofs"
)

# Retrieve a lemma
lemma = clu.get_lemma(code)
print(lemma['statement'])
```

### Updating and Deleting Lemmas

```python
# Update a lemma
clu.update_lemma(
    code,
    proof="Updated proof with more detail...",
    tags=["real_analysis", "inequality", "fundamental"]
)

# Delete a lemma
clu.delete_lemma(code)
```

### Managing Dependencies

```python
# Add lemmas
l1 = clu.add_lemma("Lemma 1: Basic property")
l2 = clu.add_lemma("Lemma 2: Follows from Lemma 1")
l3 = clu.add_lemma("Theorem: Uses both previous lemmas")

# Create dependency relationships
clu.add_dependency(l2, l1)  # l2 depends on l1
clu.add_dependency(l3, l1)  # l3 depends on l1
clu.add_dependency(l3, l2)  # l3 depends on l2

# Get all dependencies (recursive)
deps = clu.get_dependency_chain(l3)
print(f"L3 depends on: {deps}")  # Output: ['L1000', 'L1001']

# Find what depends on a lemma
dependents = clu.get_dependents(l1)
print(f"Lemmas depending on L1: {dependents}")  # Output: ['L1001', 'L1002']

# Remove a dependency
clu.remove_dependency(l3, l2)
```

### Searching

#### Simple Text Search
```python
# Search in statements and proofs
results = clu.search(query="induction")
```

#### Tag-based Search
```python
# Find all lemmas with specific tags (must have ALL tags)
results = clu.search(tags=["arithmetic", "basic"])

# Find lemmas with a single tag
results = clu.search_by_tag("algebra")
```

#### Category Filter
```python
# Find all lemmas in a category
results = clu.search(category="number_theory")
```

#### Proof Status Filter
```python
# Find lemmas with proofs
results = clu.search(has_proof=True)

# Find lemmas without proofs (TODO items)
results = clu.search(has_proof=False)
```

#### Regex Search
```python
# Use regular expressions
results = clu.search(query=r"\bsum\b.*\bn\b", regex=True)
```

#### Combined Search
```python
# Combine multiple criteria
results = clu.search(
    query="triangle",
    category="geometry",
    tags=["pythagorean"],
    has_proof=True
)
```

### Exporting

#### Export Single Lemma
```python
# Export in different formats
text = clu.export_lemma(code, format='text')
markdown = clu.export_lemma(code, format='markdown')
latex = clu.export_lemma(code, format='latex')
json_str = clu.export_lemma(code, format='json')

print(markdown)
```

#### Export All Lemmas
```python
# Export to file
clu.export_all('markdown', 'all_lemmas.md')
clu.export_all('latex', 'all_lemmas.tex')
clu.export_all('json', 'backup.json')

# Get content without saving
content = clu.export_all('markdown')
print(content)
```

### Statistics and Overview

```python
# Get collection statistics
stats = clu.get_statistics()
print(f"Total lemmas: {stats['total_lemmas']}")
print(f"With proofs: {stats['with_proof']}")
print(f"Categories: {stats['categories']}")
print(f"Tags: {stats['tags']}")

# List all categories
categories = clu.list_categories()
for cat, count in categories.items():
    print(f"{cat}: {count} lemmas")

# List all tags
tags = clu.list_tags()
for tag, count in sorted(tags.items(), key=lambda x: -x[1]):
    print(f"{tag}: {count} uses")

# Get all lemmas (code: statement pairs)
all_lemmas = clu.list_all()
```

### Importing Data

```python
# Import lemmas from another JSON file
clu.import_from_json('imported_lemmas.json')

# Load from a different data file
clu2 = CodedLemmaUtility('alternate_collection.json')
```

## API Reference

### Class: CodedLemmaUtility

#### Constructor
```python
CodedLemmaUtility(data_file: str = "lemmas.json")
```
Initialize the utility with optional data file path.

#### Methods

##### Lemma Management
- `add_lemma(statement, proof=None, tags=None, category=None, notes=None) -> str`
- `get_lemma(code) -> Optional[Dict]`
- `update_lemma(code, **kwargs) -> bool`
- `delete_lemma(code) -> bool`

##### Dependency Management
- `add_dependency(code, depends_on) -> bool`
- `remove_dependency(code, depends_on) -> bool`
- `get_dependency_chain(code) -> List[str]`
- `get_dependents(code) -> List[str]`

##### Search
- `search(query=None, tags=None, category=None, has_proof=None, regex=False) -> Dict`
- `search_by_tag(tag) -> Dict`

##### Export
- `export_lemma(code, format='text') -> Optional[str]`
- `export_all(format='markdown', filename=None) -> str`

##### Information
- `list_all() -> Dict[str, str]`
- `list_categories() -> Dict[str, int]`
- `list_tags() -> Dict[str, int]`
- `get_statistics() -> Dict[str, Any]`

##### Persistence
- `save() -> bool`
- `load() -> bool`
- `import_from_json(filename) -> bool`

## Command Line Interface

```bash
# Show help
python clu.py --help

# Show statistics
python clu.py --stats

# Export to different formats
python clu.py --export markdown --output lemmas.md
python clu.py --export latex --output paper.tex
python clu.py --export json --output backup.json
python clu.py --export text --output notes.txt

# Use a specific data file
python clu.py --file my_collection.json --stats
python clu.py --file my_collection.json --export markdown
```

## Examples

### Example 1: Building a Number Theory Collection

```python
from clu import CodedLemmaUtility

clu = CodedLemmaUtility('number_theory.json')

# Fundamental theorem of arithmetic
fta = clu.add_lemma(
    statement="Every integer greater than 1 can be represented uniquely "
              "as a product of prime numbers",
    proof="Proof by strong induction...",
    category="number_theory",
    tags=["fundamental", "primes", "factorization"]
)

# Euclid's lemma
euclid = clu.add_lemma(
    statement="If p is prime and p divides ab, then p divides a or p divides b",
    proof="Assume p divides ab but p does not divide a...",
    category="number_theory",
    tags=["primes", "divisibility"]
)

# Show dependency
clu.add_dependency(fta, euclid)

# Export
clu.export_all('markdown', 'number_theory_lemmas.md')
```

### Example 2: Tracking TODO Lemmas

```python
# Find all lemmas without proofs
todo = clu.search(has_proof=False)

print(f"Lemmas needing proofs: {len(todo)}")
for code, lemma in todo.items():
    print(f"\n{code}: {lemma['statement']}")
    print(f"Category: {lemma['category']}")
    print(f"Tags: {', '.join(lemma['tags'])}")
```

### Example 3: Category Analysis

```python
# Analyze your collection by category
categories = clu.list_categories()

print("Collection Overview:")
for category, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"\n{category}: {count} lemmas")
    
    # Find lemmas with most dependencies in this category
    cat_lemmas = clu.search(category=category)
    for code, lemma in cat_lemmas.items():
        dep_count = len(lemma['dependencies'])
        if dep_count > 0:
            print(f"  {code}: {dep_count} dependencies")
```

## File Formats

### JSON Storage Format

```json
{
  "metadata": {
    "created": "2024-01-01T12:00:00",
    "last_modified": "2024-01-02T15:30:00",
    "version": "1.0.0"
  },
  "code_counter": 1003,
  "lemmas": {
    "L1000": {
      "statement": "For all integers n, n + 0 = n",
      "proof": "By the identity property of addition",
      "tags": ["arithmetic", "basic"],
      "category": "algebra",
      "notes": "",
      "dependencies": [],
      "created": "2024-01-01T12:00:00",
      "modified": "2024-01-01T12:00:00"
    }
  }
}
```

### Markdown Export Format

```markdown
## L1000

**Category:** algebra

**Statement:** For all integers n, n + 0 = n

**Proof:**

By the identity property of addition

**Tags:** `arithmetic`, `basic`

*Created: 2024-01-01T12:00:00*

*Modified: 2024-01-01T12:00:00*
```

### LaTeX Export Format

```latex
\begin{lemma}[L1000]
\label{lemma:L1000}
For all integers n, n + 0 = n
\end{lemma}

\begin{proof}
By the identity property of addition
\end{proof}

% Tags: arithmetic, basic
```

## Best Practices

### Organization
1. **Use consistent categories**: Define a category scheme before starting
2. **Tag generously**: Use multiple tags for better searchability
3. **Write clear statements**: Make statements precise and unambiguous
4. **Document dependencies**: Always link related lemmas
5. **Add notes**: Include context, applications, or historical notes

### Workflow
1. **Start with basic lemmas**: Build foundational results first
2. **Add proofs gradually**: Mark lemmas without proofs for later completion
3. **Regular exports**: Backup your collection regularly
4. **Review dependencies**: Periodically check dependency chains for accuracy
5. **Use statistics**: Monitor collection growth and coverage

### Naming Conventions
- **Categories**: Use lowercase with underscores (e.g., `number_theory`, `linear_algebra`)
- **Tags**: Use lowercase, descriptive words (e.g., `fundamental`, `geometric`)
- **Statements**: Write in mathematical notation when appropriate

### Data Safety
1. **Regular backups**: Export to JSON regularly
2. **Version control**: Consider using git for your JSON files
3. **Multiple collections**: Use separate files for different subjects
4. **Test imports**: Verify imported data before merging

## Troubleshooting

### Common Issues

**Problem**: "File not found" error
```
Solution: Check that the data file path is correct. The utility creates
a new file if none exists, so this usually indicates a permissions issue.
```

**Problem**: Lemmas not saving
```
Solution: Ensure you have write permissions in the directory. Check that
the save() method returns True. Verify the JSON file is not corrupted.
```

**Problem**: Search returns no results
```
Solution: Check your search criteria. Remember that tag search requires
ALL specified tags to be present. Try broader search terms.
```

**Problem**: Import fails
```
Solution: Validate the JSON file format. Ensure it matches the expected
structure. Check for duplicate codes.
```

### Error Messages

- **"Error saving data"**: Check file permissions and disk space
- **"Error loading data"**: JSON file may be corrupted; restore from backup
- **"Error importing data"**: Source file format is incorrect

### Getting Help

For issues or questions:
1. Check this README
2. Review the CONFIG.md file for setup instructions
3. Examine the example code in `clu.py`
4. Check the source code comments for detailed explanations

## License

This utility is provided as-is for educational and research purposes.

## Version History

- **1.0.0** (2024): Initial release
  - Core lemma management
  - Persistence with JSON
  - Multiple export formats
  - Advanced search capabilities
  - Dependency tracking

## Contributing

Suggestions for improvements:
- Additional export formats (e.g., HTML, CSV)
- Graphical visualization of dependencies
- Web interface
- Collaborative features
- Integration with theorem provers
- Import from LaTeX documents
