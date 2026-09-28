import { use, useState } from "react";
function Register({ email, setEmail, password, setPassword, handleRegister, message, setShowRegister }) {
    const[showPassword, setShowPassword] = useState(false);
    
    return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
        <h1 className="text-2xl font-bold text-center mb-1">Skill Gap Analyzer</h1>
        <h2 className="text-lg text-gray-500 text-center mb-6">Create Account</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-3"
        />

        <div className="relative mb-4">
            <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full border border-gray-300 rounded px-3 py-2 pr-16"
            />
            <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-sm text-blue-600"
            >
                {showPassword ? "Hide" : "Show"}
            </button>
        </div>

        <button
          onClick={handleRegister}
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Register
        </button>

        {message && <p className="text-red-600 text-sm mt-3">{message}</p>}

        <p className="text-sm text-center mt-4">
          Already have an account?{" "}
          <button
            onClick={() => setShowRegister(false)}
            className="text-blue-600 hover:underline"
          >
            Log in
          </button>
        </p>
      </div>
    </div>
  );
}

export default Register;