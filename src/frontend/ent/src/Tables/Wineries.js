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

function Wineries() {
    const [page, setPage] = useState(1);
    const [wineries, setWineries] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://localhost:20001/Winery`)
            .then((response) => response.json())
            .then((data) => {
                setWineries(data);
                setMaxDataSize(data.length);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, [page]);

    const renderWineries = () => {
        if (wineries) {
            const startIndex = (page - 1) * PAGE_SIZE;
            const endIndex = startIndex + PAGE_SIZE;
            const displayedWineries = wineries.slice(startIndex, endIndex);

            return displayedWineries.map((winery) => (
                <TableRow
                    key={winery.id}
                    style={{ background: "gray", color: "black" }}
                >
                    <TableCell component="td" align="center">{winery.id}</TableCell>
                    <TableCell component="td" scope="row">
                        {winery.name}
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
            <h1>Wineries</h1>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Winery Name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {renderWineries()}
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

export default Wineries;
