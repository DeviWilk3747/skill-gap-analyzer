import { useState, useEffect } from "react";
import Login from "./Login";
import Skills from "./Skills";
import Postings from "./Postings";
import Gaps from "./Gaps"

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
      <Skills
        skills={skills}
        newSkillName={newSkillName}
        setNewSkillName={setNewSkillName}
        newProficiency={newProficiency}
        setNewProficiency={setNewProficiency}
        handleAddSkill={handleAddSkill}
        handleDeleteSkill={handleDeleteSkill}
      />
      <Postings
        postings={postings}
        title={title}
        setTitle={setTitle}
        company={company}
        setCompany={setCompany}
        rawText={rawText}
        setRawText={setRawText}
        handleAddPosting={handleAddPosting}
        handleDeletePosting={handleDeletePosting}
      />
      <Gaps gaps={gaps} />
    </div>
    );
  }

  return (
    <Login  
      email={email}
      setEmail={setEmail}
      password={password}
      setPassword={setPassword}
      handleLogin={handleLogin}
      message={message}
    />
  );
}

export default App;