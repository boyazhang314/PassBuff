<template>
    <div class="passbuff-container" v-bind:class="{
        'weak-container':(this.$store.state.score < 4 && this.$store.state.score >= 1),
        'med-container':(this.$store.state.score === 4 || this.$store.state.score === 5),
        'strong-container':(this.$store.state.score >= 6)
    }" >
        <h1 class="passbuff-title" v-if="!text">P@s$8ufF</h1>
        <div class="title-message">
            <h2 class="passbuff-subtitle" v-if="this.$store.state.score === 1">Password is Really Weak</h2>
            <h2 class="passbuff-subtitle" v-else-if="this.$store.state.score === 2 || this.$store.state.score === 3">Password is Weak</h2>
            <h2 class="passbuff-subtitle" v-else-if="this.$store.state.score === 4 || this.$store.state.score === 5">Password is Ok</h2>
            <h2 class="passbuff-subtitle" v-else-if="this.$store.state.score === 6">Password is Buff</h2>
            <h2 class="passbuff-subtitle bounce" v-else-if="this.$store.state.score === 7">Password is Really Buff!</h2>
            <h2 class="passbuff-subtitle" v-else>Enter a Password to Buff</h2>
            
            <div class="emoticon" v-if="this.$store.state.score === 1">（ー△ー；）</div> 
            <div class="emoticon" v-else-if="this.$store.state.score === 2">ᕙ(⇀‸↼‶)</div>
            <div class="emoticon" v-else-if="this.$store.state.score === 3">ᕦ(ò_óˇ)</div>   
            <div class="emoticon" v-else-if="this.$store.state.score === 4">୧( ˵ ° ~ ° ˵ )୨</div>
            <div class="emoticon" v-else-if="this.$store.state.score === 5">ᕙ(⊙‸⊙)ᕗ</div>
            <div class="emoticon" v-else-if="this.$store.state.score === 6">ᕦ⊙෴⊙ᕤ</div>
            <div class="emoticon bounce" v-else-if="this.$store.state.score === 7">ᕦ༼ ˵ ◯ ਊ ◯ ˵ ༽ᕤ</div>
            <div class="emoticon" v-else>(・∀・)</div>
        </div>
        <div class="score bounce" :key="this.$store.state.score" v-if="this.$store.state.score >= 1">
            Power Level: {{ this.$store.state.score }}
        </div>
        <button class="hint-button" v-if="this.$store.state.password" @click="hints()">Hints</button>
        <div class="input-container" v-bind:class="{
            'weak-input':(this.$store.state.score < 4 && this.$store.state.score >= 1),
            'med-input':(this.$store.state.score === 4 || this.$store.state.score === 5),
            'strong-input':(this.$store.state.score >= 6)
        }">
            <div class="input-bar">
                <div class="input-button left">
                    <button class="button" id="undo-button" @click="undo()" @mouseover="undoMsg='CTRL Z'" @mouseleave="undoMsg='Undo'">{{ undoMsg }}</button>
                </div>
                <input class="password-input" spellcheck="false" v-model="text" v-if="show" />
                <input class="password-input" spellcheck="false" v-model="text" v-if="!show" type="password" />
                <div class="input-button right">
                    <button class="button" id="copy-button" @click="copy()" @mouseover="copyMsg='CTRL C'" @mouseleave="copyMsg='Copy'">{{ copyMsg }}</button>
                </div>
            </div>
            <button class="show-hide-button" v-if="!show" @click="showhide()">Show</button>
            <button class="show-hide-button" v-if="show" @click="showhide()">Hide</button>
        </div>
    </div>
    <div class="bottom-container" v-bind:class="{
            'weak-bottom':(this.$store.state.score < 4 && this.$store.state.score >= 1),
            'med-bottom':(this.$store.state.score === 4 || this.$store.state.score === 5),
            'strong-bottom':(this.$store.state.score >= 6)
        }">
        <!-- Display 3 buffs at a time -->
        <div class="buff-box">
            <div class="buff" tabindex="1" v-if="this.$store.state.buffs && this.$store.state.buffs[0] && this.$store.state.password" 
                        v-on:click="buffClick(this.$store.state.buffs[0][1])">
                <div class="buff-name">{{ this.$store.state.buffs[0][0] }}</div>
                <div class="buff-string" v-if="show">{{ this.$store.state.buffs[0][1] }}</div>
                <div class="buff-amount">+{{ this.$store.state.buffs[0][2] }}</div>
            </div>
            <div class="buff" tabindex="2" v-if="this.$store.state.buffs && this.$store.state.buffs[1] && this.$store.state.password" 
                        v-on:click="buffClick(this.$store.state.buffs[1][1])">
                <div class="buff-name">{{ this.$store.state.buffs[1][0] }}</div>
                <div class="buff-string" v-if="show">{{ this.$store.state.buffs[1][1] }}</div>
                <div class="buff-amount">+{{ this.$store.state.buffs[1][2] }}</div>
            </div>
            <div class="buff" tabindex="3" v-if="this.$store.state.buffs && this.$store.state.buffs[2] && this.$store.state.password" 
                        v-on:click="buffClick(this.$store.state.buffs[2][1])">
                <div class="buff-name">{{ this.$store.state.buffs[2][0] }}</div>
                <div class="buff-string" v-if="show">{{ this.$store.state.buffs[2][1] }}</div>
                <div class="buff-amount">+{{ this.$store.state.buffs[2][2] }}</div>
            </div>
        </div>
        <button class="reroll-button" v-if="this.$store.state.buffs[0] && this.$store.state.password" @click="getPassword()">
            Reroll
            <div class="icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-repeat" viewBox="0 0 16 16">
                    <path d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z"/>
                    <path fill-rule="evenodd" d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z"/>
                </svg>
            </div> 
        </button>
        <button class="restart-button" v-if="this.$store.state.score === 7" @click="restart()">Restart</button>
        <!-- <p>{{ this.$store.state.password }}</p>
        <p>{{ this.$store.state.score }}</p>
        <p>{{ this.$store.state.buffs }}</p>
        <p>{{ this.$store.state.previous }}</p> -->
        <!-- <p>{{ msg }}</p> -->
    </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
    data() {
        return {
            msg: "",
            undoMsg: "Undo",
            copyMsg: "Copy",
            show: false
        }
    },
    computed: {
        text: {
            get() {
                return this.$store.state.password
            },
            set(value) {
                this.$store.commit("changePassword", value)
                if (value.length === 0) {
                    this.$store.commit("changeScore", 0)
                }
            }
        }
    },
    methods: {
        getPassword() {
            const path = "http://localhost:5000/power"
            axios.get(path)
                .then(async (res) => {
                    this.msg = await res.data["power"]
                    const score = await res.data["power"]["score"]
                    const buffs = await res.data["power"]["buffs"]
                    const advice = await res.data["power"]["advice"]
                    this.$store.commit("changeScore", score + 1)
                    this.$store.commit("changeBuffs", buffs)
                    this.$store.commit("changeAdvice", advice)
                })
                .catch((err) => {
                    console.error(err);
                })
        },
        postPassword(pw) {
        const path = "http://localhost:5000/power"
        axios.post(path, pw)
            .then(() => {
                this.getPassword()
            })
            .catch((err) => {
                console.error(err)
            })
        },
        buffClick(pw) {
            this.$store.commit("pushPrevious", this.text)
            this.text=pw
        },
        undo() {
            if (this.$store.state.previous.length > 0) {
                this.text = this.$store.state.previous.at(-1)
                this.$store.commit("popPrevious")
            } else {
                this.text = "";
                this.$store.commit("changeScore", 0)
                this.$store.commit("changeBuffs", [])
            }
        },
        copy() {
            navigator.clipboard.writeText(this.text)
        },
        restart() {
            window.location.reload()
        },
        showhide() {
            this.show = !this.show
        },
        hints() {
            var html = ""
            for (let i = 0; i < this.$store.state.advice.length; i++) {
                html += this.$store.state.advice[i] + "<br><br>"
            }
            if (this.$store.state.advice.length > 0) {
                Swal.fire({
                    icon: 'info',
                    title: 'Hints',
                    height: 'fit-content',
                    width: '50vw',
                    html: html,
                    okButtonColor: '#3085d6'
                })
            } else {
                Swal.fire({
                    icon: 'success',
                    title: 'Hints',
                    text: 'Looking good!'
                })
            }
        }
    },
    watch: {
        text: async function() {
            await this.postPassword({"password": this.$store.state.password})
        }
    },
    created() {
        let keyPressed = {}
        var ref = this
        window.addEventListener('keydown', function (e) {
            keyPressed[e.key] = true
            if ((keyPressed['Control'] && e.key == 'z') || (keyPressed['z'] && e.key == 'Control')) {
                document.getElementById("undo-button").style.backgroundColor = "#005e46";
                ref.undo()
            } else if ((keyPressed['Control'] && e.key == 'c') || (keyPressed['c'] && e.key == 'Control')) {
                document.getElementById("copy-button").style.backgroundColor = "#005e46";
                ref.copy()
            }
        })
        window.addEventListener('keyup', function (e) {
            keyPressed[e.key] = false
            document.getElementById("undo-button").style.backgroundColor = "";
            document.getElementById("copy-button").style.backgroundColor = "";
        })
    }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@800&display=swap');

.passbuff-container {
    height: fit-content;
    width: auto;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.weak-container {
    background: linear-gradient(.25turn, #d83e33, #f09663); 
}
.med-container {
    background: linear-gradient(.25turn, #ffa600, #ffd000); 
}
.strong-container {
    background: linear-gradient(.25turn, #03ee16, #33caa4); 
}

.passbuff-title {
    font-size: 13vh;
    font-style: bold;
    font-family: 'Rubik', sans-serif;

    background-image: linear-gradient(to left top, #202283, #0082ce); 
    background-size: 100%;
    background-clip: text;

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent; 
    -moz-background-clip: text;
    -moz-text-fill-color: transparent;

    user-select: none;
    margin-bottom: 0;

    -webkit-text-stroke: 1px rgb(8, 0, 53);
}
.weak-title {
    background-image: linear-gradient(.25turn, #920123, #ff033e); 
    -webkit-text-stroke: 1px rgb(53, 0, 0);
}
.med-title {
    background-image: linear-gradient(.25turn, #c97800, #ffce2d); 
    -webkit-text-stroke: 1px rgb(88, 65, 0);
}
.strong-title {
    background-image: linear-gradient(.25turn, #008f3b, #3eff7e); 
    -webkit-text-stroke: 1px rgb(4, 53, 0);
}

.title-message {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    height: 20vh;
    margin: 2%;
}

.score {
    font-size: 3vh;
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    color: white;
    user-select: none;
    margin: 1%;
    transform: .35s ease-in-out;
}

.emoticon {
    font-family: "Rubik", sans-serif;
    font-size: 3vh;
    color: white;
    user-select: none;
}

.passbuff-subtitle {
    font-size: 5vh;
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    color: white;
    user-select: none;
}

.hint-button {
    font-size: 3vh;
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    color: white;
    user-select: none;

    background: #00a6ff;

    margin-bottom: 0.5%;
    padding-left: 2vh;
    padding-right: 2vh;

    border: none;
    border-radius: 10vh;

    cursor: pointer;
}
.hint-button:hover {
    background: #165cbc;
}

.input-container {
    width: 100vw;
    height: 30vh;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    background: linear-gradient(.25turn, #003cbe, #339aca); 
}
.weak-input {
    background: linear-gradient(.25turn, #88070d, #ff2732); 
}
.med-input {
    background: linear-gradient(.25turn, #dd6503, #ffb84d); 
}
.strong-input {
    background: linear-gradient(.25turn, #008b23, #45ff2c); 
}

.show-hide-button {
    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 2vh;
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    color: rgb(255, 255, 255);
    cursor: pointer;

    border: none;
    background: none;
    margin-top: 1%;
}

.show-hide-button:hover {
    color: rgb(191, 250, 255);
}

.input-bar {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;

    margin-top: 2%;
}

.input-button {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.button {
    display: flex;
    justify-content: center;
    align-items: center;

    height: 10vh;
    width: 12vw;
    font-size: 3vh;
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    color: rgb(255, 255, 255);
    cursor: pointer;

    border: none;
    border-radius: 10vh;
    background-color: #1dd4a7;

    padding: 3vh;
    padding-left: 7vh;
    padding-right: 7vh;   

    z-index: 2;
    user-select: none;
}
.left {
    margin-right: -14%;
}
.right {
    margin-left: -14%;
}
.button:hover {
    background-color: #005e46;
}

.password-input {
    text-align: center;
    
    border: none;
    height: 7vh;
    width: 130vh;

    border-radius: 10vh;

    font-size: 5vh;
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');

    padding: 3vh;
    padding-left: 7vh;
    padding-right: 7vh;   
}

.bottom-container {
    height: 100%;
    width: 100%;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    background: linear-gradient(.25turn, #0062be, #64cee9);
}
.weak-bottom {
    background: linear-gradient(.25turn, #9e1e15, #ee7d3c); 
}
.med-bottom {
    background: linear-gradient(.25turn, #cf7602, #e4b415); 
}
.strong-bottom {
    background: linear-gradient(.25turn, #0bbb1a, #1dd4a7); 
}

.icon {
    margin-left: 10%;
}

.reroll-button {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;

    margin-top: 3%;
    padding-left: 3vh;
    padding-right: 3vh;

    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    font-size: 3vh;

    border: none;
    border-radius: 2vh;

    color: white;
    background-color: #3064d6; 

    cursor: pointer;
    user-select: none;
}
.reroll-button:hover {
    background-color: #042979; 
}

.buff-box {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.buff {
    color: white;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    padding: 1vh;
    margin-left: 5vh;
    margin-right: 5vh;
    width: 25vw;

    border-radius: 3vh;

    background-color: #28cc2d; 
    box-shadow: inset 0px 0px 18px 0px rgba(208, 255, 208, 0.75);

    cursor: pointer;
    user-select: none;
    transition: 200ms ease-out;
}
.buff-name {
    font-family: 'Rubik', sans-serif;
    font-size: 3vh;
}
.buff-string {
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    font-size: 3vh;
}
.buff-amount {
    font-family: url('https://fonts.googleapis.com/css2?family=Rubik:wght@500&display=swap');
    font-size: 4vh;
}
.buff:hover {
    transform: scale(1.2);
}
.buff:active {
    background-color: #007745; 
    box-shadow: inset 0px 0px 18px 0px rgba(0, 44, 0, 0.75);
}

.bounce {
  animation: bounce-in 0.5s;
}
@keyframes bounce-in {
    0% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.25);
    }
    100% {
        transform: scale(1);
    }
}

.restart-button {
    display: flex;
    justify-content: center;
    align-items: center;

    height: 10vh;
    padding: 5vh;
    font-size: 5vh;
    font-family: 'Rubik', sans-serif;
    color: rgb(255, 255, 255);
    cursor: pointer;

    border: none;
    border-radius: 2vh;
    background: rgb(0, 145, 202);

    user-select: none;
}
.restart-button:hover {
    background: rgb(3, 39, 117);
}
</style>