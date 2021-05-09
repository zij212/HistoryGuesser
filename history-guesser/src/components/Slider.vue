<template>
  <vue-slider :disabled="disabled" v-model="value" min="-800" max="1900" interval="100"/>
</template>
 
<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/antd.css'

//  @Options({
//   props: {
//   },
//   components: {
//       Bubble,
//       Slider
//   }
// })
@Options({
  props: {
    onChange: undefined,
    disabled: false,
  },
  components: {
      VueSlider
  },
  watch: {
      value: function(newValue:any){
          console.log(this.onChange)
          if (this.onChange) this.onChange(newValue)
      }
  }
})
export default class Slider extends Vue {
  onChange!:(newValue:any) => void
  disabled!: boolean
  data () {
    return {
      value: 0
    }
  }


}
</script>