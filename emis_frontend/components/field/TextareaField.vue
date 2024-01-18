<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" md="12">
          <tiptap-editor v-model="valueItem" label="Важная информация"></tiptap-editor>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import TiptapEditor from "~/components/field/TiptapEditor";

export default {
  name: "TextField",
  components: {TiptapEditor},
  props: {
    value: {
      type: String,
      default: null
    },
    label: {
      type: String,
      default: null
    },
  },
  data() {
    return {}
  },
  computed: {
    valueItem: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('update', value)
      }
    },
  }
}
</script>
