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
    const [selectedCountry, setSelectedCountry] = useState("");
    const [procData, setProcData] = useState(null);
    const [countries, setCountries] = useState([]);
    const [loadingCountries, setLoadingCountries] = useState(true);
    const [loadingWineData, setLoadingWineData] = useState(false);

    useEffect(() => {
        // Fetch countries from the specified endpoint
        fetch("http://localhost:20004/api/country")
            .then((response) => response.json())
            .then((data) => {
                setCountries(data.countries || []);
                setLoadingCountries(false);
            })
            .catch((error) => {
                console.error("Error fetching countries:", error);
                setLoadingCountries(false);
            });
    }, []);

    useEffect(() => {
        setProcData(null);

        if (selectedCountry) {
            // Fetch wine data based on the selected country
            setLoadingWineData(true);
            fetch(`http://localhost:20004/api/wine?country=${selectedCountry}`)
                .then((response) => response.json())
                .then((data) => {
                    setProcData(data.wines || []);
                })
                .catch((error) => {
                    console.error("Error fetching wine data:", error);
                })
                .finally(() => {
                    setLoadingWineData(false);
                });
        }
    }, [selectedCountry]);

    return (
        <>
            <h1>Wines By Country</h1>

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
                        <InputLabel id="countries-select-label">
                            Country
                        </InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedCountry}
                            label="Country"
                            onChange={(e) => setSelectedCountry(e.target.value)}
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
                {loadingWineData ? (
                    <CircularProgress />
                ) : procData ? (
                    <ul>
                        {procData.map((wine, index) => (
                            <li key={index}>{wine}</li>
                        ))}
                    </ul>
                ) : selectedCountry ? (
                    <div>No wine data available</div>
                ) : (
                    "--"
                )}
            </Container>
        </>
    );
}

export default WinesByCountry;
