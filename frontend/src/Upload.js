import React, { useState } from "react";
import { predictImage } from "./api";

function Upload() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);

  const submitImage = async () => {
    const formData = new FormData();
    formData.append("image", image);

    const res = await predictImage(formData);
    setResult(res.data);
  };

  return (
    <div>
      <h2>Medical Image Report Generator</h2>
      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <button onClick={submitImage}>Generate Report</button>

      {result && (
        <div>
          <h3>Diagnosis: {result.diagnosis}</h3>
          <p>Confidence: {result.confidence.toFixed(2)}%</p>
          <pre>{result.report}</pre>
        </div>
      )}
    </div>
  );
}

export default Upload;
