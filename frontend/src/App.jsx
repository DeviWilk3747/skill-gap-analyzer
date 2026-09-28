import { useState, useEffect } from "react";
import Login from "./Login";
import Skills from "./Skills";
import Postings from "./Postings";
import Gaps from "./Gaps";
import Register from "./Register";
const API = import.meta.env.VITE_API_URL;

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [showRegister, setShowRegister] = useState(false)
  const [skills, setSkills] = useState([]);
  const [newSkillName, setNewSkillName] = useState("");
  const [newProficiency, setNewProficiency] = useState("Beginner")
  const [gaps, setGaps] = useState([])

  const [postings, setPostings] = useState([]);
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [rawText, setRawText] = useState("");

  const handleLogin = () => {
    fetch(`${API}/login`, {
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

  const handleRegister = () => {
    fetch(`${API}/register`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({email, password}),
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

  const handleLogout = () => {
    fetch(`${API}/logout`, {
      method: "POST",
      credentials: "include"
    })
    .then(() => {
      setLoggedIn(false);
      setSkills([]);
      setPostings([]);
      setGaps([]);
    });
  };

  const handleAddSkill = () => {
    fetch(`${API}/api/skills`, {
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
    fetch(`${API}/api/skills/${skillId}`, {
      method: "DELETE",
      credentials: "include",
    })
    .then(() => {
      setSkills(skills.filter((skill) => skill.id !== skillId));
    });
  };

  const handleAddPosting = () => {
    fetch(`${API}/api/postings`, {
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
      fetch(`${API}/api/gaps`, {
        credentials:"include"
      })
      .then((response) => response.json())
      .then ((data) => setGaps(data));
    });
  };

  const handleDeletePosting = (postingId) => {
    fetch(`${API}/api/postings/${postingId}`, {
      method: "DELETE",
      credentials: "include",
    })
    .then(() => {
      setPostings(postings.filter((posting) => posting.id !== postingId));
      fetch(`${API}/api/gaps`, {
        credentials:"include"
      })
      .then((response) => response.json())
      .then ((data) => setGaps(data));
    });
  };

    useEffect(() => {
      if (loggedIn) {
        fetch(`${API}/api/skills`, {
          credentials: "include",
        })
        .then((response) => response.json())
        .then((data) => setSkills(data));

        fetch(`${API}/api/postings`, {
           credentials: "include"
        })
        .then((response) => response.json())
        .then((data) => setPostings(data));

        fetch(`${API}/api/gaps`,{
          credentials: "include"
        })
        .then((response) => response.json())
        .then ((data) => setGaps(data));
      }
    }, [loggedIn]);

    useEffect(() => {
      fetch (`${API}/api/me`, {
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
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="max-w-2xl mx-auto px-4">
          <h1 className="text-3xl font-bold text-center mb-6">Skill Gap Analyzer</h1>
          <div className="flex justify-end mb-4">
            <button 
              onClick={handleLogout}
              className="text-md font-small text-gray-700 hover:underline"
              >
                Logout
            </button>
          </div>
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
    </div>
    );
  }
  if (showRegister) {
    return (
      <Register
        email={email}
        setEmail={setEmail}
        password={password}
        setPassword={setPassword}
        handleRegister={handleRegister}
        message={message}
        setShowRegister={setShowRegister}
      />
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
      setShowRegister={setShowRegister}
    />
  );
}

export default App;