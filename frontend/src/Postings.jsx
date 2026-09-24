function Postings({ postings, title, setTitle, company, setCompany, rawText, setRaWText, handleAddPosting, handleDeletePosting }) {
    return (
        <div>
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
        </div>
    );
}
export default Postings