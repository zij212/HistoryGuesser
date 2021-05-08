<template>
    <container>
  <div v-if="!playing">
    <div v-if="!loading">
      History Guesser is an game where you are matched with
      a random person from history and you need to figure out
      who they are!
    </div>
    <div v-else>
      Matching you with a random figure from history...
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
    <Game firstMessage="My name is ________.  What questions can I answer for you?" />
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
  clickStart() {
    console.log("start");
    this.loading = true;
    setTimeout(()=>{
      this.playing = true;
      this.loading = false;
    },300);
  }
}
</script>
