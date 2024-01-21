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

function Tasters() {
    const [page, setPage] = useState(1);
    const [tasters, setTasters] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://localhost:20001/Taster`)
            .then((response) => response.json())
            .then((data) => {
                setTasters(data);
                setMaxDataSize(data.length);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, [page]);

    const renderTasters = () => {
        if (tasters) {
            const startIndex = (page - 1) * PAGE_SIZE;
            const endIndex = startIndex + PAGE_SIZE;
            const displayedTasters = tasters.slice(startIndex, endIndex);

            return displayedTasters.map((taster) => (
                <TableRow
                    key={taster.id}
                    style={{ background: "gray", color: "black" }}
                >
                    <TableCell component="td" align="center">{taster.id}</TableCell>
                    <TableCell component="td" scope="row">
                        {taster.name}
                    </TableCell>
                    <TableCell component="td" scope="row">
                        {taster.twitter_handle}
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
            <h1>Tasters</h1>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Taster Name</TableCell>
                            <TableCell>Twitter Handle</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {renderTasters()}
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

export default Tasters;
