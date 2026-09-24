import { useState, useEffect } from "react";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [skills, setSkills] = useState([]);
  const [newSkillName, setNewSkillName] = useState("");
  const [newProficiency, setNewProficiency] = useState("Beginner")
  const [gaps, setGaps] = useState([])

  const [postings, setPostings] = useState([]);
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [rawText, setRawText] = useState("");

  const handleLogin = () => {
    fetch("http://localhost:5000/login", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          setLoggedIn(true);
        } else {
          setMessage(data.error);
        }
      });
  };

  const handleAddSkill = () => {
    fetch("http://localhost:5000/api/skills", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        skill_name: newSkillName,
        proficiency: newProficiency,
      }),
    })
    .then((response) => response.json())
    .then((newSkill) => {
      setSkills([...skills, newSkill])
    });
  };
  
  const handleDeleteSkill = (skillId) => {
    fetch(`http://localhost:5000/api/skills/${skillId}`, {
      method: "DELETE",
      credentials: "include",
    })
    .then(() => {
      setSkills(skills.filter((skill) => skill.id !== skillId));
    });
  };

  const handleAddPosting = () => {
    fetch("http://localhost:5000/api/postings", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: title,
        company: company,
        raw_text: rawText,
      }),
    })
  
    .then((response) => response.json())
    .then((newPosting) => {
      setPostings([...postings, newPosting]);
      setTitle("");
      setCompany("");
      setRawText("");
    });
  };

  const handleDeletePosting = (postingId) => {
    fetch(`http://localhost:5000/api/postings/${postingId}`, {
      method: "DELETE",
      credentials: "include",
    })
    .then(() => {
      setPostings(postings.filter((posting) => posting.id !== postingId));
    });
  };

    useEffect(() => {
      if (loggedIn) {
        fetch("http://localhost:5000/api/skills", {
          credentials: "include",
        })
        .then((response) => response.json())
        .then((data) => setSkills(data));

        fetch("http://localhost:5000/api/postings", {
           credentials: "include"
        })
        .then((response) => response.json())
        .then((data) => setPostings(data));

        fetch("http://localhost:5000/api/gaps",{
          credentials: "include"
        })
        .then((response) => response.json())
        .then ((data) => setGaps(data));
      }
    }, [loggedIn]);

    useEffect(() => {
      fetch ("http://localhost:5000/api/me", {
        credentials: "include",
      })
      .then((response) => {
        if (response.ok) {
          setLoggedIn(true);
        }
      });
    }, []);

  if (loggedIn) {
    return (
      <div>
        <h1>Skill Gap Analyzer</h1>
        <h2>My Skills</h2>
        <div>
          <input
            type="text"
            placeholder="Skill name"
            value={newSkillName}
            onChange={(e) => setNewSkillName(e.target.value)}
          />
          <select
            value={newProficiency}
            onChange={(e) => setNewProficiency(e.target.value)}
          >
            <option value="Beginner">Beginner</option>
            <option value="Intermediate">Intermediate</option>
            <option value="Advanced">Advanced</option>
          </select>
          <button onClick={handleAddSkill}>Add Skill</button>
        </div>
        <ul>
          {skills.map((skill) => (
            <li key={skill.id}>
              {skill.skill_name} - {skill.proficiency}
              <button onClick={() => handleDeleteSkill(skill.id)}>Delete</button>
            </li>
          ))}
        </ul>

        <h2>Add a Posting</h2>
        <input
          type="text"
          placeholder="Job title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input 
          type="text"
          placeholder="Company"
          value={company}
          onChange={(e) => setCompany(e.target.value)}
        />
        <textarea
          placeholder="Paste the job description"
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
        />
        <button onClick={handleAddPosting}>Analyze Posting</button>
        <h2>My Postings</h2>
        <ul>
          {postings.map((posting) => (
            <li key={posting.id}>
              <strong>{posting.title}</strong> - {posting.company}
              <div>Skills found: {posting.skills.join(", ")}</div>
              <button onClick={() => handleDeletePosting(posting.id)}>Delete</button>
            </li>
          ))}
        </ul>

        <h2>Skill Gaps</h2>
        <ul>
          {gaps.map((gap) => (
            <li key={gap.skill}>
              {gap.skill} appears in {gap.count} postings
            </li>
          ))}
        </ul>
      </div>
    );
  }

  return (
    <div>
      <h1>Skill Gap Analyzer</h1>
      <h2>Log In</h2>

      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={handleLogin}>Log In</button>

      {message && <p>{message}</p>}
    </div>
  );
}

export default App;