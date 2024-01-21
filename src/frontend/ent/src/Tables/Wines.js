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

function Wines() {
    const [page, setPage] = useState(1);
    const [wines, setWines] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(0);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://localhost:20001/Wine`)
            .then((response) => response.json())
            .then((data) => {
                setWines(data);
                setMaxDataSize(data.length);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching data:", error);
                setLoading(false);
            });
    }, [page]);

    const renderWines = () => {
        if (wines) {
            const startIndex = (page - 1) * PAGE_SIZE;
            const endIndex = startIndex + PAGE_SIZE;
            const displayedWines = wines.slice(startIndex, endIndex);

            return displayedWines.map((wine) => (
                <TableRow
                    key={wine.id}
                    style={{ background: "gray", color: "black" }}
                >
                    <TableCell component="td" align="center">{wine.id}</TableCell>
                    <TableCell component="td" scope="row">
                        {wine.name}
                    </TableCell>
                    <TableCell component="td" align="center">
                        {wine.points}
                    </TableCell>
                    <TableCell component="td" align="center">
                        {wine.price}
                    </TableCell>
                    <TableCell component="td" align="center">
                        {wine.variety}
                    </TableCell>
                    <TableCell component="td" align="center">
                        {wine.id_province}
                    </TableCell>
                    <TableCell component="td" align="center">
                        {wine.id_taster}
                    </TableCell>
                    <TableCell component="td" align="center">
                        {wine.id_winery}
                    </TableCell>
                </TableRow>
            ));
        } else {
            return (
                <TableRow>
                    <TableCell colSpan={8}>
                        <CircularProgress />
                    </TableCell>
                </TableRow>
            );
        }
    };

    return (
        <>
            <h1>Wines</h1>

            <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Wine Name</TableCell>
                            <TableCell align="center">Points</TableCell>
                            <TableCell align="center">Price</TableCell>
                            <TableCell align="center">Variety</TableCell>
                            <TableCell align="center">Province ID</TableCell>
                            <TableCell align="center">Taster ID</TableCell>
                            <TableCell align="center">Winery ID</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {renderWines()}
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

export default Wines;
