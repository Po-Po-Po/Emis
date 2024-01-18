<template>
  <div>
    <v-card>
      <v-card-actions v-if="toolbar">
        <v-container>
          <v-row class="align-center align-md-center justify-start">
            <v-col v-if="addButton" cols="6" md="1">
              <v-btn
                color="primary"
                elevation="2"
                dark
                class="mb-1 mx-0"
                :to="createUrl"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
            <v-col v-if="xlsxButton" cols="6" md="1">
              <v-btn
                  title="Сохранить в xlsx"
                  color="primary"
                  elevation="2"
                  dark
                  class="mb-1 mx-0"
                  @click="handlePrintRequest"
              >
                <v-icon>mdi-file-excel-outline</v-icon>
              </v-btn>
            </v-col>
            <v-col v-if="printButton" cols="12" md="1">
              <v-btn
                color="primary"
                elevation="2"
                dark
                class="mb-2"
                @click="printTable"
              >
                <v-icon>mdi-file-excel-outline</v-icon>
              </v-btn>
            </v-col>
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
              <date-picker
                v-if="filter.type === 'date'"
                :item="filter.value"
                :label="filter.title"
                @update="filterValueUpdate($event, filter.name)"
              ></date-picker>
              <date-picker
                v-if="filter.type === 'date-range'"
                :dates="filter.value"
                :label="filter.title"
                :range="true"
                @update="filterValueUpdate($event, filter.name)"
              ></date-picker>
            </v-col>
            <v-col v-if="showDeleteItems" cols="12" md="2">
              <slot name="deleteButton">
                <v-btn class="error">Удалить выбранное</v-btn>
              </slot>
            </v-col>
          </v-row>
        </v-container>
      </v-card-actions>
      <v-data-table
        v-model="selected"
        dense
        :headers="headerAction"
        :items="desserts"
        :items-per-page="countItems"
        :options.sync="options"
        :server-items-length="totalDesserts"
        :loading="loading"
        class="elevation-1"
        fixed-header
        :height="height"
        :single-select="singleSelect"
        :show-select="showSelect"
        :footer-props="{
          itemsPerPageOptions: PageOptions,
        }"
        @click:row="actionClickRow"
      >
        <template
          v-for="header in headers"
          #[`item.${header.value}`]="{ item }"

        >
          <slot v-if="header.type === 'file'" :name=header.value :item="item">
            <a v-if="item[header.value]" :key="header.value" :href="baseUrl + item[header.value]" target="_blank">
              <v-icon>
                mdi-file-download
              </v-icon>
            </a>
          </slot>
          <slot v-else-if="header.type === 'date'" :name=header.value :item="item">
            <div v-if="item[header.value]" :key="header.name">
              {{ item[header.value] | dateFormater(header.format, header.sourceFormat) }}
            </div>
          </slot>
          <slot v-else-if="header.type === 'phone'" :name=header.value :item="item">
            <div v-if="item[header.value]" :key="header.name">
              {{ item[header.value] | nationalPhone }}
            </div>
          </slot>
          <slot v-else-if="header.type === 'array'" :name=header.value :item="item">
            {{ item[header.value] | arrayToString(header.showField) }}
          </slot>
          <slot v-else-if="header.type === 'object'" :name=header.value :item="item">
            {{ item[header.value][header.showField] }}
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
                    :to="actionClickRow(item, true)">Открыть
                  </v-btn>
                </v-list-item>
                <v-list-item dense>
                  <v-btn
                    x-small
                    block
                    :to="actionClickRow(item, true)" target="_blank">Открыть в новой вкладке
                  </v-btn>
                </v-list-item>
              </v-list>
            </v-menu>
            <div v-else :key="item.id">
              {{ item[header.value] }}
            </div>
          </slot>
        </template>
        <template #item.actions="{ item }">
          <slot name="action_custom" :item="item">
            <v-icon small @click="deleteDataObject(item.id)">
              mdi-delete
            </v-icon>
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
      <v-dialog
        v-model="dialog"
        persistent
        max-width="290"
      >
        <v-card>
          <v-card-title class="text-h5">
            Удалить?
          </v-card-title>
          <v-card-text>

          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="error darken-1"
              text
              @click="dialog = false"
            >
              Нет
            </v-btn>
            <v-btn
              color="green darken-1"
              text
              @click="deleteDataObject(null, true)"
            >
              Да
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </div>
</template>

<script>
import SelectAutocomplete from "./SelectAutocomplete";
import SelectApi from "./SelectApi";
import DatePicker from "./DatePicker";
import nationalPhone from "~/filters/nationalPhone";
import arrayToString from "~/filters/arrayToString";
import dateFormater from "~/filters/dateFormater";

export default {
  name: "TableView",
  components: {DatePicker, SelectAutocomplete, SelectApi},
  filters: {
    nationalPhone,
    arrayToString,
    dateFormater
  },
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
    title: {
      type: String,
      default: 'Table'
    },
    createUrl: {
      type: String,
      default: '/'
    },
    showSelect: {
      type: Boolean,
      default: false
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
    dataList: {
      type: Array,
      default: () => []
    },
    actions: {
      type: Boolean,
      default: false
    },
    reload: {
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
    xlsxButton: {
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
    closeCard: {
      type: Boolean,
      default: true
    },
    menuRow: {
      type: Boolean,
      default: false
    },
    cardUrl: {
      type: String,
      default: null
    },
    idItem: {
      type: String,
      default: null
    },
    printButton: {
      type: Boolean,
      default: false
    },
    printServerUrl: {
      type: String,
      default: null
    },
    printServerUrlParams: {
      type: String,
      default: null
    },
    printFileName: {
      type: String,
      default: 'table_data.xlsx'
    }
  },
  asyncData({$dateFns}) {
    return {
      dateFormatted: $dateFns.format(new Date())
    }
  },
  data() {
    return {
      sortDesc: false,
      sortBy: '',
      showDeleteItems: false,
      idOpenItem: null,
      singleSelect: false,
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
      PageOptions: ([5, 25, 50, 10, -1]),
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
    },
    selected: {
      get() {
        return []
      },
      set(value) {
        this.showDeleteItems = value.length > 0;
        this.$emit('select', value)
      }
    },
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
    closeCard(value) {
      if (value) {
        this.openCard = false
      }
    }
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
    handlePrintRequest() {
      this.$toast.info('Файл формируется, ожидайте ...')
      this.$axios({
        url: 'api/v1/personnel_print/',
        method: "GET",
        responseType: 'blob'
      }).then((response) => {
        const href = URL.createObjectURL(response.data);
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', this.printFileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(href)
      })
    },
    async getDataFromApi() {
      this.loading = true
      await this.fakeApiCall().then(data => {
        this.desserts = data.items
        this.totalDesserts = data.total
        this.loading = false
      })
    },
    async deleteDataObject(idObject, deleteObject = false) {
      this.dialog = true
      if (idObject) {
        this.selectDeleteObject = `${this.endpoint}${idObject}/`
      }
      if (deleteObject) {
        await this.$serverApi.$delete(this.selectDeleteObject).then(() => {
          this.desserts = []
          this.getDataFromApi()
          this.$toast.success('Успешное удаление')
        })
        this.dialog = false
      }
    },
    actionClickRow(value, createUrl = false) {
      let url = this.$route.name
      if (this.cardUrl){
        url = this.cardUrl
        return `${url}${value[this.idItem]}/`
      }
      if (url.includes('-id')) {
        url = this.endpoint.split('/')
        url = `/${url[url.length - 2]}`
        this.idOpenItem = value.id
        if (this.clickRow) {
          this.openCard = true
        }
      }
      if (this.clickRow && !this.openCard) {
        if (createUrl === true && this.menuRow) {
          return `/${url}/${value.id}/`
        } else {
          this.$router.push(`/${url}/${value.id}/`)
        }
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
    getPrintUrl(){
      let url = this.getUrl(true)
      if (this.printServerUrlParams){
        url = `${url}&${this.printServerUrlParams}`
      }
      return url
    },
    printTable() {
      this.$toast.info('Файл формируется, ожидайте ...')
      this.$axios({
        url: this.getPrintUrl(),
        method: "GET",
        responseType: 'blob'
      }).then((response) => {
        const href = URL.createObjectURL(response.data);
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', this.printFileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(href)
      })
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
  }
}
</script>


