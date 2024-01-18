<template>
  <table-view
    :endpoint="endpoint"
    :headers="headers"
    :menu-row="true"
    :actions="false"
    :toolbar="true"
    :click-row="true"
    create-url="/equipment/new"
    height="calc(100vh - 260px)"
    :filters="filters"
  >
  </table-view>
</template>
<script>
import TableView from "@/components/view/TableView";
import title from "~/mixin/main";

export default {
  auth: true,
  name: 'Equipment',
  components: {TableView},
  mixins: [title],
  data() {
    return {
      endpoint: '/api/v1/equipment/',
      title: 'Оборудование',
      headers: [
        {
          text: 'Тип',
          align: 'start',
          sortable: true,
          value: 'type_name',
          sortBy: 'type'
        },
        {text: 'Наименование', value: 'name'},
        {text: 'Номер', value: 'factory_number'},
        {text: 'Обьект', value: 'entity', type: 'array', showField: 'name', sortBy: 'entity__name'},
        {text: 'Метрология', value: 'validity', type: 'date'},
        {text: 'Статус', value: 'status'},
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
          title: 'Тип',
          name: 'type',
          type: 'select',
          endpoint: '/api/v1/equipment_type/',
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
          title: 'Статус',
          name: 'status',
          type: 'select',
          endpoint: '/api/v1/equipment_status/',
          selectData: []
        },
        {
          title: 'Период окончания поверки',
          name: 'validity',
          type: 'date-range',
          selectData: [],
          value: [],
        },
      ]
    }
  },
}
</script>
