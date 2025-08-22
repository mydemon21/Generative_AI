import React, { useState, useRef } from 'react';
import axios from 'axios';
import html2pdf from 'html2pdf.js';
import './App.css';

function App() {
  const [description, setDescription] = useState('');
  const [resume, setResume] = useState(null);
  const [loading, setLoading] = useState(false);
  const [accentColor, setAccentColor] = useState('#333');
  const resumeRef = useRef();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResume(null);
    try {
      const response = await axios.post('http://localhost:5001/api/generate-resume', { description });
      setResume(response.data);
    } catch (error) {
      console.error('Error generating resume:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = () => {
    const element = resumeRef.current;
    const opt = {
      margin:       0.5,
      filename:     'resume.pdf',
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { scale: 2 },
      jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
    html2pdf().from(element).set(opt).save();
  };

  const resumeStyle = {
    '--accent-color': accentColor,
  };

  return (
    <div className="App">
      <header className="App-header" style={{ backgroundColor: accentColor }}>
        <h1>AI Resume Builder</h1>
      </header>
      <main>
        <div className="controls">
          <label htmlFor="accent-color">Accent Color:</label>
          <input
            type="color"
            id="accent-color"
            value={accentColor}
            onChange={(e) => setAccentColor(e.target.value)}
          />
        </div>
        <form onSubmit={handleSubmit}>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Tell us about your professional background... Mention your skills, experience, and education."
            rows="10"
          />
          <button type="submit" disabled={loading} style={{ backgroundColor: accentColor }}>
            {loading ? 'Generating...' : 'Generate Resume'}
          </button>
        </form>
        {loading && <p>Loading...</p>}
        {resume && (
          <>
            <div className="resume" ref={resumeRef} style={resumeStyle}>
              <div className="resume-header">
                <h2>{resume.name}</h2>
                <p>{resume.email} | {resume.phone}</p>
              </div>
              <div className="resume-section">
                <h3>Summary</h3>
                <p>{resume.summary}</p>
              </div>
              <div className="resume-section">
                <h3>Experience</h3>
                {resume.experience.map((exp, index) => (
                  <div key={index} className="experience-item">
                    <h4>{exp.title} at {exp.company}</h4>
                    <p><em>{exp.dates}</em></p>
                    <p>{exp.description}</p>
                  </div>
                ))}
              </div>
              <div className="resume-section">
                <h3>Education</h3>
                {resume.education.map((edu, index) => (
                  <div key={index} className="education-item">
                    <h4>{edu.degree}</h4>
                    <p>{edu.university} ({edu.dates})</p>
                  </div>
                ))}
              </div>
              <div className="resume-section">
                <h3>Skills</h3>
                <ul className="skills-list">
                  {resume.skills.map((skill, index) => (
                    <li key={index}>{skill}</li>
                  ))}
                </ul>
              </div>
            </div>
            <button onClick={handleDownloadPdf} className="download-btn">
              Download PDF
            </button>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
