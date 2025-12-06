import React, { useState, useEffect } from 'react';
import { validateAnswer } from '@site/src/utils/validation';
import { submitExercise } from '@site/src/services/exerciseService';
import styles from './styles/MCQComponent.module.css';

/**
 * MCQ Component for interactive exercises in the textbook
 * Supports single and multiple answer options
 */
const MCQComponent = ({
  question,
  options,
  multipleAnswers = false, 
  questionId, 
  correctAnswers,
  onSubmit,
  userId = null
}) => {
  const [selectedAnswers, setSelectedAnswers] = useState(multipleAnswers ? [] : '');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [isFocused, setIsFocused] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Initialize with a random ID for accessibility
  const componentId = `mcq-${questionId}-${Math.random().toString(36).substr(2, 9)}`;

  const handleOptionChange = (optionValue) => {
    if (multipleAnswers) {
      // For multiple answers, toggle the selection
      setSelectedAnswers(prev =>
        prev.includes(optionValue)
          ? prev.filter(item => item !== optionValue)
          : [...prev, optionValue]
      );
    } else {
      // For single answer, just set the value
      setSelectedAnswers(optionValue);
    }
  };

  const handleKeyDown = (e, optionValue) => {
    // Allow spacebar to select options for accessibility
    if (e.key === ' ' || e.key === 'Spacebar') {
      e.preventDefault();
      handleOptionChange(optionValue);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);

    try {
      // Submit the answer to the backend for validation
      const result = await submitExercise(
        questionId,
        { answer: selectedAnswers },
        userId
      );

      // Determine if the answer is correct based on the backend response
      // For now, we'll use local validation if backend doesn't provide correctness
      const answerCorrect = result.is_correct !== undefined
        ? result.is_correct
        : validateAnswer(selectedAnswers, correctAnswers,
            multipleAnswers ? 'multiple-select' : 'single-choice');

      setIsSubmitted(true);
      setIsCorrect(answerCorrect);
      setFeedback(result.feedback ||
        (answerCorrect
          ? 'Correct! Well done.'
          : 'Not quite right. Review the material and try again.'));

      // Call the onSubmit callback with the results
      if (onSubmit) {
        onSubmit({
          questionId,
          selectedAnswers,
          isCorrect: answerCorrect,
          feedback: result.feedback
        });
      }
    } catch (err) {
      setError('Failed to submit answer. Please try again.');
      console.error('Error submitting exercise:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedAnswers(multipleAnswers ? [] : '');
    setIsSubmitted(false);
    setIsCorrect(null);
    setFeedback('');
    setError(null);
  };

  const allSelected = multipleAnswers ?
    selectedAnswers.length === options.length :
    !!selectedAnswers;

  return (
    <div
      className={styles.mcqContainer}
      role="radiogroup"
      aria-labelledby={`${componentId}-question`}
      aria-disabled={isSubmitted || loading}
    >
      <div
        id={`${componentId}-question`}
        className={styles.question}
        tabIndex={isFocused ? -1 : 0}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
      >
        {question}
      </div>

      <ul className={styles.optionsList}>
        {options.map((option, index) => {
          const optionId = `${componentId}-option-${index}`;
          return (
            <li key={index} className={styles.optionItem}>
              <label
                htmlFor={optionId}
                className={styles.optionLabel}
                onKeyDown={(e) => handleKeyDown(e, option.value)}
                tabIndex={0}
              >
                <input
                  id={optionId}
                  type={multipleAnswers ? 'checkbox' : 'radio'}
                  name={multipleAnswers ? `${componentId}-options` : `${componentId}-option`}
                  value={option.value}
                  checked={
                    multipleAnswers
                      ? selectedAnswers.includes(option.value)
                      : selectedAnswers === option.value
                  }
                  onChange={() => handleOptionChange(option.value)}
                  disabled={isSubmitted || loading}
                  className={styles.optionInput}
                  aria-describedby={`${optionId}-description`}
                />
                <span
                  id={`${optionId}-description`}
                  className={styles.optionText}
                >
                  {option.text}
                </span>
              </label>
            </li>
          );
        })}
      </ul>

      {error && (
        <div className={styles.error}>
          {error}
        </div>
      )}

      {!isSubmitted ? (
        <button
          onClick={handleSubmit}
          disabled={
            loading ||
            (multipleAnswers && selectedAnswers.length === 0) ||
            (!multipleAnswers && !selectedAnswers)
          }
          className={styles.submitButton}
          aria-describedby={`${componentId}-status`}
        >
          {loading ? 'Submitting...' : 'Submit Answer'}
        </button>
      ) : (
        <div className={styles.result}>
          <div
            id={`${componentId}-status`}
            className={styles.feedback}
            role="status"
            aria-live="polite"
          >
            {feedback && (
              <p className={isCorrect ? styles.correct : styles.incorrect}>
                {feedback}
              </p>
            )}
          </div>
          <button
            onClick={handleReset}
            className={styles.resetButton}
            aria-label="Try this question again"
          >
            Try Again
          </button>
        </div>
      )}

      {/* Hidden element for screen reader announcements */}
      <div
        className={styles.visuallyHidden}
        aria-live="polite"
        aria-atomic="true"
      >
        {isSubmitted && feedback}
      </div>
    </div>
  );
};

export default MCQComponent;