function Gaps({ gaps }) {
    return(
        <div>
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

export default Gaps