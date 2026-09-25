function Login({ email, setEmail, password, setPassword, handleLogin, message}){
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
                <h1 className="text-2xl font-bold text-center mb-1">Skill Gap Analyzer</h1>
                <h2 className="text-lg text-gray-500 text-center mb-6">Log In</h2>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full border border-gray-300 rounded px-3 py-2 mb-3"
                />

                <input 
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full border border-gray-300 rounded px-3 py-2 mb-4"
                />

                <button onClick={handleLogin}
                className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
                >
                    Log In
                </button>

                {message && <p className="text-red-600 text-sm mt-3">{message}</p>}
            </div>
        </div>
    );
}

export default Login;