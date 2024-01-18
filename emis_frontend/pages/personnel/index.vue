<template>
  <table-view
    :endpoint="endpoint"
    :headers="headers"
    :xlsx-button="true"
    :menu-row="true"
    :actions="false"
    :toolbar="true"
    :click-row="true"
    create-url="/personnel/new"
    height="calc(100vh - 260px)"
    :filters="filters"
  >
  </table-view>
</template>
<script>
import TableView from "~/components/view/TableView";
import title from "~/mixin/main";

export default {
  auth: true,
  name: 'Personnel',
  components: {TableView},
  mixins: [title],
  data() {
    return {
      endpoint: '/api/v1/personnel/',
      title: 'Персонал',
      headers: [
        {
          text: 'ФИО',
          align: 'start',
          sortable: true,
          value: 'name',
        },
        {text: 'Дата рождения', value: 'birthday'},
        {text: 'Должность', value: 'position'},
        {text: 'Объект', value: 'entity_name', sortBy: 'entity__name'},
        {text: 'Отдел', value: 'department_name', sortBy: 'department__name'},
        {text: 'Телефон', value: 'phone', type: 'phone', width: '150'},
        {text: 'Статус', value: 'status'},
        {text: 'Почта', value: 'email'}
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
          title: 'Отдел',
          name: 'department',
          type: 'select',
          endpoint: '/api/v1/department/',
          selectData: []
        },
        {
          title: 'Объект',
          name: 'entity',
          type: 'select-auto',
          endpoint: '/api/v1/entity/',
          selectData: []
        },
      ]
    }
  },
}
</script>
