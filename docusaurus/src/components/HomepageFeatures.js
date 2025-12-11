import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'AI Agents & Reasoning',
    Svg: require('../../static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Learn how intelligent agents think, plan, and interact with humans in real-world
        environments using modern AI architectures.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    Svg: require('../../static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Explore the fundamentals of humanoid robot design, motion, control, and human–robot
        collaboration.
      </>
    ),
  },
  {
    title: 'Hands-On Physical AI Projects',
    Svg: require('../../static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Practical labs, simulations, and build your own robotics challenges to help you apply
        concepts step by step.
      </>
    ),
  },
];

function Feature({ Svg, title, description }) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} alt={title} />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
