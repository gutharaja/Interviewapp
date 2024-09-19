import React, { useState, useEffect } from 'react';

const AudioStreamer = () => {
  const [transcript, setTranscript] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState(null);
  let ws; // Declare WebSocket variable

  useEffect(() => {
    const setupWebSocket = () => {
      ws = new WebSocket('ws://localhost:5000');
      // ws = new WebSocket('ws://127.0.0.1:5000'); // Ensure WebSocket URL is correct'

      ws.onopen = () => console.log('WebSocket connection established');
      ws.onmessage = (event) => {
        const data = event.data;
        if (typeof data === 'string') {
          setTranscript((prev) => prev + '\n' + data); // Append incoming message to transcript
        } else {
          console.error('Received non-string data from WebSocket');
        }
      };

      ws.onerror = (err) => {
        console.error('WebSocket error:', err);
        setError('WebSocket connection error');
        setIsRecording(false);
      };

      ws.onclose = () => console.log('WebSocket connection closed');
    };

    const setupAudioStream = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const audioContext = new AudioContext();

        // Set up audio processing and WebSocket data sending
        const processor = audioContext.createScriptProcessor(4096, 1, 1);
        processor.onaudioprocess = (event) => {
          const inputBuffer = event.inputBuffer.getChannelData(0);
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(inputBuffer); // Send audio data to WebSocket server
          }
        };

        const source = audioContext.createMediaStreamSource(stream);
        source.connect(processor);
        processor.connect(audioContext.destination);
      } catch (err) {
        console.error('Audio streaming error:', err);
        setError('Audio streaming error');
        setIsRecording(false);
      }
    };

    if (isRecording) {
      setupWebSocket();
      setupAudioStream();
    } else {
      if (ws) ws.close(); // Close WebSocket connection when not recording
    }

    return () => {
      if (ws) ws.close(); // Cleanup WebSocket on component unmount
    };
  }, [isRecording]);

  return (
    <div>
      <button onClick={() => setIsRecording(!isRecording)}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <h3>Transcript:</h3>
        <pre>{transcript}</pre>
      </div>
    </div>
  );
};

export default AudioStreamer;