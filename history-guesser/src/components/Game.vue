<template>
  <div >
    <!-- <h1>{{ title }}</h1> -->
    <div class="container" style="max-width:20%">
        <div class="columns">
            <div class="column"></div>
            <div class="column is-half">
                <div class="card ">
                    <footer class="card-footer">
                        <p class="card-footer-item">Time</p>
                        <p class="card-footer-item">{{time}}</p>
                    </footer>
                </div>
            </div>
            <div class="column"></div>
        </div>
    </div>

    <div class="tile is-ancestor">
        <div class="tile is-parent">
            <div class="tile is-child box">
                <div class="typing-indicator" v-show="is_typing">
                <span></span>
                <span></span>
                <span></span>
                </div>
               <ul id="example-1">
                    <div v-for="message in discussion" :key="message.message">
                        <div>

                            <Bubble :name="message.source" :message ="message.message" :url="message.url"/>
                        </div>
                    </div>
                </ul> 
            </div>
        </div>

        <div class="tile is-4 is-vertical is-parent">
            <div class="tile is-child box">
            <p class="title">Submit</p>
            <p>Century</p>
            <p>Civilization</p>
            <p>Name</p>
            </div>
            <div class="tile is-child box">
            <p class="title">Points</p>
            <p>0</p>
            </div>
        </div>
    </div>

  </div>
</template>


<script lang="ts">
import { Options, Vue } from 'vue-class-component';
// import Bubble from './Bubble'

let STUB_QUESTIONS = [
"What is your favorite food?",
"What's on the other side of the ocean?",
"Would you accept a dual?",
"Did you visit england?",
"Do you know about gunpowder?",
"Have you ever been to england?",
"Do you know how to read the temperature in celsius?",
"Do you like protestantism?",
"Where was your biggest victory?",
"Where was your favorite place to travel to?",
"What do you do in your spare time?",
"Who is your favorite king?",
"Who is your favorite queen?",
"Do you have any children?",
"What is your opinion on exploration?",
"Did you know how to use a sword?",
"Who is your best ally?",
"Where did you die?",
"Do you have a spouse?",
"Where was your biggest defeat?",
"What do you think about philosophy?",
"Do you like Catholicism",
"Do you like Taoism?",
"Is the earth flat?",
"Do you know calculus?",
];
function randomChoice(arr: any[]): any {
    return arr[Math.floor(arr.length * Math.random())];
}

class Message{
    source: string
    message: string
    constructor(message:string, source:string) {
        this.source = source;
        this.message = message;
    }
}

import Bubble from '@/components/Bubble.vue';
@Options({
  props: {
    firstMessage: String
  },
  components: {
      Bubble,
  }
})
export default class Game extends Vue {
  firstMessage!: string
  time = 60
  is_typing = false
  discussion: Message[] = []
  mounted(){
      console.log('mounted');
      this.time = 60;
      let interval = setInterval(()=>{
          this.time = this.time - 1;
          if (this.time == 0) {
              clearInterval(interval);
              this.timesUp();
          }
      },1000);

      // STUB
      this.is_typing = true;
      setTimeout(()=>{
          this.is_typing = false;
          this.discussion.push(
              new Message(this.firstMessage, "AI")
          )
          var questions: string[] = [];
          questions.push(randomChoice(STUB_QUESTIONS));
          questions.push(randomChoice(STUB_QUESTIONS));
          questions.push(randomChoice(STUB_QUESTIONS));
          questions.push(randomChoice(STUB_QUESTIONS));
          questions.push(randomChoice(STUB_QUESTIONS));
          this.onNewQuestions(questions);
      },400)
  }

  timesUp(){
      console.log("times up!");
  }

  onNewQuestions(questions: string[]): void {
      console.log('new questions', questions);
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
</style>

