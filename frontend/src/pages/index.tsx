import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import styles from './index.module.css';

export default function Home() {
  return (
    <Layout
      title="Humanoid Robotics: AI-Driven Textbook"
      description="Comprehensive guide to humanoid robotics concepts, applications, and implementation"
    >
      <main>
        <section className={styles.hero}>
          <div className={styles.container}>
            <h1 className={styles.title}>Humanoid Robotics</h1>
            <p className={styles.tagline}>
              AI-Driven Textbook: A Comprehensive Guide to Concepts, Applications, and Implementation
            </p>
            <div className={styles.buttons}>
              <Link className={styles.button} to="/docs/intro">
                Start Reading
              </Link>
              <Link className={styles.button + ' ' + styles.secondary} to="/docs/Chapters/foundations">
                View Chapters
              </Link>
            </div>
          </div>
        </section>

        <section className={styles.features}>
          <div className={styles.container}>
            <h2>What You'll Learn</h2>
            <div className={styles.featureGrid}>
              <div className={styles.featureCard}>
                <h3>Foundations</h3>
                <p>
                  Understand the fundamental principles of robotics, physics, and AI that power humanoid systems.
                </p>
              </div>
              <div className={styles.featureCard}>
                <h3>Perception & Sensing</h3>
                <p>
                  Learn how robots perceive and interact with their environment through sensors and perception systems.
                </p>
              </div>
              <div className={styles.featureCard}>
                <h3>Control & Motion</h3>
                <p>
                  Master control theory, kinematics, dynamics, and motion planning for humanoid robots.
                </p>
              </div>
              <div className={styles.featureCard}>
                <h3>Manipulation & Interaction</h3>
                <p>
                  Explore how humanoid robots interact with objects and environments through manipulation and control.
                </p>
              </div>
              <div className={styles.featureCard}>
                <h3>AI Integration</h3>
                <p>
                  Discover how artificial intelligence enhances robotics capabilities and enables autonomous behavior.
                </p>
              </div>
              <div className={styles.featureCard}>
                <h3>Safety & Simulation</h3>
                <p>
                  Understand safety considerations and simulation tools for developing and testing robotic systems.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.chapters}>
          <div className={styles.container}>
            <h2>Chapters</h2>
            <div className={styles.chapterList}>
              <Link to="/docs/Chapters/foundations" className={styles.chapterLink}>→ Foundations of Robotics</Link>
              <Link to="/docs/Chapters/kinematics" className={styles.chapterLink}>→ Kinematics</Link>
              <Link to="/docs/Chapters/dynamics" className={styles.chapterLink}>→ Dynamics</Link>
              <Link to="/docs/Chapters/control-systems" className={styles.chapterLink}>→ Control Systems</Link>
              <Link to="/docs/Chapters/perception" className={styles.chapterLink}>→ Perception</Link>
              <Link to="/docs/Chapters/sensors" className={styles.chapterLink}>→ Sensors</Link>
              <Link to="/docs/Chapters/motion-planning" className={styles.chapterLink}>→ Motion Planning</Link>
              <Link to="/docs/Chapters/locomotion" className={styles.chapterLink}>→ Locomotion</Link>
              <Link to="/docs/Chapters/manipulation" className={styles.chapterLink}>→ Manipulation</Link>
              <Link to="/docs/Chapters/ai-integration" className={styles.chapterLink}>→ AI Integration</Link>
              <Link to="/docs/Chapters/simulation" className={styles.chapterLink}>→ Simulation</Link>
              <Link to="/docs/Chapters/safety" className={styles.chapterLink}>→ Safety</Link>
            </div>
          </div>
        </section>

        <section className={styles.cta}>
          <div className={styles.container}>
            <h2>Ready to Learn?</h2>
            <p>Begin your journey into humanoid robotics today.</p>
            <Link className={styles.button} to="/docs/intro">
              Get Started Now
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}
