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

function WinesByCountry() {
  // State hooks
  const [selectedCountry, setSelectedCountry] = useState("");
  const [countries, setCountries] = useState([]);
  const [procData, setProcData] = useState(null);
  const [gqlData, setGQLData] = useState(null);

  useEffect(() => {
    // Fetch countries from the API endpoint
    const fetchCountries = async () => {
      try {
        const response = await fetch("http://localhost:20004/api/country");
        const data = await response.json();
        const countriesArray =
          data?.countries?.map((countryArray) => countryArray[0]) || [];
        setCountries(countriesArray);
      } catch (error) {
        console.error("Error fetching countries:", error);
      }
    };

    // Call the fetchCountries function when the component mounts
    fetchCountries();
  }, []); // Empty dependency array ensures this effect runs only once on mount

  useEffect(() => {
    setProcData(null);
    setGQLData(null);

    if (selectedCountry) {
      setTimeout(() => {
        console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
        // Modify this part based on your actual data fetching logic
        // For now, setting procData to an empty array
        setProcData([]);
      }, 500);

      setTimeout(() => {
        console.log(`fetching from ${process.env.REACT_APP_API_GRAPHQL_URL}`);
        // Modify this part based on your actual data fetching logic
        // For now, setting gqlData to an empty array
        setGQLData([]);
      }, 1000);
    }
  }, [selectedCountry]);

  return (
    <>
      <h1>Top Teams</h1>

      <Container
        maxWidth="100%"
        sx={{
          backgroundColor: "background.default",
          padding: "2rem",
          borderRadius: "1rem",
        }}
      >
        <Box>
          <h2 style={{ color: "white" }}>Options</h2>
          <FormControl fullWidth>
            <InputLabel id="countries-select-label">Country</InputLabel>
            <Select
              labelId="countries-select-label"
              id="demo-simple-select"
              value={selectedCountry}
              label="Country"
              onChange={(e, v) => {
                setSelectedCountry(e.target.value);
              }}
            >
              <MenuItem value={""}>
                <em>None</em>
              </MenuItem>
              {countries.map((c) => (
                <MenuItem key={c} value={c}>
                  {c}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </Container>

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
        <h2>
          Results <small>(PROC)</small>
        </h2>
        {procData ? (
          <ul>
            {procData.map((data, index) => (
              <li key={index}>{data.team}</li>
            ))}
          </ul>
        ) : selectedCountry ? (
          <CircularProgress />
        ) : (
          "--"
        )}
        <h2>
          Results <small>(GraphQL)</small>
        </h2>
        {gqlData ? (
          <ul>
            {gqlData.map((data, index) => (
              <li key={index}>{data.team}</li>
            ))}
          </ul>
        ) : selectedCountry ? (
          <CircularProgress />
        ) : (
          "--"
        )}
      </Container>
    </>
  );
}

export default WinesByCountry;
