<template>
  <v-row>
    <v-col class="text-center">
      <blockquote class="blockquote">
        Страница: {{ $route.name }}, находится в разработки
        <footer>
          <small>
            <em>&mdash;Administrator</em>
          </small>
        </footer>
      </blockquote>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: "EmptyPage"
}
</script>
