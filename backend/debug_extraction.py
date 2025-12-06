# Debug script to check why index-content returns 0 chapters
import os
from pathlib import Path

# Add the utils directory to the path so we can import
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.content_extraction import ContentExtractor

def debug_content_extraction():
    print("Debugging Content Extraction...")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Test different possible paths
    possible_paths = [
        "../frontend/docs/Chapters",
        "../../frontend/docs/Chapters",
        "frontend/docs/Chapters",
        "./frontend/docs/Chapters",
        "../../../frontend/docs/Chapters"
    ]
    
    print("\nChecking possible paths:")
    for path_str in possible_paths:
        path_obj = Path(path_str)
        print(f"  Path: {path_obj.absolute()}")
        print(f"    Exists: {path_obj.exists()}")
        if path_obj.exists():
            files = list(path_obj.glob("*.mdx"))
            print(f"    .mdx files: {len(files)}")
            if files:
                print(f"    Sample files: {[f.name for f in files[:3]]}")  # Show first 3
        print()
    
    print("Creating extractor with default path...")
    extractor = ContentExtractor()
    print(f"Extractor docs_path: {extractor.docs_path}")
    
    print("Attempting to extract chapters...")
    try:
        chapters = extractor.extract_all_chapters()
        print(f"Successfully extracted {len(chapters)} chapters")
        
        for i, ch in enumerate(chapters[:3]):  # Show first 3
            print(f"  Chapter {i+1}: {ch.title} (ID: {ch.id})")
    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_content_extraction()