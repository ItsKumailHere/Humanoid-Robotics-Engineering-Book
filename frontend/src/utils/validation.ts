/**
 * Validation utilities for MCQ answers
 * Provides functions to validate user answers against correct answers
 */

/**
 * Validates a single answer against a correct answer
 * @param {any} userAnswer - The answer provided by the user
 * @param {any} correctAnswer - The correct answer
 * @returns {boolean} Whether the answer is correct
 */
export const validateSingleAnswer = (userAnswer:any, correctAnswer:any) => {
  // Handle string/number comparison with type coercion
  if (typeof correctAnswer === 'string' || typeof correctAnswer === 'number') {
    return userAnswer.toString().toLowerCase().trim() === 
           correctAnswer.toString().toLowerCase().trim();
  }
  
  // Handle boolean comparison
  if (typeof correctAnswer === 'boolean') {
    if (typeof userAnswer === 'boolean') {
      return userAnswer === correctAnswer;
    }
    // If userAnswer is string like 'true'/'false', convert appropriately
    if (typeof userAnswer === 'string') {
      return userAnswer.toLowerCase() === correctAnswer.toString();
    }
  }
  
  // Handle object comparison (for complex answers)
  if (typeof correctAnswer === 'object' && correctAnswer !== null) {
    return JSON.stringify(userAnswer) === JSON.stringify(correctAnswer);
  }
  
  // Default comparison
  return userAnswer === correctAnswer;
};

/**
 * Validates multiple answers against correct answers
 * @param {array} userAnswers - The answers provided by the user
 * @param {array} correctAnswers - The correct answers
 * @returns {boolean} Whether all answers are correct (and only correct answers are provided)
 */
export const validateMultipleAnswers = (userAnswers:any, correctAnswers:any) => {
  if (userAnswers.length !== correctAnswers.length) {
    return false;
  }
  
  // Check that every user answer is in the correct answers 
  for (const userAnswer of userAnswers) {
    if (!correctAnswers.some((correctAnswer:any) => 
      validateSingleAnswer(userAnswer, correctAnswer)
    )) {
      return false;
    }
  }
  
  // Check that every correct answer is in the user answers
  for (const correctAnswer of correctAnswers) {
    if (!userAnswers.some((userAnswer:any) => 
      validateSingleAnswer(userAnswer, correctAnswer)
    )) {
      return false;
    }
  }
  
  return true;
};

/**
 * Validates an answer based on exercise type
 * @param {any} userAnswer - The answer provided by the user
 * @param {any} correctAnswer - The correct answer (or array of correct answers for multiple)
 * @param {string} exerciseType - The type of exercise ('single-choice', 'multiple-choice', etc.)
 * @returns {boolean} Whether the answer is correct
 */
export const validateAnswer = (userAnswer:any, correctAnswer:any, exerciseType = 'single-choice') => {
  switch (exerciseType) {
    case 'multiple-choice':
    case 'single-choice':
      return validateSingleAnswer(userAnswer, correctAnswer);
    
    case 'multiple-select':
      // For multiple-select, correctAnswer should be an array
      return Array.isArray(correctAnswer) && 
             Array.isArray(userAnswer) && 
             validateMultipleAnswers(userAnswer, correctAnswer);
    
    default:
      console.warn(`Unknown exercise type: ${exerciseType}, defaulting to single answer validation`);
      return validateSingleAnswer(userAnswer, correctAnswer);
  }
};

/**
 * Sanitizes user input to prevent XSS and other security issues
 * @param {any} userInput - The input to sanitize
 * @returns {any} The sanitized input
 */
export const sanitizeUserInput = (userInput: any): any => {
  if (typeof userInput === 'string') {
    // Remove potentially dangerous characters
    return userInput
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#x27;')
      .replace(/\//g, '&#x2F;');
  }
  
  if (Array.isArray(userInput)) {
    return userInput.map((item: any) => sanitizeUserInput(item));
  }
  
  if (typeof userInput === 'object' && userInput !== null) {
    const sanitized: any = {};
    for (const key in userInput) {
      sanitized[key] = sanitizeUserInput(userInput[key]);
    }
    return sanitized;
  }
  
  return userInput;
};

/**
 * Validates an exercise object to ensure it has the required properties
 * @param {object} exercise - The exercise object to validate
 * @returns {object} Object with isValid boolean and errors array
 */
export const validateExercise = (exercise:any) => {
  const errors = [];
  
  if (!exercise) {
    errors.push('Exercise is required');
    return { isValid: false, errors };
  }
  
  // Validate required properties
  if (!exercise.id) {
    errors.push('Exercise ID is required');
  }
  
  if (!exercise.question) {
    errors.push('Exercise question is required');
  }
  
  if (!exercise.type) {
    errors.push('Exercise type is required');
  }
  
  // Validate options for MCQ-type exercises
  if (exercise.type === 'multiple-choice' || exercise.type === 'multiple-select') {
    if (!Array.isArray(exercise.options) || exercise.options.length === 0) {
      errors.push('Options are required for MCQ exercises');
    } else {
      for (let i = 0; i < exercise.options.length; i++) {
        const option = exercise.options[i];
        if (!option.value && option.value !== 0) {
          errors.push(`Option ${i + 1} must have a value`);
        }
        if (!option.text) {
          errors.push(`Option ${i + 1} must have text`);
        }
      }
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  };
};