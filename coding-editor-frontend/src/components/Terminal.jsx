import React, { useEffect, useRef } from 'react';

const Terminal = ({ output }) => {
  const terminalRef = useRef(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [output]);

  return (
    <pre ref={terminalRef} style={{ whiteSpace: 'pre-wrap', height: '100%', overflowY: 'auto' }}>
      {output}
    </pre>
  );
};

export default Terminal;