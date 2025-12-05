# Data Model: Humanoid Robotics AI-Driven Textbook

## Textbook Chapter Entity

**ID**: Unique identifier for the chapter
- Type: String
- Constraints: Required, Unique, Follows format: "chapter-[module]-[number]" (e.g., "chapter-foundations-01")

**Title**: Chapter title following consistent naming convention
- Type: String
- Constraints: Required, Max 200 characters

**Learning Objectives**: List of specific learning objectives
- Type: Array of Strings
- Constraints: Required, Each objective max 200 characters

**Concepts**: Main content sections explaining concepts
- Type: String (Markdown/MDX content)
- Constraints: Required, Use proper semantic headings

**Examples**: Practical examples supporting concepts
- Type: Array of Example objects
- Constraints: At least one example required

**Code/Pseudocode**: Code samples or validated pseudocode
- Type: Array of CodeBlock objects
- Constraints: Each block must be tagged as "code" or "pseudocode"

**Diagrams**: SVG images with alt-text and descriptions
- Type: Array of Diagram objects
- Constraints: Each diagram must have alt text and description

**Exercises**: Practice problems with automated validation
- Type: Array of Exercise objects
- Constraints: At least 3 exercises required per chapter

**Summary**: Chapter summary
- Type: String (Markdown content)
- Constraints: Required, Concise summary of key concepts

**References/Citations**: Bibliography with verifiable sources
- Type: Array of Reference objects
- Constraints: Each citation must reference verifiable source

**Metadata**: Creation date, author, last updated, version
- Type: Metadata object
- Properties:
  - created: Date
  - last_updated: Date
  - author: String
  - version: String
  - tags: Array of Strings

## Example Entity

**ID**: Unique identifier
- Type: String
- Constraints: Required, Unique within chapter

**Title**: Example title
- Type: String
- Constraints: Required

**Description**: Description of the example
- Type: String (Markdown content)
- Constraints: Required 

**Content**: The actual example content
- Type: String (Markdown/MDX content)
- Constraints: Required

**Related Concepts**: Links to relevant concepts in the textbook
- Type: Array of concept identifiers
- Constraints: Required

## CodeBlock Entity

**ID**: Unique identifier
- Type: String
- Constraints: Required, Unique within chapter

**Language**: Programming language or 'pseudocode'
- Type: String
- Constraints: Required, Valid language identifier

**Content**: The actual code content
- Type: String
- Constraints: Required

**Caption**: Optional caption explaining the code
- Type: String
- Constraints: Optional, Max 500 characters

**Validation**: For exercises, how to validate the code
- Type: Validation object
- Properties:
  - expected_output: String
  - test_cases: Array of Test objects

## Diagram Entity

**ID**: Unique identifier
- Type: String
- Constraints: Required, Unique within chapter

**Title**: Diagram title
- Type: String
- Constraints: Required

**Description**: Text description for accessibility
- Type: String (Markdown content)
- Constraints: Required, Detailed enough for screen readers

**Alt Text**: Alt text for image
- Type: String
- Constraints: Required, Concise description

**SVG Content**: SVG code or reference
- Type: String
- Constraints: Required, Valid SVG

**Related Concepts**: Links to relevant concepts in the textbook
- Type: Array of concept identifiers
- Constraints: Required

## Exercise Entity

**ID**: Unique identifier
- Type: String
- Constraints: Required, Unique within chapter

**Content**: Exercise description and requirements
- Type: String (Markdown content)
- Constraints: Required

**Solution**: Solution or validation criteria
- Type: String (Markdown content) or Validation object
- Constraints: Required

**Difficulty**: Beginner, Intermediate, Advanced
- Type: String
- Constraints: Required, One of ["beginner", "intermediate", "advanced"]

**Related Concepts**: Links to relevant concepts in the textbook
- Type: Array of concept identifiers
- Constraints: Required

**Type**: Exercise type (e.g., "multiple-choice", "coding", "theory")
- Type: String
- Constraints: Required

## Reference Entity

**ID**: Unique identifier
- Type: String
- Constraints: Required, Unique within chapter

**Title**: Title of the referenced work
- Type: String
- Constraints: Required

**Authors**: Authors of the referenced work
- Type: Array of Strings
- Constraints: Required

**Publication**: Where the work was published
- Type: String
- Constraints: Required for academic papers

**URL**: Link to the reference (if available)
- Type: String (URL)
- Constraints: Optional but preferred

**Citation Type**: Type of reference (e.g., "academic-paper", "book", "website")
- Type: String
- Constraints: Required

**Access Date**: When the reference was accessed (for web resources)
- Type: Date
- Constraints: Required for web resources

## User Entity (for personalization)

**ID**: Unique identifier
- Type: String
- Constraints: Required, Unique

**Experience Level**: User's programming and robotics experience
- Type: String
- Constraints: Required, One of ["beginner", "intermediate", "advanced"]

**Preferences**: User's content preferences
- Type: Object
- Properties:
  - language: String (default: "en")
  - content_type: Array of Strings (e.g., ["text-heavy", "diagram-heavy", "code-heavy"])
  - difficulty_override: Boolean (whether to show content beyond user's level)

**Progress**: User's progress through the textbook
- Type: Object
- Properties:
  - completed_chapters: Array of chapter IDs
  - completed_exercises: Array of exercise IDs
  - last_accessed: Date

## Personalization Mapping

**Chapter ID**: The chapter to customize
- Type: String
- Constraints: Required, References a valid chapter

**User Level**: For which user level this customization applies
- Type: String
- Constraints: Required, One of ["beginner", "intermediate", "advanced"]

**Custom Content**: Alternative content for this user level
- Type: Object
- Properties:
  - simplified_concepts: String (optional simplified explanations)
  - additional_examples: Array of Example objects (optional extra examples)
  - adjusted_exercises: Array of Exercise objects (optional adjusted difficulty)

## Validation Rules

### Chapter Validation
- Must have all required fields
- Learning objectives must be between 1 and 5 items
- Concepts section must contain at least 500 words of content
- Must include at least 3 examples
- Must include at least 3 diagrams
- Must include at least 3 exercises
- Must include at least 3 citations/references
- All citations must have valid URLs or DOI

### Content Validation
- All text content must pass readability checks (appropriate for target audience)
- All code samples must be validated as syntactically correct
- All diagrams must have alt-text and descriptions
- All exercises must have solutions or validation criteria
- Content must not contain ambiguous pronouns or references without proper antecedents

### Accessibility Validation
- All images must have alt text
- All diagrams must have text descriptions
- Color contrast ratios must meet WCAG 2.1 AA standards
- All content must be navigable via keyboard
- All content must be compatible with screen readers