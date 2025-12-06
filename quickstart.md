# Quickstart Guide: Humanoid Robotics AI-Driven Textbook

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager
- Git
- GitHub account
- Basic knowledge of Markdown and MDX

## Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd humanoid-robotics-book
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Start Local Development Server
```bash
npm run start
# or
yarn start
```

The site will be available at `http://localhost:3000`

## Creating a New Chapter

### 1. Use the Chapter Template
```bash
# Copy the MDX template to a new file in docs/chapters/
cp docs/templates/chapter-template.mdx docs/chapters/new-chapter.mdx
```

### 2. Update the Chapter Frontmatter
```md
---
id: chapter-[module]-[number]
title: [Your Chapter Title]
description: [Brief description of the chapter]
tags: [relevant, tags]
sidebar_position: [position-in-sidebar]
---

# [Your Chapter Title]

## Learning Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Concepts
[Explain the core concepts in this section]

## Examples
[Provide practical examples that illustrate the concepts]

## Code/Pseudocode
[Include code samples or pseudocode]

## Diagrams
[Embed SVG diagrams with proper alt-text and descriptions]

## Exercises
[Include at least 3 exercises with solutions]

## Summary
[Concise summary of key concepts]

## References
[Include citations to verifiable sources]
```

### 3. Add Chapter to Sidebar
Edit `sidebars.js` to include your new chapter in the navigation:

```js
module.exports = {
  docs: [
    {
      type: 'category',
      label: 'Foundations',
      items: [
        'chapters/foundations/introduction',
        'chapters/foundations/new-chapter', // Add this line
      ],
    },
  ],
};
```

## Content Guidelines

### Writing Style
- Write for engineering students with basic programming knowledge
- Use active voice and short sentences
- Follow consistent terminology across all chapters
- Include SI units for all measurements

### Code Samples
- Include runnable code or validated pseudocode
- Tag code blocks with appropriate language identifiers
- Provide explanations for complex code sections
- Include test cases where applicable

### Diagrams
- Use SVG format for all diagrams
- Include descriptive alt-text for accessibility
- Provide text descriptions that explain the diagram content
- Tag diagrams with relevant concepts they illustrate

### Exercises
- Create at least 3 exercises per chapter
- Include solutions or validation criteria
- Vary difficulty levels (beginner, intermediate, advanced)
- Align exercises with learning objectives

### Citations
- Cite all factual statements with verifiable sources
- Use academic papers, standards, textbooks, or official specifications
- Include URLs or DOIs when available
- Follow consistent citation format throughout the book

## Quality Checks

### Before Submitting
- Run the local development server to check formatting
- Verify all links and cross-references work correctly
- Check that all images and diagrams are properly displayed
- Ensure all exercises have solutions or validation criteria
- Confirm all citations have valid sources

### Linting
The project includes custom linting for MDX files:
```bash
npm run lint
# or
yarn lint
```

This checks for:
- Required section presence
- Citation presence
- Proper naming and folder structure
- MDX formatting

## Deployment

### Local Build
```bash
npm run build
# or
yarn build
```

### GitHub Pages Deployment
The site is automatically deployed to GitHub Pages when changes are merged to the `main` branch via GitHub Actions.

## Contributing

### Development Workflow
1. Create a new branch for your feature: `git checkout -b feature/new-chapter`
2. Make your changes
3. Run linting: `npm run lint`
4. Commit your changes with descriptive messages
5. Push to your branch: `git push origin feature/new-chapter`
6. Create a pull request to the `main` branch
7. Reference the relevant task ID in your pull request description

### Review Process
- All changes must pass linting checks
- Pull requests require at least one approval
- Reviewers will check for consistency with existing content
- All factual statements must be properly cited