<template>
    <container>
  <div v-if="!playing">
    <div v-if="!loading">
      History Guesser is an game where you are matched with
      a random person from history and you need to figure out
      who they are!
      <div>
        <span class="has-text-weight-bold has-text-danger">Warning</span>: This is powered by AI.  Some answers will be off, but most will be accurate.
      </div>
    </div>

    <div v-else>
      Matching you with a random figure from history...
    </div>
    <div class="field">
        <label class="label">Your name:</label>
        <div class="control">
            <input style="max-width:20em;" id="usernameInput" class="input" type="text" placeholder="Enter your username"  :class="{'shake' : animatedUsername}">
        </div>
    </div>

    <button 
      v-if="!loading"
      v-on:click="clickStart()" 
      class="button is-info">Start!</button>
    <button 
      v-else
      class="button is-info is-loading"
      >Loading</button>
  </div>
  <div v-else>
    <Game firstMessage="My name is ________.  What questions can I answer for you?" :onStop="clickStop" :username="username"/>
  </div>
  </container>
</template>

<style scoped>
button.button{
  padding: 2em;
  font-weight: bold;
}
</style>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import HelloWorld from '@/components/HelloWorld.vue';
import Game from '@/components/Game.vue';
import Bubble from '@/components/Bubble.vue';
import axios from "axios";

@Options({
  components: {
    HelloWorld,
    Game,
    Bubble,
  },
})
export default class Home extends Vue {
  message = "Hello!"
  playing = false
  loading = false
  animatedUsername = false
  username = "Human"
  clickStart() {
    console.log("start");
      var input = document.getElementById('usernameInput');
      if (input) {
        var name= (input as HTMLInputElement).value
        if (!name) {
          this.animatedUsername= true; setTimeout(() => { this.animatedUsername= false }, 1000);
          console.log('no username!');
          return;
        }
        this.username = name;
      }

    this.loading = true;
    setTimeout(()=>{
    // axios.post('/start/conversation', {'username': 'Human'}).then((response:any) => {
      this.playing = true;
      this.loading = false;
    // }).catch((e)=>{
      // console.log('ERROR /start/conversation',e)
    // })
    },200);
  }
  clickStop() {

      this.loading = false;
      this.playing= false;
  }
}
</script>
