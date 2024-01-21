import Countries from "../Tables/Countries";
import Provinces from "../Tables/Provinces";
import Wines from "../Tables/Wines";
import Wineries from "../Tables/Wineries";
import Tasters from "../Tables/Tasters";

const Sections = [

    {
        id: "countries",
        label: "Countries",
        content: <Countries/>
    },

    {
        id: "provinces",
        label: "Provinces",
        content: <Provinces/>
    },

    {
        id: "wines",
        label: "Wines",
        content: <Wines/>
    },

    {
        id: "wineries",
        label: "Wineries",
        content: <Wineries/>
    },

    {
        id: "tasters",
        label: "Tasters",
        content: <Tasters/>
    }

];

export default Sections;