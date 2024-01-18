<template>
  <v-card :min-height="minHeight" light>
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
    <control-table
        :endpoint="`${endpoint}`"
        :headers="headers"
        :menu-row="true"
        :actions="false"
        :toolbar="true"
        :add-button="false"
        :click-row="true"
        height="calc(100vh - 260px)"
        :filters="filters"
    >
    </control-table>
  </v-card>
</template>
<script>
import ControlTable from "~/components/view/ControlTable.vue";
import title from "~/mixin/main";
import dateFormater from "~/filters/dateFormater";

export default {
  auth: true,
  name: 'Control',
  components: {ControlTable},
  filters: {
    dateFormater
  },
  mixins: [title],
  data() {
    return {
      tab: null,
      endpointPrint: '/api/v1/control/',
      endpoint: '/api/v1/control/',
      title: 'Контроль',
      headers: [
        {text: 'Раздел', value: 'section', sortable: false},
        {text: 'Тип', value: 'type'},
        {text: 'Информация', value: 'info'},
        {text: 'Номер', value: 'number'},
        {text: 'Объект', value: 'entity'},
        {text: 'Отдел', value: 'department'},
        {text: 'Дата окончания', value: 'end_date', type: 'date', format: 'DD.MM.YYYY'}
      ],
      filters: [
        {
          title: 'Поиск по информации',
          name: 'search_info',
          value: null,
          type: 'search',
          endpoint: '/api/v1/control/',
          selectData: []
        },
        {
          title: 'Поиск по номеру',
          name: 'search_number',
          value: null,
          type: 'search',
          endpoint: '/api/v1/control/',
          selectData: []
        },
        {
          title: 'Раздел',
          name: 'section',
          type: 'select',
          endpoint: '/api/v1/section/',
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
          title: 'Отдел',
          name: 'department',
          type: 'select-auto',
          endpoint: '/api/v1/department/',
          selectData: []
        }
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
    }
  },
  methods: {

  }
}
</script>
