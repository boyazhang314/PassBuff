<template>
  <div class="container">
    <router-view />
  </div>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style>
body {
  margin: 0;
  padding: none;;
  box-sizing: border-box;
}

.container {
  height: 100vh;
  width: 100%;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  background: linear-gradient(.25turn, #0076BE, #8BD9C7);
}
</style>
