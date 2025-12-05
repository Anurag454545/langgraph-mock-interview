import React, { useState } from 'react';
import { createSession, submitAnswer } from './api';

export default function Interview() {
  const [jd, setJd] = useState('');
  const [key, setKey] = useState(null);
  const [q, setQ] = useState(null);
  const [ans, setAns] = useState('');
  const [history, setHistory] = useState([]);

  async function start() {
    if (!jd) return alert('Paste a JD');
    let res = await createSession(jd);
    setKey(res.session_key);
    setQ(res.current_question);
  }

  async function send() {
    let res = await submitAnswer(key, q.id, ans);
    setHistory([...history, { q, ans, feedback: res.feedback }]);
    setAns('');
    setQ(res.next_question);
    if (res.done) alert('Interview finished');
  }

  return (
    <div>
      {!key && (
        <>
          <textarea value={jd} onChange={(e) => setJd(e.target.value)} rows='8' style={{ width: '100%' }} />
          <button onClick={start}>Start Interview</button>
        </>
      )}

      {key && q && (
        <>
          <h3>Question:</h3>
          <div>{q.text}</div>
          <textarea value={ans} onChange={(e) => setAns(e.target.value)} rows='5' style={{ width: '100%' }} />
          <button onClick={send}>Submit Answer</button>
        </>
      )}

      <h4>History</h4>
      {history.map((h, i) => (
        <div key={i} style={{ border: '1px solid #ccc', margin: '10px', padding: '10px' }}>
          <b>Q:</b> {h.q.text}
          <br />
          <b>A:</b> {h.ans}
          <br />
          <b>Feedback:</b> {JSON.stringify(h.feedback)}
        </div>
      ))}
    </div>
  );
}
