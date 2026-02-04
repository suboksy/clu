"""
Codified Lemma Utility (CLU)
A comprehensive system for managing mathematical lemmas, theorems, and proofs
with persistence, advanced search, and multiple export formats.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Set, Any
import re


class CodedLemmaUtility:
    """
    Main class for the Codified Lemma Utility.
    Manages lemmas with persistence, search, and export capabilities.
    """
    
    def __init__(self, data_file: str = "lemmas.json"):
        """
        Initialize the utility.
        
        Args:
            data_file: Path to the JSON file for persistence
        """
        self.data_file = data_file
        self.lemmas = {}
        self.code_counter = 1000
        self.metadata = {
            'created': datetime.now().isoformat(),
            'last_modified': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        self.load()
    
    def add_lemma(self, statement: str, proof: Optional[str] = None, 
                  tags: Optional[List[str]] = None, 
                  category: Optional[str] = None,
                  notes: Optional[str] = None) -> str:
        """
        Add a new lemma to the utility.
        
        Args:
            statement: The lemma statement
            proof: Proof or justification
            tags: Tags for categorization
            category: Primary category
            notes: Additional notes
            
        Returns:
            The assigned code for the lemma
        """
        code = f"L{self.code_counter}"
        self.code_counter += 1
        
        self.lemmas[code] = {
            'statement': statement,
            'proof': proof or '',
            'tags': tags or [],
            'category': category or 'general',
            'notes': notes or '',
            'dependencies': [],
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }
        
        self.metadata['last_modified'] = datetime.now().isoformat()
        self.save()
        return code
    
    def get_lemma(self, code: str) -> Optional[Dict[str, Any]]:
        """Retrieve a lemma by its code."""
        return self.lemmas.get(code)
    
    def update_lemma(self, code: str, **kwargs) -> bool:
        """
        Update an existing lemma.
        
        Args:
            code: The lemma code
            **kwargs: Fields to update (statement, proof, tags, category, notes)
            
        Returns:
            True if successful, False otherwise
        """
        if code not in self.lemmas:
            return False
        
        allowed_fields = ['statement', 'proof', 'tags', 'category', 'notes']
        for field, value in kwargs.items():
            if field in allowed_fields:
                self.lemmas[code][field] = value
        
        self.lemmas[code]['modified'] = datetime.now().isoformat()
        self.metadata['last_modified'] = datetime.now().isoformat()
        self.save()
        return True
    
    def delete_lemma(self, code: str) -> bool:
        """
        Delete a lemma.
        
        Args:
            code: The lemma code
            
        Returns:
            True if successful, False otherwise
        """
        if code not in self.lemmas:
            return False
        
        # Remove dependencies from other lemmas
        for lemma_code, lemma_data in self.lemmas.items():
            if code in lemma_data['dependencies']:
                lemma_data['dependencies'].remove(code)
        
        del self.lemmas[code]
        self.metadata['last_modified'] = datetime.now().isoformat()
        self.save()
        return True
    
    def add_dependency(self, code: str, depends_on: str) -> bool:
        """
        Record that one lemma depends on another.
        
        Args:
            code: The dependent lemma code
            depends_on: The lemma it depends on
            
        Returns:
            True if successful, False otherwise
        """
        if code in self.lemmas and depends_on in self.lemmas:
            if depends_on not in self.lemmas[code]['dependencies']:
                self.lemmas[code]['dependencies'].append(depends_on)
                self.lemmas[code]['modified'] = datetime.now().isoformat()
                self.save()
            return True
        return False
    
    def remove_dependency(self, code: str, depends_on: str) -> bool:
        """Remove a dependency relationship."""
        if code in self.lemmas and depends_on in self.lemmas[code]['dependencies']:
            self.lemmas[code]['dependencies'].remove(depends_on)
            self.save()
            return True
        return False
    
    def search(self, query: Optional[str] = None, 
               tags: Optional[List[str]] = None,
               category: Optional[str] = None,
               has_proof: Optional[bool] = None,
               regex: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        Advanced search functionality.
        
        Args:
            query: Text to search in statement and proof
            tags: List of tags (lemma must have ALL tags)
            category: Category to filter by
            has_proof: Filter by proof existence
            regex: Use regex for query matching
            
        Returns:
            Dictionary of matching lemmas
        """
        results = {}
        
        for code, lemma in self.lemmas.items():
            # Check category
            if category and lemma['category'] != category:
                continue
            
            # Check proof existence
            if has_proof is not None:
                has_lemma_proof = bool(lemma['proof'])
                if has_lemma_proof != has_proof:
                    continue
            
            # Check tags (must have all specified tags)
            if tags:
                if not all(tag in lemma['tags'] for tag in tags):
                    continue
            
            # Check query text
            if query:
                search_text = f"{lemma['statement']} {lemma['proof']} {lemma.get('notes', '')}"
                
                if regex:
                    try:
                        if not re.search(query, search_text, re.IGNORECASE):
                            continue
                    except re.error:
                        # Invalid regex, skip this filter
                        pass
                else:
                    if query.lower() not in search_text.lower():
                        continue
            
            results[code] = lemma
        
        return results
    
    def search_by_tag(self, tag: str) -> Dict[str, Dict[str, Any]]:
        """Find all lemmas with a specific tag."""
        return {code: lemma for code, lemma in self.lemmas.items() 
                if tag in lemma['tags']}
    
    def get_dependency_chain(self, code: str) -> List[str]:
        """
        Get all lemmas that a given lemma depends on (recursively).
        
        Args:
            code: The lemma code
            
        Returns:
            List of dependency codes
        """
        if code not in self.lemmas:
            return []
        
        chain = set()
        to_process = [code]
        
        while to_process:
            current = to_process.pop()
            if current in chain:
                continue
            chain.add(current)
            to_process.extend(self.lemmas[current]['dependencies'])
        
        chain.discard(code)  # Remove the original lemma
        return sorted(list(chain))
    
    def get_dependents(self, code: str) -> List[str]:
        """
        Get all lemmas that depend on the given lemma.
        
        Args:
            code: The lemma code
            
        Returns:
            List of dependent lemma codes
        """
        dependents = []
        for lemma_code, lemma_data in self.lemmas.items():
            if code in lemma_data['dependencies']:
                dependents.append(lemma_code)
        return sorted(dependents)
    
    def list_all(self) -> Dict[str, str]:
        """List all lemma codes and statements."""
        return {code: lemma['statement'] for code, lemma in self.lemmas.items()}
    
    def list_categories(self) -> Dict[str, int]:
        """List all categories with lemma counts."""
        categories = {}
        for lemma in self.lemmas.values():
            cat = lemma['category']
            categories[cat] = categories.get(cat, 0) + 1
        return categories
    
    def list_tags(self) -> Dict[str, int]:
        """List all tags with usage counts."""
        tags = {}
        for lemma in self.lemmas.values():
            for tag in lemma['tags']:
                tags[tag] = tags.get(tag, 0) + 1
        return tags
    
    def export_lemma(self, code: str, format: str = 'text') -> Optional[str]:
        """
        Export a single lemma in the specified format.
        
        Args:
            code: The lemma code
            format: Export format ('text', 'markdown', 'latex', 'json')
            
        Returns:
            Formatted string or None if lemma not found
        """
        if code not in self.lemmas:
            return None
        
        lemma = self.lemmas[code]
        
        if format == 'text':
            return self._export_text(code, lemma)
        elif format == 'markdown':
            return self._export_markdown(code, lemma)
        elif format == 'latex':
            return self._export_latex(code, lemma)
        elif format == 'json':
            return json.dumps({code: lemma}, indent=2)
        else:
            return self._export_text(code, lemma)
    
    def _export_text(self, code: str, lemma: Dict[str, Any]) -> str:
        """Export in plain text format."""
        output = f"Code: {code}\n"
        output += f"Category: {lemma['category']}\n"
        output += f"Statement: {lemma['statement']}\n"
        if lemma['proof']:
            output += f"Proof: {lemma['proof']}\n"
        if lemma['tags']:
            output += f"Tags: {', '.join(lemma['tags'])}\n"
        if lemma['notes']:
            output += f"Notes: {lemma['notes']}\n"
        if lemma['dependencies']:
            output += f"Depends on: {', '.join(lemma['dependencies'])}\n"
        output += f"Created: {lemma['created']}\n"
        output += f"Modified: {lemma['modified']}\n"
        return output
    
    def _export_markdown(self, code: str, lemma: Dict[str, Any]) -> str:
        """Export in Markdown format."""
        output = f"## {code}\n\n"
        output += f"**Category:** {lemma['category']}\n\n"
        output += f"**Statement:** {lemma['statement']}\n\n"
        if lemma['proof']:
            output += f"**Proof:**\n\n{lemma['proof']}\n\n"
        if lemma['tags']:
            output += f"**Tags:** {', '.join(f'`{tag}`' for tag in lemma['tags'])}\n\n"
        if lemma['notes']:
            output += f"**Notes:** {lemma['notes']}\n\n"
        if lemma['dependencies']:
            output += f"**Dependencies:** {', '.join(f'[{dep}](#{dep})' for dep in lemma['dependencies'])}\n\n"
        output += f"*Created: {lemma['created']}*\n\n"
        output += f"*Modified: {lemma['modified']}*\n\n"
        return output
    
    def _export_latex(self, code: str, lemma: Dict[str, Any]) -> str:
        """Export in LaTeX format."""
        output = f"\\begin{{lemma}}[{code}]\n"
        output += f"\\label{{lemma:{code}}}\n"
        output += f"{lemma['statement']}\n"
        output += "\\end{lemma}\n\n"
        if lemma['proof']:
            output += "\\begin{proof}\n"
            output += f"{lemma['proof']}\n"
            output += "\\end{proof}\n\n"
        if lemma['tags']:
            output += f"% Tags: {', '.join(lemma['tags'])}\n"
        if lemma['notes']:
            output += f"% Notes: {lemma['notes']}\n"
        return output
    
    def export_all(self, format: str = 'markdown', filename: Optional[str] = None) -> str:
        """
        Export all lemmas in the specified format.
        
        Args:
            format: Export format ('text', 'markdown', 'latex', 'json')
            filename: Optional filename to save to
            
        Returns:
            The exported content
        """
        if format == 'json':
            content = json.dumps({
                'metadata': self.metadata,
                'lemmas': self.lemmas
            }, indent=2)
        else:
            content = ""
            if format == 'markdown':
                content = "# Codified Lemma Collection\n\n"
                content += f"Generated: {datetime.now().isoformat()}\n\n"
                content += f"Total Lemmas: {len(self.lemmas)}\n\n"
                content += "---\n\n"
            elif format == 'latex':
                content = "\\documentclass{article}\n"
                content += "\\usepackage{amsthm}\n"
                content += "\\newtheorem{lemma}{Lemma}\n"
                content += "\\begin{document}\n\n"
            
            for code in sorted(self.lemmas.keys()):
                content += self.export_lemma(code, format) + "\n"
            
            if format == 'latex':
                content += "\\end{document}\n"
        
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return content
    
    def save(self) -> bool:
        """
        Save lemmas to JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {
                'metadata': self.metadata,
                'code_counter': self.code_counter,
                'lemmas': self.lemmas
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load(self) -> bool:
        """
        Load lemmas from JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(self.data_file):
            return False
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.metadata = data.get('metadata', self.metadata)
            self.code_counter = data.get('code_counter', self.code_counter)
            self.lemmas = data.get('lemmas', {})
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def import_from_json(self, filename: str) -> bool:
        """
        Import lemmas from another JSON file.
        
        Args:
            filename: Path to JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            imported_lemmas = data.get('lemmas', {})
            for code, lemma in imported_lemmas.items():
                if code not in self.lemmas:
                    self.lemmas[code] = lemma
                    # Update counter if needed
                    try:
                        code_num = int(code[1:])
                        if code_num >= self.code_counter:
                            self.code_counter = code_num + 1
                    except ValueError:
                        pass
            
            self.save()
            return True
        except Exception as e:
            print(f"Error importing data: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the lemma collection."""
        total_lemmas = len(self.lemmas)
        with_proof = sum(1 for l in self.lemmas.values() if l['proof'])
        with_dependencies = sum(1 for l in self.lemmas.values() if l['dependencies'])
        
        return {
            'total_lemmas': total_lemmas,
            'with_proof': with_proof,
            'without_proof': total_lemmas - with_proof,
            'with_dependencies': with_dependencies,
            'categories': self.list_categories(),
            'tags': self.list_tags(),
            'created': self.metadata['created'],
            'last_modified': self.metadata['last_modified'],
            'version': self.metadata['version']
        }


def main():
    """Example usage and CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Codified Lemma Utility')
    parser.add_argument('--file', default='lemmas.json', help='Data file path')
    parser.add_argument('--export', choices=['text', 'markdown', 'latex', 'json'], 
                       help='Export all lemmas in specified format')
    parser.add_argument('--output', help='Output filename for export')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    clu = CodedLemmaUtility(args.file)
    
    if args.stats:
        stats = clu.get_statistics()
        print("=== CLU Statistics ===")
        print(f"Total Lemmas: {stats['total_lemmas']}")
        print(f"With Proof: {stats['with_proof']}")
        print(f"Without Proof: {stats['without_proof']}")
        print(f"With Dependencies: {stats['with_dependencies']}")
        print(f"\nCategories: {stats['categories']}")
        print(f"\nTags: {stats['tags']}")
        return
    
    if args.export:
        content = clu.export_all(args.export, args.output)
        if not args.output:
            print(content)
        else:
            print(f"Exported to {args.output}")
        return
    
    # Interactive demo
    print("=== Codified Lemma Utility Demo ===\n")
    
    l1 = clu.add_lemma(
        "For all integers n, n + 0 = n",
        proof="By the identity property of addition",
        tags=["arithmetic", "basic", "identity"],
        category="algebra"
    )
    
    l2 = clu.add_lemma(
        "For all integers a, b: a + b = b + a",
        proof="By the commutative property of addition",
        tags=["arithmetic", "commutative"],
        category="algebra"
    )
    
    l3 = clu.add_lemma(
        "Sum of first n natural numbers = n(n+1)/2",
        proof="By mathematical induction using base case n=1 and inductive step",
        tags=["series", "induction"],
        category="number_theory",
        notes="Classic result used in many complexity analyses"
    )
    
    clu.add_dependency(l3, l1)
    clu.add_dependency(l3, l2)
    
    print("Added 3 sample lemmas")
    print("\nAll lemmas:")
    for code, statement in clu.list_all().items():
        print(f"  {code}: {statement}")
    
    print(f"\n\n{clu.export_lemma(l3, 'markdown')}")
    
    print("Search for 'induction':")
    results = clu.search(query="induction")
    for code in results:
        print(f"  {code}: {results[code]['statement']}")


if __name__ == "__main__":
    main()
