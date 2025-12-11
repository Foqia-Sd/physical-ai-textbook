/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

module.exports = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Chapter 1: The Robotic Nervous System',
      items: ['chapter1/module1'],
    },
    {
      type: 'category',
      label: 'Chapter 2: The Digital Twin',
      items: ['chapter2/module2'],
    },
    {
      type: 'category',
      label: 'Chapter 3: The AI-Robot Brain',
      items: ['chapter3/module3'],
    },
    {
      type: 'category',
      label: 'Chapter 4: Vision-Language-Action (VLA)',
      items: ['chapter4/module4'],
    },
  ],
};
