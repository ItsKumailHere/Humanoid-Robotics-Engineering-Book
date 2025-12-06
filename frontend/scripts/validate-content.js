#!/usr/bin/env node

/**
 * Content Validation Script for Humanoid Robotics Textbook
 * Validates all chapters against the defined rules
 */

const fs = require('fs');
const path = require('path');
const validationConfig = require('./content-validation.config.js');

const CHAPTERS_DIR = path.join(__dirname, 'docs', 'Chapters');

function parseFrontmatter(content) {
  // Extract frontmatter between --- delimiters
  const frontmatterRegex = /^---\n([\s\S]*?)\n---/;
  const match = content.match(frontmatterRegex);
  if (!match) return {};

  const frontmatterText = match[1];
  const lines = frontmatterText.split('\n');
  const frontmatter = {};
  
  for (const line of lines) {
    const colonIndex = line.indexOf(':');
    if (colonIndex > 0) {
      const key = line.substring(0, colonIndex).trim();
      let value = line.substring(colonIndex + 1).trim();
      
      // Handle different value types
      if (value.startsWith('"') && value.endsWith('"')) {
        value = value.substring(1, value.length - 1); // Remove quotes
      } else if (value === 'true') {
        value = true;
      } else if (value === 'false') {
        value = false;
      } else if (!isNaN(value)) {
        value = Number(value);
      }
      
      frontmatter[key] = value;
    }
  }
  
  return frontmatter;
}

function validateChapter(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const errors = [];

  // Validate frontmatter
  const frontmatter = parseFrontmatter(content);
  const frontmatterErrors = validationConfig.validators.validateFrontmatter(frontmatter);
  errors.push(...frontmatterErrors);

  // Validate required sections
  const sectionErrors = validationConfig.validators.validateSections(content);
  errors.push(...sectionErrors);

  // Validate learning objectives
  const objectiveErrors = validationConfig.validators.validateLearningObjectives(content);
  errors.push(...objectiveErrors);

  // Validate exercises
  const exerciseErrors = validationConfig.validators.validateExercises(content);
  errors.push(...exerciseErrors);

  return errors;
}

function validateAllChapters() {
  const allFiles = fs.readdirSync(CHAPTERS_DIR);
  const mdxFiles = allFiles.filter(file => path.extname(file) === '.mdx');
  
  console.log(`Validating ${mdxFiles.length} chapters...\n`);
  
  let totalErrors = 0;
  let validChapters = 0;
  
  for (const file of mdxFiles) {
    console.log(`Validating ${file}...`);
    const filePath = path.join(CHAPTERS_DIR, file);
    const errors = validateChapter(filePath);
    
    if (errors.length === 0) {
      console.log(`✓ ${file} is valid\n`);
      validChapters++;
    } else {
      console.log(`✗ ${file} has ${errors.length} error(s):`);
      for (const error of errors) {
        console.log(`  - ${error}`);
      }
      console.log('');
      totalErrors += errors.length;
    }
  }
  
  console.log(`\nValidation Summary:`);
  console.log(`- Valid chapters: ${validChapters}/${mdxFiles.length}`);
  console.log(`- Total errors: ${totalErrors}`);
  
  if (totalErrors === 0) {
    console.log('\n✓ All chapters passed validation!');
    return 0;
  } else {
    console.log('\n✗ Some chapters failed validation.');
    return 1;
  }
}

// Run validation if this script is executed directly
if (require.main === module) {
  const exitCode = validateAllChapters();
  process.exit(exitCode);
}

module.exports = { validateChapter, validateAllChapters, parseFrontmatter };