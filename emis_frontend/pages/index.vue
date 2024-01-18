<template>
  <div>
  <v-tabs
      v-model="tab"
  >
    <v-tab href="#tab-main" :to="Info">
      ИНФО
    </v-tab>
    <v-tab href="#tab-metrology" :to="Control">
      КОНТРОЛЬ
    </v-tab>
  </v-tabs>
  <table-view
    :endpoint="endpoint"
    :headers="historyHeader"
    :toolbar="true"
    :add-button="false"
    height="calc(100vh - 260px)"
    :filters="filters"
  >
  </table-view>
  </div>
</template>
<script>
import TableView from "@/components/view/TableView";
import title from "~/mixin/main";

export default {
  auth: true,
  name: 'Index',
  components: {TableView},
  mixins: [title],
  data () {
    return {
      tab: null,
      endpoint: '/api/v1/history/',
      title: 'Рабочий стол',
      historyHeader: [
        {text: 'Дата', value: 'created_on', type: 'date', width: 150, format: 'HH:mm; dd.MM.yyyy', sourceFormat: 'dd.MM.yyyy HH:mm'},
        {text: 'Ответственный', value: 'user_name', width: 200, sortBy: 'history_user'},
        {text: 'Операция', value: 'type_name', sortBy: 'type'},
        {text: 'Оборудование', value: 'equipment_name', sortBy: 'equipment__name'},
        {text: 'Объект', value: 'entity_name', sortBy: 'entity__name'},
        {text: 'Информация', value: 'comment', sortable: false},
        {
          text: 'Документ',
          value: 'file',
          type: 'file',
          sortable: false,
        },
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
          title: 'Объект',
          name: 'entity',
          type: 'select-auto',
          endpoint: '/api/v1/entity/',
          selectData: []
        },
        {
          title: 'Операция',
          name: 'type',
          type: 'select',
          endpoint: '/api/v1/history_type/',
          selectData: []
        },
        {
          title: 'Ответственный',
          name: 'history_user__personnel',
          type: 'select-auto',
          endpoint: '/api/v1/personnel/',
          selectData: []
        },
      ]
    }
  },
  computed: {
    Control: {
      get() {
        return `/control`
      }
    },
    Info: {
      get() {
        return `/`
      }
    },
  }
}
</script>
