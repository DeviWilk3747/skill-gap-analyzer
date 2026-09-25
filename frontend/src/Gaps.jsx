function Gaps({ gaps }) {
    return(
        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
            <h2 className="text-xl font-bold mb-4">Skill Gaps</h2>
                <ul className="space-y-2">
                {gaps.map((gap) => (
                    <li key={gap.skill} className="flex justify-between items-center border-b pb-2">
                    {gap.skill} appears in {gap.count} postings
                    </li>
                ))}
                </ul>
        </div>
    );
}

export default Gaps