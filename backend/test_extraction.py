# Direct debug script to test the content extraction path issue
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

# Change to the backend directory to ensure relative paths work correctly
os.chdir(backend_path)

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {[p for p in sys.path if 'backend' in p or 'utils' in p]}")

# Now try to import and test the content extractor
try:
    print("\nTrying to import ContentExtractor...")
    from utils.content_extraction import ContentExtractor
    
    print("\nCreating ContentExtractor instance...")
    extractor = ContentExtractor()
    
    print(f"\nDocs path set to: {extractor.docs_path}")
    print(f"Docs path exists: {extractor.docs_path.exists()}")
    print(f"Docs path is directory: {extractor.docs_path.is_dir()}")
    
    if extractor.docs_path.exists() and extractor.docs_path.is_dir():
        print(f"\nContents of the directory:")
        for item in extractor.docs_path.iterdir():
            print(f"  - {item.name} ({'dir' if item.is_dir() else 'file'})")
        
        print(f"\nMDX files in the directory:")
        mdx_files = list(extractor.docs_path.glob("*.mdx"))
        print(f"Found {len(mdx_files)} .mdx files")
        for i, file in enumerate(mdx_files):
            print(f"  {i+1}. {file.name}")
        
        print(f"\nAttempting to extract chapters...")
        chapters = extractor.extract_all_chapters()
        print(f"Successfully extracted {len(chapters)} chapters")
        
        for i, chapter in enumerate(chapters):
            print(f"  Chapter {i+1}: {chapter.id} - {chapter.title}")
    else:
        print(f"\nERROR: The path '{extractor.docs_path}' does not exist!")
        print("Make sure you're running this from the correct directory and that the frontend/docs/Chapters directory exists.")
        
except Exception as e:
    print(f"Error during import or execution: {e}")
    import traceback
    traceback.print_exc()