<script>
    import HomeButton from "../HomeButton.svelte";

    async function getChoices() {
        let r = await fetch(
            "https://developer-survey.xfinnbar.repl.co/api/get_choices"
        );
        if (await r.status == 400) {
            // alert("Error");
            console.log({ status: r.status, text: r.text });
            return;
        }
        let retval = await r.json();
        console.log(retval)
        return retval; /*
        {
            "options": Array,
            "question": string
        }
        */
    }

    async function sumbitChoice(choice) {
        /* let url = "https://developer-survey.xfinnbar.repl.co/api/answer?choice=" + encodeURIComponent(choice);
        let r = await fetch(url);
        if (await r.status == 400) {
            alert("Error: " + await r.text())
            console.log()
            return false
        } else {
            main()
            return true
        } */
        location.href = `https://developer-survey.xfinnbar.repl.co/login?next=${encodeURIComponent("https://developer-survey.xfinnbar.repl.co/api/answer?choice=" + choice)}`
    }

    let data = new Promise(() => {});
    async function main() {
        data = await getChoices();
    };

    main()

    /*
    * Chooses an answer and sumbits it.
    * @param {string} i - Index of list, in my case it is zero
    */

    async function choose(i) {
        sumbitChoice(data["options"][i])
    }
</script>

<!-- routify:options index=-1 -->
<HomeButton />
<main>
    {#await data}
        Loading...
    {:then newdata}
        {#if data.has_answered}
            ⚠ You've already answered!
        {/if}
        <h1 data-aos="fade-up" data-aos-duration="500" >{newdata["question"]}</h1>
        <div class="buttons">
            {#each newdata["options"] as option, i}
                <button 
                data-aos="fade-up"
                data-aos-delay="{i * 2}00"
                data-aos-duration="500"
                on:click={() => {
                    choose(i)
                }}
                >{option}</button>
            {/each}
        </div>
    {/await}
</main>

<style>

    .buttons {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }

    main {
        text-align: center;
    }
    button {
        width: 500px;
        max-width: 90vw;
    }
</style>