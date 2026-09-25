function Postings({ postings, title, setTitle, company, setCompany, rawText, setRawText, handleAddPosting, handleDeletePosting }) {
    return (
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
            <h2 className="text-xl font-bold mb-4">Add a Posting</h2>
            <input
            type="text"
            placeholder="Job title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mb-3"
            />
            <input 
            type="text"
            placeholder="Company"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mb-3"
            />
            <textarea
            placeholder="Paste the job description"
            value={rawText}
            onChange={(e) => setRawText(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 mb-3"
            />
            <button
                onClick={handleAddPosting}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Analyze Posting</button>
            <h2 className="text-xl font-bold mb-4">My Postings</h2>
            <ul className="space-y-2">
            {postings.map((posting) => (
                <li key={posting.id} className="flex justify-between items-start border-b pb-2">
                    <div>
                        <strong>{posting.title}</strong> - {posting.company}
                        <div>Skills found: {posting.skills.join(", ")}</div>
                    </div>
                    <button 
                        onClick={() => handleDeletePosting(posting.id)}
                        className="text-red-600 text-sm hover:underline">Delete</button>
                </li>
            ))}
            </ul>
        </div>
    );
}
export default Postings