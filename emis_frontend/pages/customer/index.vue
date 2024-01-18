<template>
  <table-view
    :endpoint="endpoint"
    :headers="headers"
    :menu-row="true"
    :actions="false"
    :toolbar="true"
    :click-row="true"
    create-url="/customer/new"
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
  name: 'Сustomer',
  components: {TableView},
  mixins: [title],
  data() {
    return {
      endpoint: '/api/v1/customer/',
      title: 'Заказчик',
      headers: [
        {
          text: 'ФИО',
          align: 'card',
          sortable: true,
          value: 'name',
        }
      ],
      filters: [
        {
          title: 'Поиск по заказчику',
          name: 'search',
          value: null,
          type: 'input',
          endpoint: null,
          selectData: []
        },
      ]
    }
  },
}
</script>
