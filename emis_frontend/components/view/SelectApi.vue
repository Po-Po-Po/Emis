<template>
  <v-select
    v-model="itemObject"
    :items="items"
    item-text="name"
    item-value="id"
    :label="label"
    clearable
  ></v-select>
</template>

<script>
export default {
  name: "SelectApi",
  props: {
    endpoint: {
      type: String,
      default: '/'
    },
    label: {
      type: String,
      default: 'Select'
    },
    item: {
      type: String,
      default: null
    },
  },
  data() {
    return {
      items: [],
    }
  },
  async fetch() {
    this.items = await this.$serverApi.$get(this.endpoint)
  },
  computed: {
    itemObject: {
      get() {
        return this.item
      },
      set(value){
        this.$emit('update', value)
      }
    }
  },
  watch: {}
}
</script>
