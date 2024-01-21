import TopTeams from "../Procedures/TopTeams";
import TopWineries from "../Procedures/TopWineries";
import WinesByCountry from "../Procedures/WinesByCountry";

const Sections = [

    {
        id: "top-teams",
        label: "Top Teams",
        content: <TopTeams/>
    },

    {
        id: "top-scorers",
        label: "Top Scorers",
        content: <h1>Top Scorers - Work in progresss</h1>
    },

    {
        id: "top_wineries",
        label: "Top Wineries",
        content: <TopWineries/>
    },

    {
        id: "wines_country",
        label: "Wines By Country",
        content: <WinesByCountry/>
    }

];

export default Sections;