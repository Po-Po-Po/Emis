<template>
  <v-card>
    <v-card-actions>
      <v-row class="align-center align-md-center justify-start">
        <v-col cols="12" md="1">
          <v-btn
            color="primary"
            elevation="2"
            small
            dark
            class="mb-2"
            @click="open()"
          >
            <v-icon>mdi-plus</v-icon>
          </v-btn>
        </v-col>
        <v-col cols="cols" md="1">
          <v-btn v-if="selected.length > 0" class="error" @click="deleteSelected">Удалить выбранное</v-btn>
        </v-col>
      </v-row>
    </v-card-actions>
    <v-card-title>
      Дополнительные удостоверения
    </v-card-title>
    <table-view
      :endpoint="`${endpoint}?personnel=${personnelId}`"
      :headers="header"
      :count-items="-1"
      height="calc(100%-10px)"
      :reload="reload"
      :click-row="clickRow"
      :show-select="true"
      :close-card="dialogClose"
      @select="selectItem"
    >
      <template #deleteButton>
        <v-btn class="error" @click="deleteSelected">Удалить выбранное</v-btn>
      </template>
      <template #card="row">
        <additional-identity-view
          :id-item="row.id"
          :personnel-id="personnelId"
          @save="closeDialog"
          @close="closeDialog"
        ></additional-identity-view>
      </template>
    </table-view>
    <v-dialog
      v-model="dialogOpen"
      max-width="490"
    >
      <additional-identity-view
        :id-item="idOpenItem"
        :personnel-id="personnelId"
        @save="closeDialog"
        @close="closeDialog"
      >

      </additional-identity-view>
    </v-dialog>
  </v-card>
</template>

<script>
import TableView from "~/components/view/TableView";
import AdditionalIdentityView from "~/components/view/AdditionalIdentityView";

export default {
  name: "AdditionalIdentity",
  components: {AdditionalIdentityView, TableView},
  props: {
    endpoint: {
      type: String,
      default: '/api/v1/additional_identity/'
    },
    personnelId: {
      type: String || Number,
      default: null
    }
  },
  data() {
    return {
      clickRow: true,
      dialogClose: false,
      selected: [],
      header: [
        {text: 'Наименование', value: 'name'},
        {text: 'Номер', value: 'number'},
        {text: 'Дата выдачи', value: 'date1', type: 'date'},
        {text: 'Дата окончания', value: 'date2', type: 'date'},
        {text: 'Аттестационный центр', value: 'cert_center'},
        {text: 'Документ', value: 'file', type: 'file', align: 'center', width: 50, sortable: false,},
      ],
      dialogOpen: false,
      idOpenItem: null,
      reload: false,
    }
  },
  methods: {
    selectItem(value) {
      this.selected = value
    },
    open(id) {
      if (id) {
        this.idOpenItem = id
      } else {
        this.idOpenItem = null
      }
      this.reload = false
      this.dialogOpen = true
    },
    closeDialog(){
      this.reload = true
      this.dialogOpen = false
      if (this.dialogClose){
        setTimeout(() => {
          this.dialogClose = false
          this.reload = false
        }, 10)
      }
      setTimeout(() => {
        this.dialogClose = true
        this.reload = true
      }, 10)
    },
    delete(id) {
      // eslint-disable-next-line no-return-assign
      this.$serverApi.$delete(`${this.endpoint}${id}/`).then(() => {})
    },
    deleteSelected() {
      this.reload = false
      this.selected.forEach(item => {
        this.delete(item.id)
      })
      this.selected = []
      setTimeout(() => {
        this.reload = true
      }, 10)
    }
  }
}
</script>
