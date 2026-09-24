function Skills({ skills, newSkillName, setNewSkillName, newProficiency, setNewProficiency, handleAddSkill, handleDeleteSkill }){
    return (
        <div>
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
        </div>
    )
}

export default Skills