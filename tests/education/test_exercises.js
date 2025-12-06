/**
 * Exercise Validation Test
 * Verifies that exercises in chapters follow the required structure and have valid solutions
 */

describe('Exercise Validation Tests', () => {
  const fs = require('fs');
  const path = require('path');

  const CHAPTERS_DIR = path.join(__dirname, '..', '..', 'frontend', 'docs', 'Chapters');
  
  // Read all chapter files
  const chapterFiles = fs.readdirSync(CHAPTERS_DIR).filter(file => path.extname(file) === '.mdx');
  
  chapterFiles.forEach(file => {
    const filePath = path.join(CHAPTERS_DIR, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    describe(`Exercise validation for ${file}`, () => {
      test(`Chapter ${file} should have properly formatted exercises`, () => {
        // Check if exercises section exists
        expect(content).toContain('## Exercises');
        
        // Check for at least one exercise
        expect(content).toMatch(/### Exercise \d+/);
        
        // Check for solutions in details/summary format
        expect(content).toMatch(/<details>[\s\S]*?<summary>Solution<\/summary>[\s\S]*?<\/details>/);
        
        // Check for interactive exercises
        expect(content).toMatch(/<ExerciseComponent[\s\S]*?\/>/);
      });
      
      test(`Interactive exercises in ${file} should have valid structure`, () => {
        // Check that interactive exercises have proper structure
        const interactiveExerciseRegex = /<ExerciseComponent[\s\S]*?exercise={[\s\S]*?}[\s\S]*?\/>/g;
        const interactiveExercises = content.match(interactiveExerciseRegex) || [];
        
        interactiveExercises.forEach(exercise => {
          expect(exercise).toContain('id:');
          expect(exercise).toContain('type:');
          expect(exercise).toContain('question:');
          expect(exercise).toContain('options:');
          expect(exercise).toContain('correctAnswers:');
          expect(exercise).toContain('description:');
          expect(exercise).toContain('solution:');
          expect(exercise).toContain('explanation:');
        });
      });
    });
  });

  test('All chapters should have consistent exercise format', () => {
    const inconsistentChapters = [];
    
    chapterFiles.forEach(file => {
      const filePath = path.join(CHAPTERS_DIR, file);
      const content = fs.readFileSync(filePath, 'utf8');
      
      if (!content.includes('## Exercises')) {
        inconsistentChapters.push(file);
      }
    });
    
    if (inconsistentChapters.length > 0) {
      console.warn(`Chapters without exercises section: ${inconsistentChapters.join(', ')}`);
    }
    
    expect(inconsistentChapters).toHaveLength(0);
  });
});

module.exports = { testSuite: 'Exercise Validation Tests' };