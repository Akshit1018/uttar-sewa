import React from 'react';

const PageShell = ({ children, wide = false, className = '' }) => {
  return (
    <div className={`page-shell ${wide ? 'page-shell-wide' : ''} ${className}`.trim()}>
      <div className="page-shell-inner">
        {children}
      </div>
    </div>
  );
};

export default PageShell;
