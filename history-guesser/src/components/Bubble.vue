<template>
  <!-- <div style="width:100%;"> -->
    <div v-bind:class="{
        'is-pulled-left': left, 
        'is-pulled-right':right,
        'clear-left': right,
        'clear-right': left,
        }" class="pt-1" >
        <div class='quote is-inline'>
        <img v-show="left" class='round-avatar' :src="url">
        <span class='speech-bubble is-pulled-left' v-bind:class="{'left': left, 'right':!left}">
            <p>
            <!-- {{name}} -->
            </p>
            <blockquote>
                {{message}}
            </blockquote>
            <span class='time-ago is-pulled-right is-size-7'>
                {{time}}
            </span>
        </span>
        <img v-show="!left" class='round-avatar is-pulled-right' :src="url">
        </div>
    </div>
  <!-- </div> -->
</template>


<script lang="ts">
import { Options, Vue } from 'vue-class-component';

@Options({
  props: {
    message: String,
    name: String,
    time: String,
    url: String,
    left: Boolean,
    right: Boolean,
  }
})
export default class Bubble extends Vue {
  message!: string
  name!: string
  time!: string
  url!:string
  left!:boolean
  right!:boolean
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
img {
  max-width: 2em;
}

</style>

