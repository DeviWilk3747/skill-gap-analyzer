function Skills({ skills, newSkillName, setNewSkillName, newProficiency, setNewProficiency, handleAddSkill, handleDeleteSkill }){
    return (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
                <h2 className="text-xl font-bold mb-4">My Skills</h2>
                <div className="flex gap-2 mb-4">
                <input
                    type="text"
                    placeholder="Skill name"
                    value={newSkillName}
                    onChange={(e) => setNewSkillName(e.target.value)}
                    className="felx-1 border border-gray-300 rounded px=3 py-2"
                />
                <select
                    value={newProficiency}
                    onChange={(e) => setNewProficiency(e.target.value)}
                    className="border border-gray-300 rounded px-3 py-2"
                >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                </select>
                <button 
                    onClick={handleAddSkill}
                    className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    >
                        Add Skill
                </button>
                </div>
                <ul className="space-y-2">
                {skills.map((skill) => (
                    <li key={skill.id} className="flex justify-between items-center border-b pb-2">
                        <span>{skill.skill_name} - {skill.proficiency}</span>
                        <button 
                            onClick={() => handleDeleteSkill(skill.id)}
                            className="text-red-600 text-sm hover:underline"
                            >
                                Delete
                            </button>
                    </li>
                ))}
                </ul>
        </div>
    )
}

export default Skills