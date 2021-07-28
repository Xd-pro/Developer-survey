<script>
import HomeButton from "../HomeButton.svelte";


    let prod = true;

    let getData;

    if (prod) {
        getData = async () => {
            let r = await fetch("https://developer-survey.xfinnbar.repl.co/api/get_answers")
            return await r.json()
        };
        // fetch data
    } else {
        // dummy data
        getData = async () => {
            return {
                Python: 10,
                NodeJS: 7,
                Ruby: 3,
                Total: 20,
            };
        };
    }

    let data = getData().then((data) => {
        var chartData = [
            {
                x: Object.keys(data),
                y: Object.values(data),
                type: "bar",
            },
        ];

        Plotly.newPlot("graph", chartData, {
            paper_bgcolor: "rgb(61, 66, 71)",
            plot_bgcolor: "rgb(61, 66, 71)",
            font: {
                family: "Courier New, monospace",
                size: 18,
                color: "white",
            },
        });
    });
</script>

<!-- routify:options index=1 -->
<HomeButton></HomeButton>
<main>
    <h1>Results</h1>
    <div id="graph" />
</main>

<style>
    #graph {
        width: 1300px;
        margin: auto;
        max-width: 100%;
    }

    h1 {
        text-align: center;
        margin: 0;
    }

    
</style>
