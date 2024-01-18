<template>
  <vue-tel-input-vuetify
    v-model="item"
    :label="label"
    default-country="RU"
    mode="national"
  ></vue-tel-input-vuetify>
</template>

<script>
export default {
  name: "PhoneInput",
  props: {
    itemValue: {
      type: String,
      default: null
    },
    label: {
      type: String,
      default: null
    }
  },
  computed: {
    item: {
      get() {
        return this.itemValue
      },
      set(value) {
        this.$emit('update', value)
      }
    }
  }
}
</script>

