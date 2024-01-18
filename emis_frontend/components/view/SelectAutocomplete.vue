<template>
  <div>
    <v-autocomplete
      v-model="selectedItem"
      :loading="loading"
      :items="dataObject"
      :search-input.sync="search"
      item-text="name"
      item-value="id"
      :label="`${label}`"
      class="v-size--default"
      :filter="filter"
      :no-filter="noFilter"
      :deletable-chips="true"
      :disabled="isDisabled"
      clearable
      @click:clear="selectedItem = null"
    >
      <template v-if="action" #append-outer>
        <v-btn icon @click="addAction">
          <v-icon>
            mdi-plus-thick
          </v-icon>
        </v-btn>
        <v-btn icon @click="editAction">
          <v-icon>
            mdi-square-edit-outline
          </v-icon>
        </v-btn>
      </template>
      <template #item="data">
        <slot name="item" :item="data.item">
          {{ data.item.name }}
        </slot>
      </template>

    </v-autocomplete>
    <v-dialog
      v-model="dialog"
      max-width="490"
    >
      <slot v-for="i in ['default']" :id="valueSlotAction" :name="i">

      </slot>
    </v-dialog>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: "SelectAutocomplete",
  props: {
    endpoint: {
      type: String,
      default: null
    },
    action: {
      type: Boolean,
      default: false
    },
    closeDialog: {
      type: Boolean,
      default: false
    },
    isDisabled: {
      type: Boolean,
      default: false
    },
    items: {
      type: Array,
      default: () => []
    },
    label: {
      type: String,
      default: null
    },
    filter: {
      type: Function,
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      default: (item, queryText, itemText) => {
        return itemText.toLocaleLowerCase().includes(queryText.toLocaleLowerCase())
      },
    },
    noFilter: {
      type: Boolean,
      default: false
    },
    serverSearch: {
      type: Boolean,
      default: false
    },
    item: {
      type: String && Number,
      default: null
    },
  },
  data() {
    return {
      search: null,
      loading: false,
      dialog: false,
      selected: null,
      valueSlotAction: null,
      dataObject: [],
      dataObjectItems: [],
    }
  },
  created(){
    this.debouncedGetAnswer = _.debounce(this.searchApi, 1000)
  },
  fetch() {
    this.loading = true
    // if (!this.item){}
    this.$serverApi.$get(`${this.endpoint}?page_size=10`).then(response => {
      if (response.results){
        this.dataObject = response.results
      } else {
        this.dataObject = response
      }
      this.loading = false
      if (this.item){
       this.selectedItem = this.item
      }
    })
  },
  computed: {
    selectedItem: {
      get() {
        return this.selected
      },
      set(value) {
        this.selected = value
        this.valueSlotAction = value
        this.$emit('update', value)
        this.searchApi(value)
      }
    },
  },
  watch: {
    search(value) {
      this.loading = true
      this.debouncedGetAnswer(value)
    },
    closeDialog: {
      handler() {
        this.dialog = false
        this.$fetch()
      },
      deep: true
    },
    item: {
      handler(value) {
        this.selectedItem = value
      },
      deep: true
    }
  },
  methods: {
    searchApi(value) {
      this.$serverApi.$get(`${this.endpoint}?search=${value}&page_size=20`,)
        .then((response) => {
          if (response.results) {
            this.dataObject = response.results
          } else {
            this.dataObject = response
          }
          this.loading = false
        })
    },
    addAction() {
      this.valueSlotAction = null
      this.dialog = true
    },
    editAction() {
      this.valueSlotAction = this.selectedItem
      this.dialog = true
    },
  }
}
</script>
