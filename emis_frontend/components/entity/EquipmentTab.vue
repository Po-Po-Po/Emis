<template>
  <div>
    <v-container>
      <v-row class="align-center">
        <v-col cols="12" md="1">Добавить:</v-col>
        <v-col cols="12" md="3">
          <select-autocomplete
            label="Оборудование"
            :endpoint="endpoint"
            :server-search="true"
            :no-filter="true"
            :action="false"
            @update="update"
          >
            <template #item="data">
              {{ data.item.name }} ({{ data.item.factory_number }})
            </template>
          </select-autocomplete>
        </v-col>
        <v-col cols="12" md="4">
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
      </v-row>
    </v-container>
    <v-card height="calc(70vh - 80px)" class="overflow-auto">
      <table-view
        :headers="header"
        :endpoint="`${endpoint}?entity=${entityId}`"
        :count-items="10"
        height="calc(100%-100px)"
        :reload="reload"
        :actions="false"
        :filters="filters"
        :toolbar="true"
        :add-button="false"
        :click-row="clickRow"
        :show-select="true"
        @select="selectItem"
      >
        <template #deleteButton>
          <v-btn class="error" @click="deleteSelected">Удалить выбранное</v-btn>
        </template>
        <template #card="row">
          <equipment-view :id="row.id" :delete-btn="false"></equipment-view>
        </template>
      </table-view>
    </v-card>
  </div>
</template>

<script>
import TableView from "~/components/view/TableView";
import SelectAutocomplete from "@/components/view/SelectAutocomplete";


export default {
  name: "EquipmentTab",
  components: {SelectAutocomplete, TableView},
  props: {
    entityId: {
      type: String,
      default: null
    },
    dataObject: {
      type: Object,
      default: () => {
      }
    },
    endpointEntity: {
      type: String,
      default: '/'
    }
  },
  data() {
    return {
      clickRow: true,
      selected: [],
      header: [
        {text: 'Тип', value: 'type_name', sortBy: 'type'},
        {text: 'Наименование', value: 'name'},
        {text: 'Заводской номер', value: 'factory_number'},
        {text: 'Инвентарный номер', value: 'inventory_number'},
        {text: 'Метрология', value: 'validity', type: 'date'},
      ],
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
          title: 'Тип оборудования',
          name: 'type',
          type: 'select',
          endpoint: '/api/v1/equipment_type/',
          selectData: []
        },
      ],
      endpoint: '/api/v1/equipment/',
      reload: false,
      idEquipment: null,
    }
  },
  computed: {
    item: {
      get() {
        return this.dataObject.equipment
      },
      set(value) {
        this.$emit('update', value)
      }
    }
  },
  methods: {
    deleteSelected() {
      this.selected.forEach(item => {
        this.change(item.id)
      })
    },
    selectItem(value) {
      this.selected = value
    },
    update(value) {
      this.idEquipment = value
    },
    change(deleteId) {
      let message = ''
      if (this.idEquipment) {
        this.item = [...this.item, this.idEquipment]
        message = 'Оборудование добавленно'
      }
      if (deleteId && this.idEquipment === null) {
        this.item = this.item.filter(item => item !== deleteId)
        message = 'Оборудование удаленно'
      }
      const data = {equipment: this.item}

      this.$serverApi.$patch(`${this.endpointEntity}${this.entityId}/`, data)
        .then(() => {
            this.idEquipment = null
            this.reload = true
            this.$toast.success(message)
          }
        ).catch(() => {
      })

      this.reload = false
    },
  },
}
</script>
