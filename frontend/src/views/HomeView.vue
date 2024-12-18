<template>
  <div class="home">
    <div class="controls">
      <ParserView v-show="currentStage === 'parser'" />
      <FileUploader v-show="currentStage === 'uploader'" />
      <ModelSelector v-show="currentStage === 'uploader'" />
      <ChartDisplay v-show="currentStage === 'train'" />
      <LogOutput v-show="currentStage === 'train'" />
    </div>
    <div class="navigation">
      <button
        v-for="(index) in menuList"
        :key="index"
        :class="{'nav-button':true, active: activeIndex === index }"
        @click="setActive(index)"
      ></button>
    </div>
  </div>
</template>

<script>
import '@/assets/home/home.css'
import '@/assets/navigation.css'

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
      activeIndex: 0,
      currentStage: "uploader",
      menuList: ["parser", "namer", "uploader", "selector"],
      inputOffset: "",
      inputCount: "",
    };
  },
  methods: {
    setActive(index) {
      this.activeIndex = index;
      this.currentStage = this.menuList[index];
    }
  }
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