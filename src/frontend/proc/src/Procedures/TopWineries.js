import React, { useEffect, useState } from "react";
import {
  Box,
  CircularProgress,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from "@mui/material";

function TopWineries() {
  const [procData, setProcData] = useState(null);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []); // Empty dependency array means this effect runs once when the component mounts

  const fetchData = () => {
    setLoading(true); // Set loading to true when fetching starts

    // Reset procData when selectedCountry changes
    setProcData(null);

    // Simulate fetching data from the specified endpoint
    fetch(`http://localhost:20004/api/winery`)
      .then((response) => response.json())
      .then((data) => setProcData(data.wineries))
      .catch((error) => console.error("Error fetching wineries:", error))
      .finally(() => setLoading(false)); // Set loading to false when fetching is complete
  };

  return (
    <>
      <h1>Top Wineries</h1>

      <Container
        maxWidth="100%"
        sx={{
          backgroundColor: "info.dark",
          padding: "2rem",
          marginTop: "2rem",
          borderRadius: "1rem",
          color: "white",
        }}
      >
        <h2>Results</h2>
        {loading ? (
          <CircularProgress />
        ) : procData ? (
          <ul>
            {procData.map((winery, index) => (
              <li key={index}>{winery}</li>
            ))}
          </ul>
        ) : selectedCountry ? (
          <div>No data available</div>
        ) : (
          "--"
        )}
      </Container>
    </>
  );
}

export default TopWineries;
