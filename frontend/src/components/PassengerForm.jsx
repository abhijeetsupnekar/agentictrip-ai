import React, { useState } from "react";

const PassengerForm = ({ onSubmit, onCancel }) => {
    const [formData, setFormData] = useState({
        name: "",
        age: "",
        gender: "",
        email: "",
        phone: "",
    });

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <div
            className="bg-white/5 border border-white/10 rounded-3xl p-6 text-white backdrop-blur-xl"
        >
            <h2 className="text-3xl font-bold mb-6">
                Passenger Details
            </h2>

            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="name"
                    placeholder="Full Name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    style={inputStyle}
                />

                <input
                    type="number"
                    name="age"
                    placeholder="Age"
                    value={formData.age}
                    onChange={handleChange}
                    required
                    style={inputStyle}
                />

                <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleChange}
                    required
                    style={{
                        ...inputStyle,
                        backgroundColor: "#111",
                        color: "white",
                    }}
                >
                    <option value="">Select Gender</option>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Other">Other</option>
                </select>

                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    style={inputStyle}
                />

                <input
                    type="text"
                    name="phone"
                    placeholder="Phone Number"
                    value={formData.phone}
                    onChange={handleChange}
                    required
                    style={inputStyle}
                />

                <div style={{ marginTop: "15px" }}>
                    <button type="submit" style={buttonStyle}>
                        Continue
                    </button>

                    <button
                        type="button"
                        onClick={onCancel}
                        style={{
                            ...buttonStyle,
                            backgroundColor: "#ccc",
                            marginLeft: "10px",
                        }}
                    >
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    );
};

const inputStyle = {
    width: "100%",
    padding: "14px",
    marginTop: "12px",
    borderRadius: "14px",
    border: "1px solid rgba(255,255,255,0.1)",
    background: "rgba(255,255,255,0.05)",
    color: "white",
    outline: "none",
};
const buttonStyle = {
    padding: "12px 20px",
    border: "none",
    borderRadius: "14px",
    backgroundColor: "white",
    color: "black",
    cursor: "pointer",
    fontWeight: "600",
};
export default PassengerForm;