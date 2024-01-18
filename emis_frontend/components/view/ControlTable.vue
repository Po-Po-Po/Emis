<template>
  <div>
    <v-card>
      <v-card-actions v-if="toolbar">
        <v-container>
          <v-row class="align-center align-md-center justify-start">
            <v-col v-for="filter in filters" :key="filter.name" cols="12" md="2">
              <v-text-field
                  v-if="filter.type === 'input' || filter.type === 'search'"
                  :ref="filter.name"
                  v-model="filter.value"
                  :label="filter.title"
                  :placeholder="filter.placeholder"
                  clearable
              >
              </v-text-field>
              <select-autocomplete
                  v-if="filter.type === 'select-auto'"
                  :label="filter.title"
                  :endpoint="filter.endpoint"
                  :server-search="true"
                  :action="false"
                  @update="filterValueUpdate($event, filter.name)"
              ></select-autocomplete>
              <select-api
                  v-if="filter.type === 'select'"
                  :endpoint="filter.endpoint"
                  :label="filter.title"
                  @update="filterValueUpdate($event, filter.name)"
              ></select-api>
            </v-col>
          </v-row>
        </v-container>
      </v-card-actions>
      <v-data-table
          dense
          :item-class="getDateClass"
          :headers="headerAction"
          :items="desserts"
          :items-per-page="countItems"
          :options.sync="options"
          :server-items-length="totalDesserts"
          :loading="loading"
          fixed-header
          :height="height"
          :footer-props="{
          itemsPerPageOptions: PageOptions,
        }"

      >
        <template
            v-for="header in headers"
            #[`item.${header.value}`]="{ item }"
        >
          <slot v-if="header.type === 'date'" :name=header.value :item="item">
            <div v-if="item[header.value]" :key="header.name">
              {{ item[header.value] | dateFormater(header.format)}}
            </div>
          </slot>
          <slot v-else :name=header.value :item="item">
            <v-menu
                v-if="menuRow"
                transition="slide-x-transition"
                max-width="220"
                bottom
                right
            >
              <template #activator="{ on, attrs }">
                <div v-bind="attrs" v-on="on">
                  {{ item[header.value] }}
                </div>

              </template>
              <v-list>
                <v-list-item dense>
                  <v-btn
                      x-small
                      block
                      :to="actionClickRow(item)">Открыть
                  </v-btn>
                </v-list-item>
                <v-list-item dense>
                  <v-btn
                      x-small
                      block
                      :to="actionClickRow(item)" target="_blank">Открыть в новой вкладке
                  </v-btn>
                </v-list-item>
              </v-list>
            </v-menu>
          </slot>
        </template>
      </v-data-table>
      <v-dialog
          v-model="openCard"
          max-width="calc(70%)"
      >
        <slot v-if="openCard" :id="idOpenItem" name='card'>
          <v-card>
            <h1>{{ idOpenItem }}</h1>
          </v-card>
        </slot>
      </v-dialog>
    </v-card>
  </div>
</template>

<script>
import SelectAutocomplete from "./SelectAutocomplete";
import SelectApi from "./SelectApi";
import moment from 'moment';

export default {
  name: "TableView",
  components: {SelectAutocomplete, SelectApi},
  props: {
    headers: {
      type: Array,
      default: () => [
        {
          text: 'Dessert (100g serving)',
          align: 'start',
          sortable: false,
          value: 'name',
        },
        {text: 'Calories', value: 'calories'},
        {text: 'Fat (g)', value: 'fat'},
        {text: 'Carbs (g)', value: 'carbs'},
        {text: 'Protein (g)', value: 'protein'},
        {text: 'Iron (%)', value: 'iron'},
      ],
    },
    endpoint: {
      type: String,
      default: ''
    },
    countItems: {
      type: Number,
      default: 25
    },
    height: {
      type: String,
      default: '700px'
    },
    actions: {
      type: Boolean,
      default: false
    },
    toolbar: {
      type: Boolean,
      default: false
    },
    clickRow: {
      type: Boolean,
      default: false
    },
    addButton: {
      type: Boolean,
      default: true
    },
    filters: {
      type: Array,
      default: () => []
    },
    menuRow: {
      type: Boolean,
      default: false
    }
  },
  filters: {
    dateFormater(date, format) {
        const momentDate = moment(date, "YYYY-MM-DD", true);
        if (momentDate.isValid()) {
          const standardizedDate = momentDate.format(format);
          return standardizedDate;
        } else {
          return date;
        }
    }
  },
  data() {
    return {
      sortDesc: false,
      sortBy: '',
      showDeleteItems: false,
      idOpenItem: null,
      dialog: false,
      openCard: false,
      selectDeleteObject: '',
      totalDesserts: 0,
      desserts: [],
      loading: true,
      options: {},
      search: [],
      searchField: null,
      resultData: [],
      PageOptions: ([5, 10, 25, 50, -1]),
      pageLimit: null,
      pageOffset: null,
      pageFilter: [],
      page: 1,
      action: {
        text: 'Действие',
        value: 'actions',
        type: 'action',
        sortable: false,
        align: 'center',
        width: 100
      },
      resultFilter: [],
      url: null,
    }
  },
  computed: {
    headerAction() {
      if (this.actions) {
        return [...this.headers, this.action]
      }
      return this.headers
    },
    baseUrl() {
      return this.$config.axios.baseURL
    }
  },
  watch: {
    options: {
      handler() {
        this.getDataFromApi()
      },
      deep: true
    },
    async endpoint() {
      await this.getDataFromApi()
    },
    reload: {
      async handler(value) {
        if (value) {
          await this.getDataFromApi()
          this.showDeleteItems = false
        }
      },
      deep: true
    },
    filters: {
      handler(value) {
        let count
        let error = {type: 'success', message: null}
        const validateItem = []
        const setValidateItem = (name) => {
          validateItem.forEach(i => {
            if (i.name === name){
              i.status = true
            }
          })
        }
        if (value) {
          value.forEach(item => {
            const validateInputCount = 3
            if (item.type === 'search' || item.name === 'search') {
              validateItem.push({'name': item.name, 'status': false})
              if (item.value) {
                count = item.value.length
              }
              if (item.value && count >= item.validateInputCount && item.validator && item.value){
                error = item.validator(item.value)
                setValidateItem(item.name)
              }
              if (!item.value && item.validateInputCount && item.validator) {
                setValidateItem(item.name)
              }
              if (count >= validateInputCount && !item.validateInputCount && !item.validator) {
                setValidateItem(item.name)
              }
              if (!item.value && !item.validateInputCount && !item.validator) {
                setValidateItem(item.name)
              }
            }
          })
        }
        if (error.type !== 'error' && validateItem.every(element => element.status === true)) {
          this.getDataFromApi()
        } else {
          this.$toast.error(error.message)
        }
        if (count === undefined) {
          this.getDataFromApi()
        }
      },
      deep: true
    },
  },
  methods: {
    filterValueUpdate(value, filter) {
      const filters = []
      const dateFilter = []
      this.filters.forEach(item => {
        if (item.name === filter) {
          item.value = value
          if (item.type === 'date-range') {
            dateFilter.push(
                {
                  name: `${item.name}_after`,
                  value: item.value[0]
                },
                {
                  name: `${item.name}_before`,
                  value: item.value[1]
                }
            )
          } else {
            filters.push(item)
          }
        }
      })
      if (dateFilter.length > 0) {
        this.resultFilter = this.resultFilter.filter(
            item => {
              return !(item.name.includes('_after') || item.name.includes('_before'));
            }
        )
      }
      this.resultFilter = [...this.resultFilter, ...filters, ...dateFilter]
      if (this.resultFilter) {
        this.getDataFromApi()
      }
    },
    async getDataFromApi() {
      this.loading = true
      await this.fakeApiCall().then(data => {
        this.desserts = data.items
        this.totalDesserts = data.total
        this.loading = false
      })
    },
    actionClickRow(value) {
      if (value.section === 'Персонал') {
        let url = 'personnel/'
        return `${url}${value.item_id}/`
      }
      if (value.section === 'Оборудование') {
        let url = 'equipment/'
        return `${url}${value.item_id}/`
      }
    },
    getUrl(printUrl=false) {
      let url = this.endpoint
      if (printUrl){
        url = this.printServerUrl
      }
      let resultFilter = [
        ...this.resultFilter, ...this.filters.filter(item => item.type === 'input' || item.type === 'search'), ...this.pageFilter
      ]
      if (this.sortBy){
        let desc = ''
        if (!this.sortDesc){
          desc = '-'
        }
        resultFilter = [...resultFilter, {name: 'ordering', value: `${desc}${this.sortBy}`}]
      }
      if (resultFilter) {
        resultFilter.forEach((item) => {
          if (item.value) {
            if (url.includes('?') && url.includes('=')) {
              url = url + '&'
            } else {
              url = url + '?'
            }
            url = `${url}${item.name}=${item.value}`
          }
        })
      }
      return url
    },
    getPage(limit, page) {
      this.pageLimit = limit
      if (this.pageLimit < 0) {
        this.pageLimit = null
      }
      if (page === 1) {
        this.pageOffset = this.pageLimit
      }
      if (page > 1) {
        if (page > this.page) {
          this.pageOffset = this.pageOffset + this.pageLimit
        } else {
          this.pageOffset = this.pageOffset - this.pageLimit
        }
      } else {
        this.pageOffset = null
      }
      this.page = page

      this.pageFilter = [
        {name: 'offset', value: this.pageOffset},
        {name: 'limit', value: this.pageLimit},
      ]
    },
    async fakeApiCall() {
      return await new Promise((resolve) => {
        const {sortBy, sortDesc, page, itemsPerPage} = this.options
        if (sortBy.length === 1 && sortDesc.length === 1) {
          this.sortBy = sortBy[0]
          this.sortDesc = sortDesc[0]
          this.headers.forEach(item => {
            if (item.sortBy && item.value === this.sortBy){
              this.sortBy = item.sortBy
            }
          })
        }

        this.getPage(itemsPerPage, page)
        this.url = this.getUrl()
        let total = 0
        this.$serverApi.$get(this.url)
            .then(response => {
              if (response.results) {
                this.resultData = response.results
                total = response.count
              } else {
                this.resultData = response
                total = this.resultData.length
              }
              const items = this.resultData
              resolve({
                items,
                total,
              })
            })
            .catch(e => {
              this.$toast.error(e + ': ' + e.response.data)
            })
      })
    },
    getDateClass(data) {
        const dateValue = data.end_date
        const currentDate = new Date();
        const parts = dateValue.split('.');
        const formattedDate = new Date(`${parts[2]}-${parts[1]}-${parts[0]}`);
        const differenceInDays = Math.floor((formattedDate - currentDate) / (1000 * 60 * 60 * 24));
        if (differenceInDays <= 10) {
          return 'red-background'
        } else if (differenceInDays <= 20 && differenceInDays > 10) {
          return 'yellow-background'
        } else {
          return ''
        }
    },

  }
}
</script>

<style>
.yellow-background {
  background-color: #FFEF9A;
}

.red-background {
  background-color: #FFD8D8;
}
</style>


