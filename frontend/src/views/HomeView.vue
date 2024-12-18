<template>
  <div class="home">
    <div class="content">
      <ParserPhoto v-show="currentStage === 'parser'"
                   @nextPage="nextPage" />
      <ProjectNamer v-show="currentStage === 'namer'"
                    :pName="projectName"
                    @nextPage="nextPage" />
      <FileUploader v-show="currentStage === 'uploader'"
                    :pName="projectName"
                    :fPath="filePath"
                    @nextPageTrain="nextPageTrain"/>
      <ModelSelector v-show="currentStage === 'selector'" />
      <!--<ChartDisplay v-show="currentStage === 'train'" />
      <LogOutput v-show="currentStage === 'train'" />-->
    </div>
    <div class="navigation">
      <button
        v-for="(stage, index) in menuList"
        :key="index"
        :class="{ 'nav-button': true, active: activeIndex >= index }"
        @click="setActive(index)"
      ></button>
    </div>
  </div>
</template>

<script>
import '@/assets/home/home.css'
import '@/assets/home/content-view.css';
import '@/assets/home/navigation-bar.css'

import '@/assets/home/input-text.css'
import '@/assets/home/input-button.css'
import '@/assets/home/content-table.css'

import ParserPhoto from "@/views/ParserPhoto.vue";
import ProjectNamer from "@/components/ProjectNamer.vue"
import FileUploader from "@/components/FileUploader.vue";
import ModelSelector from "@/components/ModelSelector.vue";
import ChartDisplay from "@/components/ChartDisplay.vue";
import LogOutput from "@/components/LogOutput.vue";


export default {
  name: "HomeView",
  components: {
    ParserPhoto,
    ProjectNamer,
    FileUploader,
    ModelSelector,
    /*ChartDisplay,
    LogOutput,*/
  },
  data() {
    return {
      inputOffset: "",
      inputCount: "",
      items: [],
      activeIndex: 0,
      currentStage: "parser",
      menuList: ["parser", "namer", "uploader", "selector", "trainer"],
      projectName: "",
      filePath: "",
    };
  },
  methods: {
    nextPage(name) {
      this.setActive(this.activeIndex + 1);
      this.projectName = name;
    },
    nextPageTrain(pName, fPath) {
      this.setActive(this.activeIndex + 1);
      this.projectName = pName;
      this.filePath = fPath;
    },
    setActive(index) {
      this.activeIndex = index;
      this.currentStage = this.menuList[index];
    }
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