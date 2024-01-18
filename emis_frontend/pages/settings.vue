<template>
  <empty-page></empty-page>
</template>
<script>
import title from "../mixin/main";

export default {
  auth: true,
  name: 'Settings',
  mixins: [title],
  data() {
    return {
      title: 'Настройки'
    }
  }
}
</script>
