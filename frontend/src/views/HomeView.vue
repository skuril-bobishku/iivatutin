<template>
  <div class="home">
    <div>
      <ParserView v-show="currentStage === 'parser'" />
      <FileUploader v-show="currentStage === 'uploader'" />
      <ModelSelector v-show="currentStage === 'uploader'" />
      <ChartDisplay v-show="currentStage === 'train'" />
      <LogOutput v-show="currentStage === 'train'" />
    </div>
    <div class="navigation">
      <button></button>
    </div>
  </div>

</template>

<script>
import '@/assets/home/home.css'

import FileUploader from "../components/FileUploader.vue";
import ModelSelector from "../components/ModelSelector.vue";
import ChartDisplay from "../components/ChartDisplay.vue";
import LogOutput from "../components/LogOutput.vue";
import ParserView from "@/views/ParserView.vue";

export default {
  name: "HomeView",
  components: {
    ParserView,
    FileUploader,
    ModelSelector,
    ChartDisplay,
    LogOutput,
  },
  data() {
    return {
      currentStage: "uploader",
      inputOffset: "",
      inputCount: "",
      items: [],
    };
  },
};
</script>

<!--
<script setup lang="ts">
import { Ref, ref } from 'vue'
import FileUploader from "../components/FileUploader.vue";
import ModelSelector from "../components/ModelSelector.vue";
import ChartDisplay from "../components/ChartDisplay.vue";
import LogOutput from "../components/LogOutput.vue";

const currentStage: Ref<'main' | 'uploaded'>  = ref('main')
</script>-->