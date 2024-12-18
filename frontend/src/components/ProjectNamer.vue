<template>
  <div class="content-view project-namer">
    <h3>Назовите проект</h3>
    <input
        type="text"
        class="input-text"
        placeholder="Введите название"
    />
    <button
        class="input-button"
    >Создать проект</button>
  </div>
</template>

<script>
import '@/assets/project-namer/project-namer.css'

export default {
  name: "ProjectNamer",

}
</script>