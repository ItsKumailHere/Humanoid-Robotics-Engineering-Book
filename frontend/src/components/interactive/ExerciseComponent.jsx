import React from 'react';
import MCQComponent from './MCQComponent';
import styles from './styles/ExerciseComponent.module.css';

/**
 * Exercise Component that wraps different types of exercises
 * Currently supports MCQs, extensible for other types
 */
const ExerciseComponent = ({ exercise }) => {
  const { id, type, question, options, description, solution, correctAnswers } = exercise;

  // Handler for when an answer is submitted
  const handleAnswerSubmit = (answerData) => {
    console.log('Answer submitted:', answerData);
    // In a real implementation, this would send the data to a backend
    // and potentially update user progress
  }; 

  // Render different exercise types based on the type property
  const renderExerciseContent = () => {
    switch (type) {
      case 'multiple-choice':
        return (
          <MCQComponent
            question={question}
            options={options}
            questionId={id}
            correctAnswers={correctAnswers}
            onSubmit={handleAnswerSubmit}
          />
        );

      case 'multiple-select':
        return (
          <MCQComponent
            question={question}
            options={options}
            multipleAnswers={true}
            questionId={id}
            correctAnswers={correctAnswers}
            onSubmit={handleAnswerSubmit}
          />
        );

      default:
        return (
          <div className={styles.unsupported}>
            Exercise type '{type}' is not supported yet.
          </div>
        );
    }
  };

  return (
    <div className={styles.exerciseContainer}>
      <div className={styles.exerciseHeader}>
        <h3 className={styles.exerciseTitle}>Exercise</h3>
        {description && <p className={styles.exerciseDescription}>{description}</p>}
      </div>

      <div className={styles.exerciseBody}>
        {renderExerciseContent()}
      </div>

      {solution && (
        <details className={styles.solution}>
          <summary>Solution</summary>
          <div className={styles.solutionContent}>{solution}</div>
        </details>
      )}
    </div>
  );
};

export default ExerciseComponent;