<template>
  <div >
    <div class='quote'>
    <img class='round-avatar' src='{{url}}'>
    <div class='speech-bubble left'>
        <p>
        {{name}}
        <span class='time-ago'>
            {{time}}
        </span>
        </p>
        <blockquote>
            {{message}}
        </blockquote>
    </div>
    </div>
  </div>

</template>


<script lang="ts">
import { Options, Vue } from 'vue-class-component';

@Options({
  props: {
    message: String,
    name: String,
    time: Date,
    url: String,
  }
})
export default class Bubble extends Vue {
  message!: string
  name!: string
  time!: Date
  url!:string
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>

