<template>
  <div>
    <v-tabs
      v-model="tab"
    >
      <v-tab href="#tab-main" :to="ReportCardUrl">
        Табель
      </v-tab>
      <v-tab href="#tab-metrology" :to="FundUrl">
        Фонд
      </v-tab>
    </v-tabs>
  <table-view
    :endpoint="endpoint"
    :headers="headers"
    :menu-row="true"
    :actions="false"
    :toolbar="true"
    :click-row="true"
    create-url="/report_card/new"
    height="calc(100vh - 260px)"
    :filters="filters"
  >
  </table-view>
  </div>
</template>

<script>
import TableView from "~/components/view/TableView";
import title from "~/mixin/main";
import { periodValidator } from "@/utils";

export default {
  auth: true,
  name: 'ReportCard',
  components: {TableView},
  mixins: [title],
  data() {
    return {
      tab: null,
      endpoint: '/api/v1/report_card/',
      title: 'Табель',
      headers: [
        {
          text: 'Табель',
          align: 'card',
          sortable: true,
          value: 'card',
        },
        {text: 'Период', value: 'period'},
        {text: 'Объект', value: 'entity_name', sortBy: 'entity__directorate'},
        {text: 'Ответственный', value: 'responsible_name', sortBy: 'responsible__name'},
        {text: 'Заказчик', value: 'customer_name', sortBy: 'customer__name'},
        {text: 'Статус', value: 'status_name', sortBy: 'status__name'}
      ],
      filters: [
        {
          title: 'Поиск по табелю',
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
          title: 'Ответственный',
          name: 'responsible',
          type: 'select-auto',
          endpoint: '/api/v1/personnel/',
          selectData: []
        },
        {
          title: 'Статус',
          name: 'status',
          type: 'select-auto',
          endpoint: '/api/v1/status_card/',
          selectData: []
        },
        {
          title: 'Поиск по периоду',
          name: 'period',
          value: null,
          type: 'search',
          endpoint: null,
          placeholder: '02.2023',
          validator: periodValidator,
          validateInputCount: 7
        },
      ]
    }
  },
  computed: {
    FundUrl: {
      get() {
        return `/fund`
      }
    },
    ReportCardUrl: {
      get() {
        return `/report_card`
      }
    }
  }
}
</script>
