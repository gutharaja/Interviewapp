import logo from './logo.svg';
import './App.css';
import React from 'react';
  import AudioStreamer from './AudioStreamer';

function App() {
  return (
    <div className="App">
      <h1>Live Transcription</h1>
      <AudioStreamer />
    </div>
  );
}

export default App;
