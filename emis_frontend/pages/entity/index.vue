<template>
  <table-view
    :endpoint="endpoint"
    :menu-row="true"
    :headers="headers"
    :actions="false"
    :toolbar="true"
    :click-row="true"
    create-url="/entity/new"
    height="calc(100vh - 260px)"
    :filters="filters"
  >
  </table-view>
</template>
<script>
import TableView from "@/components/view/TableView";
import title from "~/mixin/main";

export default {
  name: 'Entity',
  components: {TableView},
  mixins: [title],
  auth: true,
  data() {
    return {
      endpoint: '/api/v1/entity/',
      title: 'Объекты',
      headers: [
        {
          text: 'Наименование',
          align: 'start',
          sortable: true,
          value: 'name',
        },
        {text: 'Дирекция', value: 'directorate'},
        {text: 'Руководитель ЛНК', value: 'director_lnk'},
        {text: 'Адрес', value: 'address', sortable: false},
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
          title: 'Дирекция',
          name: 'directorate',
          type: 'select-auto',
          endpoint: '/api/v1/directorate/',
          selectData: []
        },
      ]
    }
  },
}
</script>
