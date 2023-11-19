import React, { useState } from "react";
import "../styles/Signup.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye } from "@fortawesome/free-solid-svg-icons";
import { faEyeSlash } from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";
import { Button } from "@chakra-ui/react";
import { useSnackbar } from "notistack";


function Signup( {isLoggedIn, setIsLoggedIn} ) {
  const [showPassword, setShowPassword] = useState(false);
  const [showLogin, setShowLogin] = useState(false);
 
  const navigate = useNavigate();
  const {enqueueSnackbar}=useSnackbar()

  const [signupFormData, setSignupFormData] = useState({
    name: "",
    username: "",
    password: "",
    confirmPassword: "",
  });

  const [loginFormData, setLoginFormData] = useState({
    username: "",
    password: "",
  });

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const handleSignup = async () => {
    const passwordRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/;

    if (!passwordRegex.test(signupFormData.password)) {
      enqueueSnackbar('Password must include at least one uppercase letter, one lowercase letter, one special character, and be at least six characters long.', {variant: 'error'})
      return;
    }

    if (signupFormData.password !== signupFormData.confirmPassword) {
      enqueueSnackbar('Password and confirmation do not match.',{variant:'error'})
      
      return;
    }

    try {
      //  API request for signup
      const response = await fetch("/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(signupFormData),
      });

      if (response.ok) {
        const data = await response.json();
        setSignupFormData({
          name: "",
          username: "",
          password: "",
          confirmPassword: "",
        });
        enqueueSnackbar(`Hello, ${data.name} Account created successfully`, {variant:'success'})

        setShowLogin(false)
      } else {
        enqueueSnackbar('Signup failed', {variant:'error'})
      }
    } catch (error) {
     
      alert("Error during signup: " + error.message);
    }
  };

  const handleLogin = async () => {
    try {
      // API request for login
      const response = await fetch("/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginFormData),
      });

      if (response.ok) {
        
        setLoginFormData({ username: "", password: "" });
        enqueueSnackbar('Login Successful', {variant:'success'})

         setIsLoggedIn(true);
        navigate('/blogs')
      } else {
        enqueueSnackbar('Login Failed',{variant:'error'})
        
      }
    } catch (error) {
      console.error("Error during login:", error);
      alert("Error during login: " + error.message);
    }
  };

  const handleLogout = async () => {
    try {
      // Send a GET request to the server to log the user out
      const response = await fetch('/logout', {
        method: 'GET',
      });

  if (response.ok) {
    // Successful logout
    setIsLoggedIn(false);
  
    navigate('/'); //Redirect to appropriate route
  } else {
    // Handle logout failure
    console.error('Logout failed');
  }
} catch (error) {
  console.error('Error during logout:', error);
}
  };

  const showLoginSection = () => {
   
    setShowLogin(true); // Show the login section
  };

  const showSignupSection = () => {
    setShowLogin(false); // Show the signup section
  };

  return (
    <div className="login-container">
      <h1> Account</h1>
      {isLoggedIn ? (
        <div className="form">
          <h2>Logout</h2>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : !showLogin ? (
        <div className="form">
          <h2>Sign Up</h2>
          <input
            type="text"
            placeholder="Full Name"
            value={signupFormData.name}
            onChange={(e) =>
              setSignupFormData({ ...signupFormData, name: e.target.value })
            }
          />
          <input
            type="text"
            placeholder="Username"
            value={signupFormData.username}
            onChange={(e) =>
              setSignupFormData({ ...signupFormData, username: e.target.value })
            }
          />
          <div className="password-input">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={signupFormData.password}
              onChange={(e) =>
                setSignupFormData({
                  ...signupFormData,
                  password: e.target.value,
                })
              }
            />
            <span onClick={togglePasswordVisibility}>
              {showPassword ? (
                <FontAwesomeIcon icon={faEye} style={{ fontSize: "16px" }} />
              ) : (
                <FontAwesomeIcon
                  icon={faEyeSlash}
                  style={{ fontSize: "16px" }}
                />
              )}
            </span>
          </div>
          <div className="password-input">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Confirm Password"
              value={signupFormData.confirmPassword}
              onChange={(e) =>
                setSignupFormData({
                  ...signupFormData,
                  confirmPassword: e.target.value,
                })
              }
            />
            <span onClick={togglePasswordVisibility}>
              {showPassword ? (
                <FontAwesomeIcon icon={faEye} style={{ fontSize: "16px" }} />
              ) : (
                <FontAwesomeIcon
                  icon={faEyeSlash}
                  style={{ fontSize: "16px" }}
                />
              )}
            </span>
          </div>
          
          <Button _hover={{'bg':'black'}} colorScheme="blue" onClick={handleSignup}>Sign Up</Button>
          
          <p>
            Already have an account?{" "}
            <Button variant={'ghost'} colorScheme="blue" onClick={showLoginSection}>
              Login
            </Button>
          </p>
        </div>
      ) : (
        <div className="form">
          <h2>Login</h2>
          <input
            type="text"
            placeholder="Username"
            value={loginFormData.username}
            onChange={(e) =>
              setLoginFormData({ ...loginFormData, username: e.target.value })
            }
          />
          <div className="password-input">
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              value={loginFormData.password}
              onChange={(e) =>
                setLoginFormData({ ...loginFormData, password: e.target.value })
              }
            />
            <span onClick={togglePasswordVisibility}>
              {showPassword ? (
                <FontAwesomeIcon icon={faEye} style={{ fontSize: "16px" }} />
              ) : (
                <FontAwesomeIcon
                  icon={faEyeSlash}
                  style={{ fontSize: "16px" }}
                />
              )}
            </span>
          </div>
          <Button _hover={{'bg':'black'}} colorScheme="blue" onClick={handleLogin}>Login</Button>
          <p>
            Do not have an account?{" "}
            <Button colorScheme="blue" variant={'ghost'} onClick={showSignupSection}>
              Sign Up
            </Button>
          </p>
        </div>
      )}
      
    </div>
  );
}

export default Signup;
