<template>
  <div class="highscores">
      <div class="rows">
        <div class="row">
            <div class="columns">
                <div class="column has-text-weight-bold">
                  Username
                </div>
                <div class="column has-text-weight-bold">
                  Historical Figure
                </div>
                <div class="column has-text-weight-bold">
                  Score
                </div>

            </div>
        </div>


        
        <span v-for="score in scores" :key="score.username">
        <div class="row">
            <div class="columns">
                <div class="column">
                    {{score.username}}
                </div>
                <div class="column">
                    {{score.topic}}
                </div>
                <div class="column">
                    {{score.score}}
                </div>

            </div>
        </div>

        </span>
      </div>



  </div>
</template>

<script lang="ts">
import { Vue } from 'vue-class-component';
import axios from "axios";

export default class Highscores extends Vue {
  //http://localhost:5000/highscores
  scores:any[] = [];
  mounted(){
    console.log('mounted');
    axios.get('/api/highscore', ).then((response:any) => {
      console.log('/api/highscore',response.data);
      this.scores = response.data.scores;
    }).catch((e)=>{
      console.log('ERROR /api/highscore',e)
    })


  }



}
</script>

