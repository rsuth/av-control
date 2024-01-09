<!-- AVRemote.svelte -->

<script>
    import SettingsIcon from "./SettingsIcon.svelte";
    import Settings from "./Settings.svelte";

    let showSettingsModal = false;
    let projector_ip = "";
    let switcher_ip = "";
    let switcher_2_ip = "";

    let inputs = [
        {
            name: "Plaintiff",
            value: 1,
        },
        {
            name: "ELMO",
            value: 2,
        },
        {
            name: "Defense",
            value: 3,
        },
        {
            name: "HDMI 4",
            value: 4,
        },
    ];
    let selectedInput = inputs[0];
    let videoMuted = false;

    function debounce_leading(func, timeout = 500) {
        let timer;
        return (...args) => {
            if (!timer) {
                func.apply(this, args);
            }
            clearTimeout(timer);
            timer = setTimeout(() => {
                timer = undefined;
            }, timeout);
        };
    }

    function toggleVideoMute() {
        let command = videoMuted ? "blankoff" : "blankon";
        videoMuted = !videoMuted;
        fetch("/c/" + command)
            .then((res) => {
                console.log(res);
            })
            .catch((err) => {
                console.log(err);
            });
    }

    function switchInputs(input) {
        console.log(input);
        selectedInput = input;

        fetch("/c/v" + input.value)
            .then((res) => {
                console.log(res);
            })
            .catch((err) => {
                console.log(err);
            });
    }

    function getInfo() {
        fetch("/c/info")
            .then((res) => {
                return res.json();
            })
            .then((data) => {
                projector_ip = data.projector_ip;
                switcher_ip = data.switcher_ip;
                switcher_2_ip = data.switcher_2_ip;
            })
            .catch((err) => {
                console.log(err);
            });
    }

    getInfo();
</script>

<div class="remote-container">
    <Settings bind:showSettingsModal>
        <h2 slot="header">Settings</h2>
        <h3>Input Labels:</h3>
        {#each inputs as input}
            <div>
                <label>
                    {input.value}:
                    <input type="text" name="input" bind:value={input.name} />
                </label>
            </div>
        {/each}
        <h4>Network Info</h4>
        <div>
            <p>
                Switcher IP Address: {switcher_ip}
            </p>
            <p>
                Projector IP Address: {projector_ip}
            </p>
            <p>
                Switcher 2 IP Address: {switcher_2_ip}
            </p>
        </div>
    </Settings>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
        class="icon-container"
        on:click={() => {
            showSettingsModal = true;
        }}
    >
        <SettingsIcon size={30} />
    </div>
    <div class="logo">
        <img src="logo.png" alt="logo" height="125px" />
    </div>

    <div class="remote">
        <div class="inputs-section">
            {#each inputs as input}
                <button
                    class="button {selectedInput === input ? 'active' : ''}"
                    on:click={debounce_leading(() => {
                        switchInputs(input);
                    })}
                >
                    {input.name}
                </button>
            {/each}
        </div>

        <div class="control-section">
            <button
                class="show-btn button {!videoMuted ? 'show-active' : ''}"
                on:click={debounce_leading(() => toggleVideoMute())}
            >
                {#if videoMuted}
                    <img src="hide.png" height="50px" alt="hide icon" /><br />
                {:else}
                    <img src="show.png" height="50px" alt="show icon" /><br />
                {/if}
                {videoMuted ? "Projector Blanked" : "Projector On"}
            </button>
        </div>
    </div>
</div>

<style>
    .icon-container {
        position: absolute;
        top: 0;
        right: 0;
        padding: 1em;
        color: #999;
    }
    .remote-container {
        padding: 1.5em;
        background-color: rgb(246, 246, 246);
        border-radius: 12px;
        width: 90vw;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: relative;
    }
    .logo {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 25px;
    }

    .remote {
        display: grid;
        grid-template-rows: auto auto;
        gap: 1rem;
        width: 100%;
    }

    .inputs-section {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.5rem;
    }

    .control-section {
        display: grid;
        grid-template-columns: repeat(1, 1fr);
        gap: 0.5rem;
        justify-items: center;
        align-items: center;
    }

    .button {
        padding: 1.5rem;
        height: 180px;
        font-size: 2rem;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.3s;
        background-color: #f5fbff;
        border: 1px solid rgb(191, 191, 191);
        color: black;
        box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 0px;
    }

    .button:hover {
        box-shadow: 0px 7px 20px rgba(0, 0, 0, 0.15);
    }

    .button.active {
        background-color: #f9ecae; /* Clearly indicate active button */
        box-shadow: inset 0px 4px 20px rgba(0, 0, 0, 0.1); /* Inset shadow for active state */
    }

    .show-btn.show-active {
        background-color: #93e393; /* Clearly indicate active button */
        box-shadow: inset 0px 4px 20px rgba(0, 0, 0, 0.2); /* Inset shadow for active state */
    }

    .show-btn {
        background-color: #f3c3c3;
        color: Black;
        width: 100%;
    }
</style>
