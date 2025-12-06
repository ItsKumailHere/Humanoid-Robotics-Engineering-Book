import React from 'react';
import styles from './styles/ExerciseResults.module.css';

/**
 * Component to display results of completed exercises
 */
const ExerciseResults = ({ results, onRetry }) => {
  if (!results || results.length === 0) {
    return (
      <div className={styles.noResults}>
        No exercise results to display.
      </div>
    );
  }
 
  // Calculate summary statistics
  const totalExercises = results.length;
  const correctAnswers = results.filter(result => result.isCorrect).length;
  const accuracy = Math.round((correctAnswers / totalExercises) * 100);

  return (
    <div className={styles.resultsContainer}>
      <div className={styles.summary}>
        <h3>Exercise Results Summary</h3>
        <div className={styles.stats}>
          <div className={styles.statItem}>
            <span className={styles.statLabel}>Total Exercises:</span>
            <span className={styles.statValue}>{totalExercises}</span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statLabel}>Correct Answers:</span>
            <span className={styles.statValue}>{correctAnswers}</span>
          </div>
          <div className={styles.statItem}>
            <span className={styles.statLabel}>Accuracy:</span>
            <span className={styles.statValue}>{accuracy}%</span>
          </div>
        </div>
      </div>

      <div className={styles.detailedResults}>
        <h4>Detailed Results</h4>
        <ul className={styles.resultsList}>
          {results.map((result, index) => (
            <li key={index} className={`${styles.resultItem} ${result.isCorrect ? styles.correct : styles.incorrect}`}>
              <div className={styles.questionSummary}>
                <span className={styles.questionText}>{result.questionText || `Question ${index + 1}`}</span>
                <span className={styles.resultIndicator}>{result.isCorrect ? '✓' : '✗'}</span>
              </div>
              {!result.isCorrect && result.feedback && (
                <div className={styles.feedback}>{result.feedback}</div>
              )}
            </li>
          ))}
        </ul>
      </div>

      {onRetry && (
        <div className={styles.actions}>
          <button onClick={onRetry} className={styles.retryButton}>
            Retry Incorrect Exercises
          </button>
        </div>
      )}
    </div>
  );
};

export default ExerciseResults;