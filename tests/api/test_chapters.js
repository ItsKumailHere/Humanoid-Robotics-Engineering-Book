const axios = require('axios');

/**
 * API Contract Test for Chapter Retrieval
 * Verifies that the chapter endpoints match the contract defined in contracts/content-api.yaml
 */

describe('Chapter API Contract Tests', () => {
  const BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000/api/v1';
  
  describe('GET /chapters', () => {
    test('should return a list of all chapters with required fields', async () => {
      const response = await axios.get(`${BASE_URL}/chapters`);
      
      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('chapters');
      expect(Array.isArray(response.data.chapters)).toBe(true);
      
      if (response.data.chapters.length > 0) {
        const chapter = response.data.chapters[0];
        expect(chapter).toHaveProperty('id');
        expect(chapter).toHaveProperty('title');
        expect(chapter).toHaveProperty('summary');
        expect(chapter).toHaveProperty('learning_objectives');
        expect(Array.isArray(chapter.learning_objectives)).toBe(true);
        expect(chapter).toHaveProperty('sections');
        expect(Array.isArray(chapter.sections)).toBe(true);
        expect(chapter).toHaveProperty('exercises_count');
        expect(typeof chapter.exercises_count).toBe('number');
        expect(chapter).toHaveProperty('last_updated');
      }
    });
  });

  describe('GET /chapters/{id}', () => {
    test('should return a specific chapter by ID with required fields', async () => {
      // Assuming at least one chapter exists - using 'foundations' as example
      const response = await axios.get(`${BASE_URL}/chapters/foundations`);
      
      expect(response.status).toBe(200);
      
      const chapter = response.data;
      expect(chapter).toHaveProperty('id');
      expect(chapter).toHaveProperty('title');
      expect(chapter).toHaveProperty('learning_objectives');
      expect(Array.isArray(chapter.learning_objectives)).toBe(true);
      expect(chapter).toHaveProperty('concepts');
      expect(chapter).toHaveProperty('examples');
      expect(Array.isArray(chapter.examples)).toBe(true);
      expect(chapter).toHaveProperty('code');
      expect(Array.isArray(chapter.code)).toBe(true);
      expect(chapter).toHaveProperty('diagrams');
      expect(Array.isArray(chapter.diagrams)).toBe(true);
      expect(chapter).toHaveProperty('exercises');
      expect(Array.isArray(chapter.exercises)).toBe(true);
      expect(chapter).toHaveProperty('summary');
      expect(chapter).toHaveProperty('references');
      expect(Array.isArray(chapter.references)).toBe(true);
      expect(chapter).toHaveProperty('metadata');
    });

    test('should return 404 for non-existent chapter', async () => {
      try {
        await axios.get(`${BASE_URL}/chapters/non-existent-chapter`);
      } catch (error) {
        expect(error.response.status).toBe(404);
      }
    });
  });
});

module.exports = { testSuite: 'Chapter API Contract Tests' };