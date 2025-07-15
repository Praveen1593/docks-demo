import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [videoUrl, setVideoUrl] = useState("");

  useEffect(() => {
    axios.get("http://localhost:8000/api/alerts").then(res => setAlerts(res.data));
    axios.get("http://localhost:8000/api/video").then(res => setVideoUrl(res.data.url));
  }, []);

  return (
    <div>
      <h1>Obscure Eye Dashboard</h1>
      <h2>Live Video</h2>
      {videoUrl && <img src={videoUrl} alt="Live Stream" width="480" />}
      <h2>Alerts</h2>
      <ul>
        {alerts.map(alert => (
          <li key={alert.id}>
            <b>{alert.type.toUpperCase()}</b>: {alert.message} <i>{alert.timestamp}</i>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;