<template>
        <v-text-field
          v-if="!range"
          v-model="dateFormate"
          :label="label"
          prepend-icon="mdi-calendar"
          type="date"
        ></v-text-field>
        <v-menu
          v-else
          ref="menu"
          v-model="menu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateList"
              :label="label"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateList"
            range
            no-title
            scrollable
          >
          </v-date-picker>
        </v-menu>
</template>

<script>
import { convertDateFormat } from '@/utils'
export default {
  name: "DatePicker",
  props: {
    label: {
      type: String,
      default: null
    },
    item: {
      type: Object && String,
      default: () => {
      }
    },
    dates: {
      type: Array,
      default: () => []
    },
    range: {
      type: Boolean,
      default: false
    },
    formatStart: {
      type: String,
      default: "dd.MM.yyyy"
    },
    formatEnd: {
      type: String,
      default: "yyyy-MM-dd"
    }
  },
  data() {
    return {
      show: false,
      idEquipment: null,
      dateString: null
    }
  },
  computed: {
    date: {
      get() {
        return this.item
      },
      set(value) {
        this.$emit('update', value)
      }
    },
    dateFormate: {
      get() {
        return convertDateFormat(this.item, this.formatStart, this.formatEnd)
      },
      set(value) {
        this.$emit('update', convertDateFormat(value, this.formatEnd, this.formatStart))
      }
    },
    dateList: {
      get() {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        this.dateString = this.dates.join(' ~ ')
        return this.dates
      },
      set(value) {
        this.$emit('update', value)
      }
    }
  }
}
</script>
