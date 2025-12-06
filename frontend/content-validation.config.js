/**
 * Content Validation Rules for Humanoid Robotics Textbook
 * Ensures all chapters follow the required structure and quality standards
 */

module.exports = {
  /**
   * Required frontmatter fields for all chapters
   */
  requiredFrontmatter: [
    'id',
    'title',
    'description',
    'sidebar_position'
  ],

  /**
   * Required sections in each chapter
   */
  requiredSections: [
    'Learning Objectives',
    'Concepts',
    'Examples',
    'Exercises',
    'Summary',
    'References'
  ],

  /**
   * Content rules for each required section
   */
  sectionRules: {
    'Learning Objectives': {
      required: true,
      minItems: 3,  // At least 3 learning objectives
      format: 'list',  // Must be in list format with hyphens
      expectsContent: true
    },
    'Concepts': {
      required: true,
      minLength: 200,  // At least 200 characters
      expectsContent: true
    },
    'Examples': {
      required: true,
      minItems: 1,  // At least 1 example
      expectsContent: true
    },
    'Exercises': {
      required: true,
      minItems: 3,  // At least 3 exercises
      hasSolutions: true,  // All exercises must have solutions
      hasInteractive: true // At least 1 interactive exercise required
    },
    'Summary': {
      required: true,
      minLength: 50,  // At least 50 characters
      expectsContent: true
    },
    'References': {
      required: true,
      minItems: 2,  // At least 2 references
      expectsContent: true
    }
  },

  /**
   * Content quality rules
   */
  qualityRules: {
    // Minimum word count for concepts section
    minConceptsWords: 300,
    
    // Maximum consecutive sentences starting with the same word
    maxConsecutiveSentences: 3,
    
    // Must include at least one code/pseudocode block
    hasCodeBlock: true,

    // Exercises must have unique IDs
    uniqueExerciseIds: true,

    // All interactive exercises must be properly formatted
    validInteractiveExercises: true
  },

  /**
   * Formatting rules
   */
  formattingRules: {
    // Use of H2 headers only for required sections
    h2Headers: ['Learning Objectives', 'Concepts', 'Examples', 'Code/Pseudocode', 'Exercises', 'Summary', 'References'],
    
    // Use of H3 headers for exercises
    h3HeadersForExercises: true,
    
    // Proper use of details/summary for solutions
    solutionFormat: 'details-summary'
  },

  /**
   * Validation functions
   */
  validators: {
    validateFrontmatter: (frontmatter) => {
      const errors = [];
      for (const field of module.exports.requiredFrontmatter) {
        if (!frontmatter[field]) {
          errors.push(`Missing required frontmatter field: ${field}`);
        }
      }
      return errors;
    },
    
    validateSections: (content) => {
      const errors = [];
      for (const section of module.exports.requiredSections) {
        const hasSection = new RegExp(`## ${section}`, 'i').test(content);
        if (!hasSection) {
          errors.push(`Missing required section: ${section}`);
        }
      }
      return errors;
    },
    
    validateLearningObjectives: (content) => {
      const errors = [];
      const objectivesSection = content.match(/## Learning Objectives[\s\S]*?(?=##\s|$)/i);
      if (objectivesSection) {
        // Count list items (lines starting with - or *)
        const objectives = objectivesSection[0].match(/^\s*[-*]\s.*$/gm) || [];
        if (objectives.length < 3) {
          errors.push(`Learning Objectives section must have at least 3 objectives, found ${objectives.length}`);
        }
      }
      return errors;
    },
    
    validateExercises: (content) => {
      const errors = [];
      
      // Check for regular exercises
      const exerciseMatches = content.match(/### Exercise \d+/g) || [];
      if (exerciseMatches.length < 3) {
        errors.push(`Chapter must have at least 3 exercises, found ${exerciseMatches.length}`);
      }
      
      // Check for solutions
      const solutionMatches = content.match(/<details>[\s\S]*?<summary>Solution<\/summary>/g) || [];
      if (solutionMatches.length < 3) {
        errors.push(`Chapter must have at least 3 solutions, found ${solutionMatches.length}`);
      }
      
      // Check for interactive exercises
      const interactiveMatches = content.match(/<ExerciseComponent/g) || [];
      if (interactiveMatches.length < 1) {
        errors.push(`Chapter must have at least 1 interactive exercise, found ${interactiveMatches.length}`);
      }
      
      return errors;
    }
  }
};