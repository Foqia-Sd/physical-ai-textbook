// docusaurus/src/theme/Navbar/index.js
import React from 'react';
import OriginalNavbar from '@theme-original/Navbar';
import AuthNavbar from '@site/src/components/AuthNavbar';

export default function Navbar(props) {
  return (
    <>
      <OriginalNavbar {...props} />
      <AuthNavbar />
    </>
  );
}