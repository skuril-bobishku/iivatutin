<template>
  <div class="content-view project-namer">
    <h3>Назовите проект</h3>
    <input type="text"
           class="input-text"
           placeholder="Введите название"
           v-model="projectName"
    />
    <button class="input-button"
            @click="nextPage"
            :disabled="!this.projectName.trim()"
    >Создать проект</button>
  </div>
</template>

<script>
import '@/assets/project-namer/project-namer.css'

export default {
  name: "ProjectNamer",
  props: {
    pName: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      projectName: this.pName,
    };
  },
  watch: {
    pName(newName) {
      this.projectName = newName;
    },
  },
  methods: {
    validatePath(name) {
      const forbiddenChars = /[./\\*?|]/;
      return !forbiddenChars.test(name);
    },
    nextPage() {
      if (!this.validatePath(this.projectName)) {
        alert("Использованы запрещённые символы!");
        return;
      }

      this.$emit('nextPage', this.projectName, '', '');
    },
  },
}
</script>