<template>
  <div>
    <div>
      <v-container>
        <v-row class="align-center align-content-center">
          <v-col cols="12" md="3">
            <select-autocomplete
              label="Сотрудник"
              endpoint="/api/v1/personnel/"
              :action="false"
              @update="idPersonnel = $event">

            </select-autocomplete>
          </v-col>
          <v-col cols="12" md="1">
            <v-btn
              color="primary"
              elevation="2"
              small
              dark
              class="mb-2"
              @click="change"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </v-col>
          <v-col v-if="showDeleteItems" cols="12" md="1">
            <v-btn class="error" @click="deleteSelected">Удалить выбранное</v-btn>
          </v-col>
        </v-row>

      </v-container>
      <v-card height="calc(70vh - 80px)" class="overflow-auto">
        <v-card>
          <table-view
            :endpoint="getEndpoint()"
            :headers="subdivisionHeader"
            height="calc(100%-100px)"
            :count-items="10"
            :reload="reload"
            :actions="false"
            :filters="filters"
            :toolbar="true"
            :add-button="false"
            :show-select="true"
            :click-row="true"
            @select="selected = $event"
          >
            <template #deleteButton>
              <v-btn class="error" @click="deleteSelected">Удалить выбранное</v-btn>
            </template>
            <template #card="row">
              <personnel-view :id="row.id" :delete-btn="false"></personnel-view>
            </template>
          </table-view>
        </v-card>
      </v-card>
    </div>
  </div>
</template>

<script>
import TableView from "~/components/view/TableView";
import SelectAutocomplete from "@/components/view/SelectAutocomplete";
import nationalPhone from "~/filters/nationalPhone";

export default {
  name: "SubDivisionTab",
  components: {SelectAutocomplete, TableView},
  filters: {
    nationalPhone,
  },
  props: {
    entityId: {
      type: String,
      default: null
    },
  },
  data() {
    return {
      reload: false,
      loaded: false,
      selected: [],
      showDeleteItems: false,
      openCard: false,
      idOpenItem: null,
      subdivisionHeader: [
        {text: 'ФИО', value: 'name'},
        {text: 'Должность', value: 'position'},
        {text: 'Отдел', value: 'department_name', sortable: true, sortBy: 'department__name'},
        {text: 'Телефон', value: 'phone', type: 'phone'},
        {text: 'Почта', value: 'email'}
      ],
      idPersonnel: [],
      endpoint: '/api/v1/personnel/',
      filters: [
        {
          title: 'Поиск',
          name: 'search',
          value: null,
          type: 'input',
          endpoint: null,
          selectData: []
        },
        {
          title: 'Отдел',
          name: 'department',
          type: 'select',
          endpoint: '/api/v1/department/',
          selectData: []
        },
      ]
    }
  },
  watch: {
    openCard(value) {
      if (!value) {
        this.$fetch()
      }
    }
  },
  methods: {
    deleteSelected() {
      this.selected.forEach(item => {
        this.delete(item.id)
      })
      this.selected = []
      setTimeout(() => {
        this.reload = true
        this.selected = []
      }, 100)
      this.reload = false
    },
    getEndpoint() {
      if (this.entityId !== null) {
        return `${this.endpoint}?entity=${this.entityId}`
      } else {
        return this.endpoint
      }
    },
    change() {
      const data = {
        entity: this.entityId
      }
      const message = "Сотрудник добавлен"
      this.$serverApi.$patch(`${this.endpoint}${this.idPersonnel}/`, data)
        .then(() => {
            this.idPersonnel = null
            this.reload = true
            this.$toast.success(message)
          }
        ).catch(() => {
      })
      this.reload = false
    },
    delete(deleteId) {
      const message = "Сотрудник удален"
      this.$serverApi.$patch(`${this.endpoint}${deleteId}/`, {entity: null})
        .then(() => {
            this.$toast.success(message)
          }
        ).catch(() => {
      })
    }
  }
}
</script>
