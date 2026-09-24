function Login({ email, setEmail, password, setPassword, handleLogin, message}){
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

export default Login;