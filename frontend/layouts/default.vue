<template>
  <div class="container">
    <LayoutHeader />
      <div class="content section-wrap">
        <slot />
      </div>
      <LayoutFooter />
  </div>
</template>

<style scoped>
  .container {
    width: 100vw;
    min-height: 100vh;
    position: absolute;
    top: 0;
    right: 0;
  }

  .content {
    padding-top: 10rem;
    padding-bottom: 5rem;
    min-height: calc(100vh - 8rem);
  }
</style>