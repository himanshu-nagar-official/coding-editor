import React, { useState, useEffect, useRef } from 'react';
import CodeEditor from './components/CodeEditor';
import Terminal from './components/Terminal';

export default function App() {
  const [code, setCode] = useState(`# Write your Python code here\nprint("Hello, World!")`);
  const [terminalOutput, setTerminalOutput] = useState('');
  const [userInput, setUserInput] = useState('');
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket('wss://35.244.58.188/ws/code-runner/');
    ws.current.onopen = () => setTerminalOutput("✅ Connected to backend\n");
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.output) setTerminalOutput((prev) => prev + data.output);
    };
    ws.current.onclose = () => setTerminalOutput((prev) => prev + "\n❌ Disconnected from backend\n");
    return () => ws.current && ws.current.close();
  }, []);

  const runCode = () => {
    setTerminalOutput('');
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify({ code, userInput }));
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>🚀 Code Playground for Young Coders</header>

      <div style={styles.main}>
        <div style={styles.leftPane}>
          <div style={styles.editorBox}>
            <CodeEditor code={code} setCode={setCode} />
          </div>
          <div style={{ marginTop: '1rem' }}>
            <label style={{ fontWeight: 'bold' }}>Input:</label>
            <textarea
              rows="4"
              style={{ width: '100%', marginTop: '0.5rem' }}
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Example for multiple inputs:
John [For String: name = input()]
25 [For Number: number = int(input())]
1 3 6 5 4 [For List: listInput = list(map(int, input().split()))]"
            />
          </div>
          <button style={styles.runButton} onClick={runCode}>▶ Run Code</button>
        </div>

        <div style={styles.terminalPane}>
          <h3 style={styles.terminalHeader}>🖥 Terminal</h3>
          <div style={styles.terminalBox}>
            <Terminal output={terminalOutput} />
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    height: '100vh',
    width: '100vw',
    fontFamily: 'Segoe UI, sans-serif',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    backgroundColor: '#282c34',
    color: '#61dafb',
    textAlign: 'center',
    padding: '1rem',
    fontSize: '1.5rem',
  },
  main: {
    flex: 1,
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    padding: '1rem',
    gap: '1rem',
    boxSizing: 'border-box',
  },
  leftPane: {
    flex: 1,
    minWidth: '300px',
    display: 'flex',
    flexDirection: 'column',
  },
  editorBox: {
    flex: 1,
    minHeight: '300px',
    maxHeight: '50vh',
    overflowY: 'auto',
    border: '1px solid #ccc',
    borderRadius: '6px',
    padding: '0.5rem',
    backgroundColor: '#f9f9f9',
  },
  runButton: {
    marginTop: '1rem',
    padding: '0.75rem',
    backgroundColor: '#28a745',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    fontSize: '1rem',
    cursor: 'pointer',
    alignSelf: 'flex-start',
  },
  terminalPane: {
    flex: 1,
    minWidth: '300px',
    display: 'flex',
    flexDirection: 'column',
    backgroundColor: '#1e1e1e',
    borderRadius: '6px',
    padding: '1rem',
    color: '#0f0',
    height: 'auto',
    maxHeight: '60vh',
    overflow: 'hidden',
  },
  terminalHeader: {
    marginBottom: '0.5rem',
  },
  terminalBox: {
    flex: 1,
    backgroundColor: '#000',
    borderRadius: '6px',
    padding: '1rem',
    overflowY: 'auto',
    whiteSpace: 'pre-wrap',
    fontFamily: 'monospace',
    height: '100%',
  },
};