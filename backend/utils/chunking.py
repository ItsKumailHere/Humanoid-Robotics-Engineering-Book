# Content Chunking and Preprocessing Pipeline
# For preparing textbook content for RAG system

import re
from typing import List, Dict, Any
from dataclasses import dataclass
from backend.database.config import DBConfig

@dataclass
class ContentChunk:
    """Represents a chunk of content with metadata"""
    id: str
    text: str
    chunk_type: str  # 'text', 'code', 'exercise', 'example', 'diagram', 'summary', etc.
    chapter_id: str
    section: str
    position: int
    metadata: Dict[str, Any]

class ContentChunker:
    """Handles the chunking of textbook content into processable pieces"""
    
    def __init__(self, config: DBConfig = DBConfig()):
        self.max_chunk_size = config.MAX_CHUNK_SIZE
        self.min_chunk_size = config.MIN_CHUNK_SIZE
        self.chunk_overlap = config.CHUNK_OVERLAP
    
    def chunk_chapter(self, chapter_id: str, content: str) -> List[ContentChunk]:
        """Chunk a chapter's content into processable pieces"""
        sections = self._split_by_sections(content)
        chunks = []
        
        for i, section in enumerate(sections):
            section_chunks = self._chunk_section(section, chapter_id, f"section-{i+1}")
            chunks.extend(section_chunks)
        
        return chunks
    
    def _split_by_sections(self, content: str) -> List[str]:
        """Split content by H2 sections (## in markdown)"""
        # Pattern to identify section headers
        section_pattern = r'(##\s+[^\n]+)'
        
        # Split content by section headers, keeping the headers
        parts = re.split(f'({section_pattern})', content)
        
        # Rejoin headers with their content
        sections = []
        for i in range(1, len(parts), 2):  # Start from index 1, step by 2
            if i + 1 < len(parts):
                section_header = parts[i].strip()
                section_content = parts[i + 1].strip()
                sections.append(f"{section_header}\n{section_content}")
        
        # If no sections found, treat entire content as one section
        if not sections:
            sections = [content]
        
        return sections
    
    def _chunk_section(self, section: str, chapter_id: str, section_name: str) -> List[ContentChunk]:
        """Chunk a section into smaller pieces"""
        # Determine section type based on header
        section_type = self._determine_section_type(section)
        
        # Split section into paragraphs
        paragraphs = self._split_into_paragraphs(section)
        
        chunks = []
        position = 0
        
        for para in paragraphs:
            if len(para.strip()) == 0:
                continue
                
            # If paragraph is too large, split it further
            if self._get_token_count(para) > self.max_chunk_size:
                sub_chunks = self._split_large_paragraph(para)
                for sub_chunk in sub_chunks:
                    chunk = ContentChunk(
                        id=f"{chapter_id}_{section_name}_{position}",
                        text=sub_chunk,
                        chunk_type=section_type,
                        chapter_id=chapter_id,
                        section=section_name,
                        position=position,
                        metadata={"source": "paragraph_split"}
                    )
                    chunks.append(chunk)
                    position += 1
            else:
                chunk = ContentChunk(
                    id=f"{chapter_id}_{section_name}_{position}",
                    text=para,
                    chunk_type=section_type,
                    chapter_id=chapter_id,
                    section=section_name,
                    position=position,
                    metadata={"source": "original_paragraph"}
                )
                chunks.append(chunk)
                position += 1
        
        # Try to combine smaller chunks if possible
        return self._combine_small_chunks(chunks)
    
    def _determine_section_type(self, section: str) -> str:
        """Determine the type of content in a section"""
        header = section.split('\n')[0].lower()
        
        if 'exercise' in header or 'exercises' in header:
            return 'exercise'
        elif 'code' in header or 'pseudocode' in header:
            return 'code'
        elif 'example' in header or 'examples' in header:
            return 'example'
        elif 'diagram' in header or 'figure' in header:
            return 'diagram'
        elif 'summary' in header:
            return 'summary'
        elif 'reference' in header or 'bibliography' in header:
            return 'reference'
        else:
            return 'text'
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs (separated by double newlines)"""
        # First, normalize the line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Split by double newlines to get paragraphs
        paragraphs = text.split('\n\n')
        
        # Clean up each paragraph
        cleaned_paragraphs = []
        for para in paragraphs:
            cleaned_para = para.strip()
            if cleaned_para:
                cleaned_paragraphs.append(cleaned_para)
        
        return cleaned_paragraphs
    
    def _get_token_count(self, text: str) -> int:
        """Estimate token count (simple word count for now, can be improved)"""
        # For now, using a simple word count
        # In practice, you might want to use tiktoken or similar for true tokenization
        return len(text.split())
    
    def _split_large_paragraph(self, paragraph: str) -> List[str]:
        """Split a large paragraph into smaller chunks"""
        sentences = re.split(r'(?<=[.!?]) +', paragraph)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding the sentence would exceed the max size
            if self._get_token_count(current_chunk + " " + sentence) <= self.max_chunk_size:
                if current_chunk:
                    current_chunk += " " + sentence
                else:
                    current_chunk = sentence
            else:
                # If the current chunk is substantial, save it
                if self._get_token_count(current_chunk) >= self.min_chunk_size:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    # If the current chunk is too small, try to add the sentence anyway
                    # to prevent very small chunks
                    current_chunk += " " + sentence
                    if self._get_token_count(current_chunk) >= self.max_chunk_size:
                        # If this makes it too large, split at the sentence level
                        # This is a fallback for very long sentences
                        chunks.append(current_chunk.strip())
                        current_chunk = ""
        
        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _combine_small_chunks(self, chunks: List[ContentChunk]) -> List[ContentChunk]:
        """Combine small chunks to improve efficiency while keeping them under max size"""
        if not chunks:
            return chunks
        
        combined_chunks = []
        current_text = chunks[0].text
        current_metadata = chunks[0].metadata
        current_position = chunks[0].position
        
        for i in range(1, len(chunks)):
            next_chunk = chunks[i]
            
            # Check if combining would exceed max size
            combined_text = current_text + " " + next_chunk.text
            if (self._get_token_count(combined_text) <= self.max_chunk_size and 
                next_chunk.section == chunks[0].section):  # Only combine within same section
                current_text = combined_text
            else:
                # Add the current combined chunk
                combined_chunk = ContentChunk(
                    id=f"{chunks[0].chapter_id}_{chunks[0].section}_{current_position}",
                    text=current_text,
                    chunk_type=chunks[0].chunk_type,
                    chapter_id=chunks[0].chapter_id,
                    section=chunks[0].section,
                    position=current_position,
                    metadata=current_metadata
                )
                combined_chunks.append(combined_chunk)
                
                # Reset for next combination
                current_text = next_chunk.text
                current_position = next_chunk.position
                current_metadata = next_chunk.metadata
        
        # Add the final combined chunk
        combined_chunk = ContentChunk(
            id=f"{chunks[0].chapter_id}_{chunks[0].section}_{current_position}",
            text=current_text,
            chunk_type=chunks[0].chunk_type,
            chapter_id=chunks[0].chapter_id,
            section=chunks[0].section,
            position=current_position,
            metadata=current_metadata
        )
        combined_chunks.append(combined_chunk)
        
        return combined_chunks

# Preprocessing functions
def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might interfere with processing
    # Keep essential markdown characters for formatting
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\#\*\`\[\]\(\)]', ' ', text)
    
    return text.strip()

def extract_exercises(content: str) -> List[Dict[str, str]]:
    """Extract exercises from content"""
    # Pattern for exercises (in details/summary format)
    exercise_pattern = r'<details>.*?<summary>Solution</summary>(.*?)</details>'
    solutions = re.findall(exercise_pattern, content, re.DOTALL)
    
    # Pattern for interactive exercises
    interactive_pattern = r'<ExerciseComponent[\s\S]*?exercise={[\s\S]*?id:\s*[\'"]([^\'"]+)[\'"][\s\S]*?question:\s*[\'"]([^\'"]+)[\'"][\s\S]*?solution:\s*[\'"]([^\'"]+)[\'"][\s\S]*?}[\s\S]*?/>'
    interactive_exercises = re.findall(interactive_pattern, content)
    
    exercises = []
    for sol in solutions:
        exercises.append({
            'type': 'regular',
            'content': sol.strip()
        })
    
    for ex_id, question, solution in interactive_exercises:
        exercises.append({
            'type': 'interactive',
            'id': ex_id,
            'question': question,
            'solution': solution
        })
    
    return exercises