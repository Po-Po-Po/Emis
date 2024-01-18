<template>
    <v-card :min-height="minHeight" light>
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
      :endpoint="`${endpoint}`"
      :headers="headers"
      :menu-row="true"
      :actions="false"
      :toolbar="true"
      :add-button="false"
      :click-row="true"
      height="calc(100vh - 260px)"
      :filters="filters"
      card-url="/report_card/"
      id-item="id_report_card"
      :print-button="true"
      :print-server-url="`${baseUrl}${endpointPrint}`"
      print-server-url-params="print=true"
      print-file-name="fund_table.xlsx"
    >
    </table-view>
    </v-card>
</template>
<script>
import TableView from "~/components/view/TableView";
import title from "~/mixin/main";
import { periodValidator } from "@/utils";
import dateFormater from "~/filters/dateFormater";

export default {
  auth: true,
  name: 'Fund',
  components: {TableView},
  filters: {
    dateFormater
  },
  mixins: [title],
  data() {
    return {
      tab: null,
      endpointPrint: '/api/v1/fund/',
      endpoint: '/api/v1/fund/',
      title: 'Фонд',
      headers: [
        {text: '№', value: 'contract_number', width: 90},
        {text: 'ФИО', align: 'name', sortable: true, sortBy: 'name', value: 'name'},
        {text: 'Дата рождения', value: 'birthday', type: 'date', format: 'dd.MM.yyyy'},
        {text: 'Дата начала договора', value: 'start_date', sortBy: 'start_date', type: 'date', format: 'dd.MM.yyyy'},
        {text: 'Дата окончания договора', value: 'end_date', sortBy: 'end_date', type: 'date', format: 'dd.MM.yyyy'},
        {text: 'Сумма', value: 'sum', type: 'sum'},
        {text: 'Содержание оказываемых услуг', value: 'service_provide'},
        {text: 'Код ОКЗ', value: 'code_name'},
        {text: 'Объект', value: 'entity_name', width: 150},
        {text: 'Заказчик', value: 'customer_name', width: 150},
        {text: 'Примечание', value: 'description'}
      ],
      filters: [
        {
          title: 'Поиск по ФИО',
          name: 'search',
          value: null,
          type: 'search',
          endpoint: '/api/v1/fund/',
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
          title: 'Код ОКЗ',
          name: 'code',
          type: 'select-auto',
          endpoint: '/api/v1/code/',
          selectData: []
        },
        {
          title: 'Заказчик',
          name: 'customer',
          type: 'select-auto',
          endpoint: '/api/v1/personnel/',
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
    baseUrl: {
      get() {
        return this.$config.printServerUrl
      }
    },
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
  },
  methods: {
      printXls() {
        alert('Функция в разработке')
      },
      print() {
        alert('Функция в разработке')
      }
  }
}
</script>
