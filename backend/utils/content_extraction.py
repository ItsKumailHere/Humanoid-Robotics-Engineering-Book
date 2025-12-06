# Content Extraction and Parsing Module
# Extracts content from Docusaurus MDX files for RAG processing

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
import frontmatter  # For parsing markdown frontmatter

@dataclass
class ParsedChapter:
    """Represents a parsed chapter with its content and metadata"""
    id: str
    title: str
    description: str
    content: str
    learning_objectives: List[str]
    sections: List[Dict[str, str]]  # {title: content}
    exercises: List[Dict[str, Any]]
    summary: str
    references: List[str]
    sidebar_position: int

class ContentExtractor:
    """Extracts and parses content from Docusaurus MDX files"""

    def __init__(self, docs_path: str = None):
        """Initialize with path to chapters directory"""
        if docs_path:
            # If explicit path is provided, use it
            self.docs_path = Path(docs_path)
        else:
            # Try to determine the correct path based on the current working directory
            # First try from current working directory
            cwd_chapters_path = Path("frontend/docs/Chapters")
            if cwd_chapters_path.exists() and cwd_chapters_path.is_dir():
                self.docs_path = cwd_chapters_path
            else:
                # Try relative to this file (one level up from utils, then frontend)
                file_dir = Path(__file__).parent  # backend/utils
                fallback_path = file_dir.parent / "frontend" / "docs" / "Chapters"  # backend/frontend/docs/Chapters
                if fallback_path.exists() and fallback_path.is_dir():
                    self.docs_path = fallback_path
                else:
                    # Try one more level up from where the script might be called
                    fallback_path = Path("../frontend/docs/Chapters")
                    if fallback_path.exists() and fallback_path.is_dir():
                        self.docs_path = fallback_path
                    else:
                        print(f"ERROR: Could not find chapters directory at any expected location:")
                        print(f"  - {cwd_chapters_path.absolute()}")
                        print(f"  - {Path('frontend/docs/Chapters').absolute()} (relative to cwd)")
                        print(f"  - {fallback_path.absolute()}")
                        print("Defaulting to './frontend/docs/Chapters' - please verify directory exists.")
                        self.docs_path = Path("frontend/docs/Chapters")  # Default path

        print(f"ContentExtractor initialized with path: {self.docs_path.absolute()}")
    
    def extract_all_chapters(self) -> List[ParsedChapter]:
        """Extract content from all chapter files"""
        chapters = []
        
        for mdx_file in self.docs_path.glob("*.mdx"):
            chapter = self.extract_chapter(mdx_file)
            if chapter:
                chapters.append(chapter)
        
        return chapters
    
    def extract_chapter(self, file_path: Path) -> ParsedChapter:
        """Extract content from a single chapter file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        fm = frontmatter.loads(content)
        frontmatter_data = fm.metadata
        
        # Extract content without frontmatter
        main_content = fm.content
        
        # Parse the main content into sections
        sections = self._parse_content_into_sections(main_content)
        
        # Extract learning objectives
        learning_objectives = self._extract_learning_objectives(main_content)
        
        # Extract exercises
        exercises = self._extract_exercises(main_content)
        
        # Extract summary
        summary = self._extract_summary(main_content)
        
        # Extract references
        references = self._extract_references(main_content)
        
        # Create ParsedChapter object
        chapter = ParsedChapter(
            id=frontmatter_data.get('id', file_path.stem),
            title=frontmatter_data.get('title', ''),
            description=frontmatter_data.get('description', ''),
            content=main_content,
            learning_objectives=learning_objectives,
            sections=sections,
            exercises=exercises,
            summary=summary,
            references=references,
            sidebar_position=frontmatter_data.get('sidebar_position', 0)
        )
        
        return chapter
    
    def _parse_content_into_sections(self, content: str) -> List[Dict[str, str]]:
        """Parse content into sections based on H2 headers"""
        # Pattern to match H2 headers and their content until the next H2
        pattern = r'##\s+(.+?)(?=\n##\s+|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)
        
        sections = []
        for match in matches:
            # Split header and content
            if '\n' in match:
                header, section_content = match.split('\n', 1)
                header = header.strip()
                section_content = section_content.strip()
            else:
                header = match.strip()
                section_content = ""
            
            sections.append({
                'title': header,
                'content': section_content
            })
        
        return sections
    
    def _extract_learning_objectives(self, content: str) -> List[str]:
        """Extract learning objectives from the Learning Objectives section"""
        # Find the Learning Objectives section
        pattern = r'## Learning Objectives\s*([\s\S]*?)(?=\n##\s|\Z)'
        match = re.search(pattern, content)
        
        if not match:
            return []
        
        section_content = match.group(1)
        
        # Extract list items
        objectives = []
        list_pattern = r'^\s*[-*]\s+(.+)$'
        matches = re.findall(list_pattern, section_content, re.MULTILINE)
        
        for obj in matches:
            objectives.append(obj.strip())
        
        return objectives
    
    def _extract_exercises(self, content: str) -> List[Dict[str, Any]]:
        """Extract exercises from the Exercises section"""
        exercises = []
        
        # Pattern for regular exercises (Exercise 1, Exercise 2, etc.)
        exercise_pattern = r'### Exercise \d+\s*([\s\S]*?)(?=<details>|<ExerciseComponent|\Z)'
        exercise_matches = re.findall(exercise_pattern, content)
        
        for i, ex_content in enumerate(exercise_matches):
            exercise = {
                'id': f'ex_{i+1}',
                'type': 'regular',
                'question': ex_content.strip()
            }
            exercises.append(exercise)
        
        # Pattern for interactive exercises
        interactive_pattern = r'<ExerciseComponent[\s\S]*?exercise={[\s\S]*?id:\s*[\'"]([^\'"]+)[\'"][\s\S]*?type:\s*[\'"]([^\'"]+)[\'"][\s\S]*?question:\s*[\'"]([^\'"]+)[\'"][\s\S]*?solution:\s*[\'"]([^\'"]+)[\'"][\s\S]*?}[\s\S]*?/>'
        interactive_matches = re.findall(interactive_pattern, content)
        
        for ex_id, ex_type, question, solution in interactive_matches:
            exercise = {
                'id': ex_id,
                'type': ex_type,
                'question': question,
                'solution': solution
            }
            exercises.append(exercise)
        
        return exercises
    
    def _extract_summary(self, content: str) -> str:
        """Extract summary from the Summary section"""
        pattern = r'## Summary\s*([\s\S]*?)(?=\n##\s|\Z)'
        match = re.search(pattern, content)
        
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_references(self, content: str) -> List[str]:
        """Extract references from the References section"""
        pattern = r'## References\s*([\s\S]*?)(?=\n##\s|\Z)'
        match = re.search(pattern, content)
        
        if not match:
            return []
        
        refs_content = match.group(1)
        # Extract reference links
        ref_pattern = r'- \[([^\]]+)\]\(([^)]+)\)'
        refs = re.findall(ref_pattern, refs_content)
        
        references = [f'[{title}]({url})' for title, url in refs]
        return references

# Example usage and testing
def test_content_extraction():
    """Test function to validate content extraction"""
    extractor = ContentExtractor()
    chapters = extractor.extract_all_chapters()
    
    print(f"Extracted {len(chapters)} chapters")
    
    for chapter in chapters[:2]:  # Show first 2 chapters
        print(f"\nChapter: {chapter.title}")
        print(f"  ID: {chapter.id}")
        print(f"  Objectives: {len(chapter.learning_objectives)}")
        print(f"  Sections: {len(chapter.sections)}")
        print(f"  Exercises: {len(chapter.exercises)}")
        print(f"  References: {len(chapter.references)}")
    
    return chapters

if __name__ == "__main__":
    test_content_extraction()