/**
 * API service for exercise submission and management
 * Provides methods to interact with the backend API for exercises
 */

// Base URL for API requests (would typically come from config)
const API_BASE_URL = '/api/v1';

/**
 * Submit an exercise answer for validation
 * @param {string} exerciseId - The ID of the exercise 
 * @param {object} answerData - The user's answer data
 * @param {string} userId - The ID of the user (optional for anonymous tracking)
 * @returns {Promise<object>} The validation result
 */
export const submitExercise = async (exerciseId, answerData, userId = null) => {
  try {
    const response = await fetch(`${API_BASE_URL}/exercises/${exerciseId}/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json', 
      },
      body: JSON.stringify({
        user_id: userId,
        answer: answerData,
        timestamp: new Date().toISOString(),
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error submitting exercise:', error);
    throw error;
  }
};

/**
 * Get an exercise by ID
 * @param {string} exerciseId - The ID of the exercise
 * @returns {Promise<object>} The exercise data
 */
export const getExercise = async (exerciseId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/exercises/${exerciseId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const exercise = await response.json();
    return exercise;
  } catch (error) {
    console.error('Error fetching exercise:', error);
    throw error;
  }
};

/**
 * Get exercises for a chapter
 * @param {string} chapterId - The ID of the chapter
 * @param {string} difficulty - Optional difficulty filter (beginner, intermediate, advanced)
 * @returns {Promise<array>} Array of exercises
 */
export const getExercisesByChapter = async (chapterId, difficulty = null) => {
  try {
    let url = `${API_BASE_URL}/exercises?chapter_id=${chapterId}`;
    if (difficulty) {
      url += `&difficulty=${difficulty}`;
    }
    
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const result = await response.json();
    return result.exercises;
  } catch (error) {
    console.error('Error fetching exercises by chapter:', error);
    throw error;
  }
};

/**
 * Get user's exercise history
 * @param {string} userId - The ID of the user
 * @returns {Promise<object>} User's exercise history
 */
export const getUserExerciseHistory = async (userId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/exercises`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    
    const history = await response.json();
    return history;
  } catch (error) {
    console.error('Error fetching user exercise history:', error);
    throw error;
  }
};

/**
 * Save user's exercise progress
 * @param {string} userId - The ID of the user
 * @param {object} progressData - The progress data to save
 * @returns {Promise<object>} The save result
 */
export const saveUserProgress = async (userId, progressData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/${userId}/progress`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(progressData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error saving user progress:', error);
    throw error;
  }
};