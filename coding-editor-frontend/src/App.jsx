import React, { useState, useEffect, useRef } from 'react';
import CodeEditor from './components/CodeEditor';
import Terminal from './components/Terminal';

export default function App() {
  const [code, setCode] = useState(`# Write your Python code here\nprint("Hello, World!")`);
  const [terminalOutput, setTerminalOutput] = useState('');
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://127.0.0.1:8000/ws/code-runner/');
    ws.current.onopen = () => {
      setTerminalOutput((o) => o + "Connected to backend.\n");
    };
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.output) {
        setTerminalOutput((o) => o + data.output);
      }
    };
    ws.current.onclose = () => {
      setTerminalOutput((o) => o + "\nDisconnected from backend.\n");
    };
    return () => {
      ws.current.close();
    };
  }, []);

  const runCode = () => {
    setTerminalOutput('');
    ws.current.send(JSON.stringify({ code }));
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', padding: '1rem' }}>
        <h2>Code Editor</h2>
        <CodeEditor code={code} setCode={setCode} />
        <button onClick={runCode} style={{ marginTop: '1rem', padding: '0.5rem' }}>
          Run Code
        </button>
      </div>

      <div style={{ flex: 1, backgroundColor: '#000', color: '#0f0', padding: '1rem', fontFamily: 'monospace', overflowY: 'auto' }}>
        <h2>Terminal</h2>
        <Terminal output={terminalOutput} />
      </div>
    </div>
  );
}