import { useEffect, useState } from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";

const PAGE_SIZE = 10;

function Countries() {
    const [page, setPage] = useState(1);
    const [countries, setCountries] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://localhost:20001/Country`)
            .then((response) => response.json())
            .then((data) => {
                setCountries(data);
                setMaxDataSize(data.length);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, [page]);

    const renderCountries = () => {
        if (countries) {
            const startIndex = (page - 1) * PAGE_SIZE;
            const endIndex = startIndex + PAGE_SIZE;
            const displayedCountries = countries.slice(startIndex, endIndex);

            return displayedCountries.map((country) => (
                <TableRow
                    key={country.id}
                    style={{ background: "gray", color: "black" }}
                >
                    <TableCell component="td" align="center">{country.id}</TableCell>
                    <TableCell component="td" scope="row">
                        {country.name}
                    </TableCell>
                </TableRow>
            ));
        } else {
            return (
                <TableRow>
                    <TableCell colSpan={2}>
                        <CircularProgress />
                    </TableCell>
                </TableRow>
            );
        }
    };

    return (
        <>
            <h1>Countries</h1>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Country Name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {renderCountries()}
                    </TableBody>
                </Table>
            </TableContainer>
            {maxDataSize && (
                <div style={{ background: "black", padding: "1rem" }}>
                    <Pagination
                        style={{ color: "black" }}
                        variant="outlined"
                        shape="rounded"
                        color={"primary"}
                        onChange={(e, v) => {
                            setPage(v);
                        }}
                        page={page}
                        count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            )}
        </>
    );
}

export default Countries;
