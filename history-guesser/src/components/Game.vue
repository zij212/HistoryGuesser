<template>
  <div >
    <!-- <h1>{{ title }}</h1> -->
    <div class="container" style="max-width:30%">
        <div class="columns">
            <div class="column is-half">
                <div class="card ">
                    <footer class="card-footer">
                        <p class="card-footer-item">Time: {{time}}</p>
                    </footer>
                </div>
            </div>
            <div class="column">
                <button class="button is-link is-danger"  v-on:click="giveUp">Restart</button>
            </div>
        </div>
    </div>

    <div class="tile is-ancestor" style="position:relative;">
        <div class="tile is-parent">
            <div class="tile is-child box" style="height:22em; width:33em; overflow-y:auto;" id="chatbox">
                <span v-if="!gameOver">
                    <div>
                        <div v-for="message in discussion" :key="message.message" class="rows">
                            <div class="row is-full">
                                <Bubble :name="message.source" :message ="message.message" :url="message.url" :left="message.source == 'AI'" :right="message.source != 'AI'" :time="message.time_ago"/>
                            </div>
                        </div>
                    </div> 
                    <div class="typing-indicator is-pulled-left clear-right" v-show="is_typing">
                    <span></span>
                    <span></span>
                    <span></span>
                    </div>
                </span>
                <span v-else>
                    <div class="content">
                        <h2 v-if="time > 0">Finished!</h2>
                        <h2 v-else>Ran out of time!</h2>
                        <div v-if="correctCentury && correctName && correctCiv">
                            Awesome job!  You got all three correct.
                            <p v-if="scoreTotal != PERFECT_SCORE">You got some missed guesses though, maybe you'll get perfect next time!</p>
                        </div>
                        <div v-else-if="correctCentury || correctName || correctCiv">
                            You got some correct, not bad!
                        </div>
                        <div v-else>
                            Better luck next time!
                        </div >
                        <h2>Solution</h2>
                        <div>
                            <a :href="'https://en.wikipedia.org/wiki/' + answer.names[0]" target="_blank" >
                                <span class="has-text-weight-bold">Name</span>: <p>{{answer.names[0]}}</p>
                            </a>
                        </div>
                        <div>
                            <span class="has-text-weight-bold">Civilization</span>: <p>{{answer.countries[0]}}</p>
                        </div>
                        <div>
                            <span class="has-text-weight-bold">Century</span>: <p>{{answer.century}}</p>
                        </div>
                        <a :href="'https://en.wikipedia.org/wiki/' + answer.names[0]" target="_blank" >
                            <h3>Read more about {{answer.names[0]}}!</h3>
                        </a>
                    </div>
                </span>

            </div>


        </div>

        <div class="tile is-4 is-vertical is-parent">
            <div class="tile is-child box">
            <p class="title">Submit</p>


            <div class="columns">
                <div class="column">
                    <p class="has-text-weight-bold">What century best describes this person?</p>
                    <div :class="{'shake' : animatedCentury}">
                        <Slider :onChange="onSliderChange"  :disabled="disabledCentury"/>
                    </div >
                </div>
                <div class="column is-one-third">
                    <div class="control mt-5">
                        <button v-if="!correctCentury"  :disabled="disabledCentury" class="button is-link "  v-on:click="guessCentury">Guess</button>
                        <button v-else class="button no-pointer is-success"  >Correct</button>

                    </div>
                </div>
            </div>


            <div class="columns">
                <div class="column">

                    <div class="field">
                        <label class="label">What was the person's civilization or nationality?</label>
                        <div class="control">
                            <input :disabled="disabledCiv" id="civInput" class="input" type="text" placeholder="Enter your guess"  :class="{'shake' : animatedCiv}">
                        </div>
                    </div>
                </div>
                <div class="column is-one-third">
                    <div class="control mt-5">
                        <button v-if="!correctCiv" class="button is-link "  :disabled="disabledCiv" v-on:click="guessCiv"  >Guess</button>
                        <button v-else class="button no-pointer is-success"  >Correct</button>
                    </div>
                </div>
            </div>
            <div class="columns">
                <div class="column">

                    <div class="field">
                        <label class="label">What is the person's name?</label>
                        <div class="control">
                            <input :disabled="disabledName" class="input" id="nameInput" type="text" placeholder="Enter your guess"   :class="{'shake' : animatedName}">
                        </div>
                    </div>

                </div>
                <div class="column is-one-third">
                    <div class="control mt-5">
                        <button v-if="!correctName" class="button is-link " :disabled="disabledName" v-on:click="guessName">Guess</button>
                        <button v-else class="button no-pointer is-success"  >Correct</button>
                    </div>
                </div>
            </div>




            </div>
            <div class="tile is-child box">
                <p class="title">Points</p>
                <div class="rows" >
                    <span v-for="score in scores" :key="score.timestamp">

                    <div class="row">
                        <div class="columns" :style="{'color':score.color}">
                            <div class="column">
                                {{score.reason}}
                            </div>
                            <div class="column">
                                {{score.score}}
                            </div>
                        </div>
                    </div>
                    </span>

                    <div class="row">
                        <div class="columns">
                            <div class="column has-text-weight-bold">
                                Total
                            </div>
                            <div class="column">
                                {{scoreTotal}}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

                <!-- <div style="height:100%; position:relative;"> -->

                    <div class="box" style="position:absolute; top:24em; left:.75em; max-width:37em;">
                        <div class="" v-if="!waiting">
                        Ask a question from the random pool:
                        <div v-for="(question, i) in questions" :key="i" class="columns">
                            <div class="hover is-inline" @click="ask(i)">
                                <div class="tile is-parent ">
                                    <article class="tile is-child notification is-light">
                                    <p class="">{{question}}</p>
                                    </article>
                                </div>
                            </div>
                            </div>
                        </div>
                        <div v-else>
                            Waiting for reply...
                        </div>
                    </div>
                <!-- </div> -->
    </div>

<!-- <div class="notification is-link is-light">
  <button class="delete"></button>
  Primar lorem ipsum dolor sit amet, consectetur
  adipiscing elit lorem ipsum dolor. <strong>Pellentesque risus mi</strong>, tempus quis placerat ut, porta nec nulla. Vestibulum rhoncus ac ex sit amet fringilla. Nullam gravida purus diam, et dictum <a>felis venenatis</a> efficitur.
</div> -->

  </div>
</template>


<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import axios from "axios";
// import Bubble from './Bubble'

// let STUB_SCORES = [
//     {"reward": -10, "reason": "Wrong guess"},
//     {"reward": -10, "reason": "Wrong guess"},
//     {"reward": -10, "reason": "Wrong guess"},
//     {"reward": -10, "reason": "Wrong guess"},
//     {"reward": -10, "reason": "Wrong guess"},
//     {"reward": -10, "reason": "Wrong guess"},
//     {"reward": -10, "reason": "Wrong guess"},
//     {"reward": 75, "reason": "Correct century"},
//     {"reward": 50, "reason": "Correct civilization"},
//     {"reward": 225, "reason": "Correct person"},
// ];
// let STUB_QUESTIONS = [
// "What is your favorite food?",
// "What's on the other side of the ocean?",
// "Would you accept a dual?",
// "Did you visit england?",
// "Do you know about gunpowder?",
// "Have you ever been to england?",
// "Do you know how to read the temperature in celsius?",
// "Do you like protestantism?",
// "Where was your biggest victory?",
// "Where was your favorite place to travel to?",
// "What do you do in your spare time?",
// "Who is your favorite king?",
// "Who is your favorite queen?",
// "Do you have any children?",
// "What is your opinion on exploration?",
// "Did you know how to use a sword?",
// "Who is your best ally?",
// "Where did you die?",
// "Do you have a spouse?",
// "Where was your biggest defeat?",
// "What do you think about philosophy?",
// "Do you like Catholicism",
// "Do you like Taoism?",
// "Is the earth flat?",
// "Do you know calculus?",
// ];
function randomChoice(arr: any[]): any {
    return arr[Math.floor(arr.length * Math.random())];
}

class Message{
    source: string
    message: string
    url: string
    date: number
    time_ago: string
    constructor(message:string, source:string) {
        this.source = source;
        this.message = message;
        this.url = "";
        if (this.source.toLowerCase() == "ai") {
            this.url = require('../assets/ai.png');
        }
        this.date = (new Date()).getTime();
        this.time_ago = "now";
    }

    setUrl(url:string):void{
        this.url = url;
    }
}

class Score {
    reason:string;
    score: number;
    timestamp: number;
    color:string;
    constructor(reason:string, score:number){
        this.reason = reason;
        this.score = score;
        this.timestamp = (new Date()).getTime();
        if (this.score < 0) {
            this.color ='red';
        } else {
            this.color ='green';
        }
    }
}

// function stub_server_score(_anser:any, cb:any): void{
//     setTimeout(()=>{
//         var questions: any[] = [];
//         var response = randomChoice(STUB_SCORES);
//         cb(response);
//     },500);
// }

// function stub_server_response(cb:any): void{
//     setTimeout(()=>{
//         var response:any = {};
//         var questions: any[] = [];
//         questions.push(randomChoice(STUB_QUESTIONS));
//         questions.push(randomChoice(STUB_QUESTIONS));
//         questions.push(randomChoice(STUB_QUESTIONS));
//         questions.push(randomChoice(STUB_QUESTIONS));
//         questions.push(randomChoice(STUB_QUESTIONS));
//         response['questions'] = questions;
//         response['reply'] = "I reply " + Math.random();
//         cb(response);
//     },500);
// }

import Slider from '@/components/Slider.vue';
import Bubble from '@/components/Bubble.vue';

@Options({
  props: {
    firstMessage: String,
    onStop: undefined,
    username: String,
  },
  components: {
      Bubble,
      Slider
  }
})
export default class Game extends Vue {
  firstMessage!: string
  username!: string
  time = 120
  is_typing = false
  discussion: Message[] = []
  scores: Score[] = []
  questions: string[] = []
  answer = {}
  scoreTotal = 0
  seed = Math.random()
  waiting = false
  PERFECT_SCORE = 350
  onStop!: ()=>void

  sliderValue = 0

  animatedName = false
  animatedCiv= false
  animatedCentury= false

  disabledName = false
  disabledCiv = false
  disabledCentury = false

  correctName = false
  correctCiv = false
  correctCentury = false

  gameOver = false

  doGameOver(){
    if (!this.gameOver) {

        axios.get('/api/finish').then((response:any) => {
        console.log('/api/finish',response.data);
        this.answer = response.data;
        this.gameOver = true;
        }).catch((e)=>{
        console.log('ERROR /api/finish',e)
        this.gameOver = true;
        })
    }


  }

  mounted(){
      console.log('mounted');
      this.time = 120;
      let interval = setInterval(()=>{
          if (!this.gameOver) {

            this.time = this.time - 1;
            if (this.time == 0) {
                clearInterval(interval);
                this.timesUp();
                this.doGameOver();
            }
          }
      },1000);

      setInterval(()=>{
          let now = (new Date()).getTime();
          for (var i = 0; i < this.discussion.length; i++) {
              let diff = now - this.discussion[i].date;
              if (diff > 10 * 1000) {
                  this.discussion[i].time_ago = "over 10s ago"
              }
              if (diff > 60 * 1000) {
                  this.discussion[i].time_ago = "1 minute ago"
              }
              if (diff > 120 * 1000) {
                  this.discussion[i].time_ago = Math.floor(diff/1000/60) + " minutes ago"
              }
          }

          // also check for end game
          if (this.correctCentury && this.correctName && this.correctCiv) {
              this.doGameOver();
          }
      },1000);

      this.is_typing = true;
      // STUB
    //   stub_server_response(this.onReply);

    axios.post('/api/start/conversation', {'username': this.username}).then((response:any) => {
      console.log('/start/conversation',response.data);
      this.onReply(response.data);
    }).catch((e)=>{
      console.log('ERROR /start/conversation',e)
    })


  }

  giveUp(){
      this.discussion = []
      this.onStop();
  }

  timesUp(){
      console.log("times up!");
  }

  onNewQuestions(questions: string[]): void {
      console.log('new questions', questions);
      var element = document.getElementById("chatbox");
      if (element) element.scrollTop = element.scrollHeight;
      this.questions = questions;
  }

  ask(index: number) {
      console.log('asking', this.questions[index]);

      var msg = new Message(this.questions[index], "You");
      msg.setUrl("https://avatars.dicebear.com/api/human/"+this.seed+".svg");
      this.discussion.push(msg)

      this.waiting = true;
      this.is_typing = true;

      var element = document.getElementById("chatbox");
      if (element) element.scrollTop = element.scrollHeight

    //   stub_server_response(this.onReply);
        axios.post('/api/ask/question', {'question': index}).then((response:any) => {
            console.log('/start/conversation',response.data);
            this.onReply(response.data);
        }).catch((e)=>{
            console.log('ERROR /start/conversation',e)
        })




  }

  onReply(response:any){
      this.onNewQuestions(response.questions);
      this.discussion.push(new Message(response.response, "AI"));
      this.waiting =false;
      this.is_typing = false;
      var element = document.getElementById("chatbox");
      if (element) element.scrollTop = element.scrollHeight;
      setTimeout(()=>{
        var element = document.getElementById("chatbox");
        if (element) element.scrollTop = element.scrollHeight;

      },2);
  }

  onSliderChange(value:number) {
      console.log(value)
      this.sliderValue = value;
  }

  guessCentury() {
      console.log('guessing century')

            this.disabledCentury = true;
        this.submitAnswer({"century":this.sliderValue}, (success)=>{
            if (!success) {

                this.disabledCentury = false;
                console.log('ANIMATE CENTUURY')
                this.animatedCentury = true; setTimeout(() => { this.animatedCentury = false }, 1000);
            }
            this.correctCentury = success;
            console.log(success);
        })

  }
  guessCiv() {
      var input = document.getElementById('civInput');
      if (input) {
        var civ = (input as HTMLInputElement).value;
        console.log('guessing civ', civ)
        if (!civ){
            this.animatedCiv = true; setTimeout(() => { this.animatedCiv = false }, 1000);
        } else {
            this.disabledCiv = true;
            this.submitAnswer({"country":civ}, (success)=>{
                if (!success) {
                    this.disabledCiv = false;
                    this.animatedCiv = true; setTimeout(() => { this.animatedCiv = false }, 1000);
                }
                this.correctCiv= success;
                console.log(success);
            })
        }

      }
  }
  guessName() {
      var input = document.getElementById('nameInput');
      if (input) {
        var name= (input as HTMLInputElement).value;
        if (!name) {
            console.log('no name')
            this.animatedName= true; setTimeout(() => { this.animatedName = false }, 1000);
        } else {
            this.disabledName = true;
            this.submitAnswer({"name":name}, (success)=>{
                if (!success) {
                    this.disabledName = false;
                    this.animatedName= true; setTimeout(() => { this.animatedName = false }, 1000);
                }
                this.correctName= success;
                console.log(success);
            })
        }
        console.log('guessing name', name)
      }

  }

  submitAnswer(answer: any, cb:(success: boolean) => void) {

    axios.post('/api/submit/answer', answer).then((res:any) => {
        console.log("/submit/answer", answer);
          if (res.data.reward < 0) {
            cb(false);
          } else {
            cb(true);
          }
          console.log(res.data);
          this.scores.push(new Score(res.data.reason, res.data.reward));
          var total = 0;
          for (var i = 0; i < this.scores.length; i++) {
              total += this.scores[i].score;
          }
          this.scoreTotal = total;
    }).catch((e)=>{
        console.log('ERROR /submit/answer',e)
    })

   //   })
  }


}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.hover{
cursor: pointer;
}
.hover:hover .is-light {
background-color: #363636;
color: #fff;
}
.no-pointer{
    cursor: default;
}
</style>

