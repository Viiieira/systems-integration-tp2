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

function Provinces() {
    const [page, setPage] = useState(1);
    const [provinces, setProvinces] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://localhost:20001/Province`)
            .then((response) => response.json())
            .then((data) => {
                setProvinces(data);
                setMaxDataSize(data.length);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, [page]);

    const renderProvinces = () => {
        if (provinces) {
            const startIndex = (page - 1) * PAGE_SIZE;
            const endIndex = startIndex + PAGE_SIZE;
            const displayedProvinces = provinces.slice(startIndex, endIndex);

            return displayedProvinces.map((province) => (
                <TableRow
                    key={province.id}
                    style={{ background: "gray", color: "black" }}
                >
                    <TableCell component="td" align="center">{province.id}</TableCell>
                    <TableCell component="td" scope="row">
                        {province.name}
                    </TableCell>
                    <TableCell component="td" align="center">
                        {province.id_country}
                    </TableCell>
                </TableRow>
            ));
        } else {
            return (
                <TableRow>
                    <TableCell colSpan={3}>
                        <CircularProgress />
                    </TableCell>
                </TableRow>
            );
        }
    };

    return (
        <>
            <h1>Provinces</h1>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Province Name</TableCell>
                            <TableCell align="center">Country ID</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {renderProvinces()}
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

export default Provinces;
