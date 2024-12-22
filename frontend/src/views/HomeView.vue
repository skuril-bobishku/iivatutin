<template>
  <div class="home">
    <div class="content">
      <ProjectNamer v-show="menuList[currentStage] === 'namer'"
                    :pName="projectName"
                    @nextPage="nextPage" />
      <ModelSelector v-show="menuList[currentStage] === 'selector'"
                     :pName="projectName"
                     :mName="modelName"
                     @nextPage="nextPage" />
      <ParserPhoto v-show="menuList[currentStage] === 'parser'"
                   :pName="projectName"
                   @nextPage="nextPage" />
      <FileUploader v-show="menuList[currentStage] === 'uploader'"
                    :pName="projectName"
                    :fPath="filePath"
                    @nextPage="nextPage"/>
      <TrainModel v-show="menuList[currentStage] === 'trainer'" />
      <!--<ChartDisplay v-show="currentStage === 'train'" />
      <LogOutput v-show="currentStage === 'train'" />-->
    </div>
    <div class="navigation">
      <button
        v-for="(stage, index) in menuList"
        :key="index"
        :class="{ 'nav-button': true, active: currentStage >= index }"
        @click="menuClick(index)"
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
import '@/assets/home/input-file.css'

import ProjectNamer from "@/components/ProjectNamer.vue"
import ModelSelector from "@/components/ModelSelector.vue";
import ParserPhoto from "@/views/ParserPhoto.vue";
import FileUploader from "@/components/FileUploader.vue";
import TrainModel from "@/components/TrainModel.vue"
import ChartDisplay from "@/components/ChartDisplay.vue";
import LogOutput from "@/components/LogOutput.vue";

export default {
  name: "HomeView",
  components: {
    ProjectNamer,
    ModelSelector,
    ParserPhoto,
    FileUploader,
    TrainModel,
    /*ChartDisplay,
    LogOutput,*/
  },
  data() {
    return {
      currentStage: 0,
      menuList: {
        0: 'namer',
        1: 'selector',
        2: 'parser',
        3: 'uploader',
        4: 'trainer',
      },
      projectName: '',
      modelName: '',
      filePath: '',
    };
  },
  methods: {
    nextPage(pName, mName, fPath) {
      let nextPage = parseInt(this.currentStage, 10);

      switch (this.menuList[this.currentStage]) {
        case 'namer':
        case 'uploader':
        case 'trainer':
          nextPage = nextPage + 1;
          break;

        case 'parser':
          nextPage = nextPage + 2;
          break;

        case 'selector':
          nextPage = nextPage + 3;
          break;

        default:
          break;
      }

      this.setActive(nextPage);

      if (this.projectName !== undefined || this.projectName !== '') {
        this.projectName = mName
      }

      if (this.modelName !== undefined || this.modelName !== '') {
        this.modelName = mName
      }

      if (this.filePath !== undefined || this.filePath !== '') {
        this.filePath = fPath;
      }

      console.log('pr: ', this.projectName)
      console.log('mo: ', this.modelName)
      console.log('fi: ', this.filePath)
    },
    menuClick(index) {
      switch (this.menuList[index]) {
        case 'namer':
          //this.setActive(index);
          break;

        case 'selector':
          if (this.menuList[this.currentStage] !== 'parser' &&
              this.menuList[this.currentStage] !== 'uploader' &&
              this.menuList[this.currentStage] !== 'trainer') {
            if (this.projectName.trim()) {
              this.setActive(index);
            }
          }
          break;

        case 'parser':
        case 'uploader':
          if (this.menuList[this.currentStage] !== 'selector' &&
              this.menuList[this.currentStage] !== 'trainer') {
            if (this.modelName.trim()) {
              this.setActive(index);
            }
          }
          break;


        case 'trainer':
          //if (this.filePath.trim()) {
            this.setActive(index);
          //}
          break;

        default:
          break;
      }
    },
    setActive(index) {
      this.currentStage = index;
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