<template>
  <div>
    <card-view
      :id="`${routeId}`"
      :endpoint="endpoint"
      :title="`${dataObject.name} (${dataObject.factory_number})`"
      :data-object="dataObject"
      :delete-btn="deleteBtn"
    >
      <template #action_custom>
        <v-btn @click="copyEquipment">
          <v-icon title="Копировать оборудование">mdi-content-copy</v-icon>
        </v-btn>
      </template>
      <template #card_content>
        <v-tabs
          v-model="tab"
        >
          <v-tab href="#tab-main">
            Основное
          </v-tab>
          <v-tab href="#tab-metrology">
            Метрология
          </v-tab>
          <v-tab href="#tab-operational">
            Операционный учет
          </v-tab>
          <v-tab href="#tab-files">
            Файлы
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item id="tab-main">
            <v-card height="calc(80vh - 70px)" class="overflow-auto">
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <select-api
                    :item="dataObject.type"
                    endpoint="/api/v1/equipment_type/"
                    label="Тип"
                    @update="updateType"
                  ></select-api>
                  <v-text-field
                    v-model="dataObject.name"
                    label="Наименование"
                  ></v-text-field>
                  <select-autocomplete
                      label="Отдел"
                      endpoint="/api/v1/department/"
                      :server-search="true"
                      :no-filter="true"
                      :item="dataObject.department"
                      :close-dialog="closeDialogDeportment"
                      @update="updateDepartment"
                  >
                  </select-autocomplete>
                  <v-text-field
                    v-model="dataObject.factory_number"
                    label="Заводской номер"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.inventory_number"
                    label="Инвентарный номер"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.purpose"
                    label="Назначение"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.year_of_manufacture"
                    label="Год изготовления"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.manufacture"
                    label="Изготовитель"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.owner"
                    label="Владелец"
                  ></v-text-field>
                  <h3 v-if="!id">Список объектов:</h3>
                  <v-list v-if="!id">
                    <v-list-item-group
                      color="primary"
                    >
                      <v-list-item v-for="entity in dataObject.entity" :key="entity.id" @click="openEntity(entity.id)">
                        <v-list-item-icon>
                          <v-icon v-text="`mdi-office-building-cog-outline`"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title v-text="entity.name"></v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                  <textarea-field
                    label="Важная информация"
                    :value="dataObject.description"
                    @update="dataObject.description = $event"
                  ></textarea-field>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item id="tab-metrology">
            <v-card>
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <select-api
                    :item="dataObject.status"
                    endpoint="/api/v1/equipment_status/"
                    label="Статус"
                    @update="updateStatus"
                  ></select-api>
                  <v-text-field
                    v-model="dataObject.place_of_verification"
                    label="Место проведения поверки"
                  ></v-text-field>
                  <date-picker
                    label="Дата поверки"
                    :item="dataObject.date_of_verification"
                    @update="updateDateOfVerification"
                  ></date-picker>
                  <date-picker
                    label="Дата окончания поверки"
                    :item="dataObject.validity"
                    @update="updateValidity"
                  ></date-picker>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item id="tab-operational">
            <v-btn
              color="primary"
              elevation="2"
              small
              dark
              class="mb-2"
              @click="dialogOpen=true"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
            <v-card>
              <table-view
                :headers="historyHeader"
                :endpoint="`${endpointHistory}?equipment=${routeId}`"
                :count-items="10"
                :reload="reloadOperation"
                height="400px"
              >
              </table-view>
            </v-card>
          </v-tab-item>
          <v-tab-item id="tab-files">
            <v-card>
              <files-view
                :files-list="filesList"
                :initially-open="initiallyOpen"
                :models="modelsFiles"
                :object-id="routeId"
                :disable="true"
                @update="updateFile"
              ></files-view>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </template>
    </card-view>
    <v-dialog
      v-model="dialogOpen"
      max-width="490"
    >
      <history-view
        :equipment-id="routeId"
        @update="updateOperation"
      ></history-view>
    </v-dialog>
    <v-dialog
      v-model="cardEntityOpen"
      max-width="calc(70%)"
    >
      <entity-view :id="cardEntityId" :delete-btn="false"></entity-view>
    </v-dialog>
  </div>
</template>

<script>
import CardView from "~/components/view/CardView";
import TableView from "~/components/view/TableView";
import FilesView from "~/components/view/FilesView";
import SelectApi from "~/components/view/SelectApi";
import DatePicker from "~/components/view/DatePicker";
import HistoryView from "~/components/view/HistoryView";
import EntityView from "~/pages/entity/_id";
import SelectAutocomplete from "~/components/view/SelectAutocomplete.vue";

export default {
  name: "EquipmentView",
  components: {
    SelectAutocomplete,
    EntityView, HistoryView, DatePicker, FilesView, TableView, CardView, SelectApi},
  props: {
    id: {
      type: Number,
      default: null
    },
    deleteBtn: {
      type: Boolean,
      default: true
    },
  },
  data() {
    return {
      cardEntityOpen: false,
      cardEntityId: null,
      dialogOpen: false,
      closeDialogDeportment: false,
      reloadOperation: 0,
      initiallyOpen: ['Файлы'],
      dataObject: {},
      equipmentFileList: [],
      endpoint: '/api/v1/equipment/',
      tab: null,
      valid: true,
      filesList: [],
      PageOptions: ([3, 5, 10, 50, 100, -1]),
      endpointAttachment: '/api/v1/attachment/',
      endpointHistory: '/api/v1/history/',
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
      fileHeader: [
        {text: 'ФИО', value: 'name'},
        {text: 'Должность', value: 'position'},
        {text: 'Телефон', value: 'phone'},
        {text: 'Почта', value: 'email'},
      ],
      modelsFiles: [
        {
          name: 'Оборудование',
          model: 'equipment',
        }
      ]
    }
  },
  async fetch() {
    this.dataObject = await this.$serverApi.$get(`${this.endpoint}${this.routeId}/`)
    await this.getFiles()
  },
  computed: {
    routeId: {
      get() {
        if (this.id) {
          return this.id
        }
        return this.$route.params.id
      }
    }
  },
  watch: {
    id() {
      this.$fetch()
    }
  },
  methods: {
    openEntity(id) {
      this.cardEntityId = id
      this.cardEntityOpen = true
    },
    async updateFile() {
      this.filesList = []
      await this.getFiles()
    },
    updateType(value) {
      this.dataObject.type = value
    },
    updateDepartment(value) {
      this.dataObject.department = value
      this.closeDialogDeportment = false
    },
    updateStatus(value) {
      this.dataObject.status = value
    },
    updateDateOfVerification(value) {
      this.dataObject.date_of_verification = value
    },
    updateValidity(value) {
      this.dataObject.validity = value
    },
    updateOperation() {
      this.reloadOperation += 1
      this.dialogOpen = false
    },
    copyEquipment() {
      const data = this.dataObject
      data.name = `${this.dataObject.name} копия`
      this.$serverApi.post(`${this.endpoint}${this.routeId}/clone/`, data)
        .then(response => {
          const path = this.$route.name.split('-id')[0]
          this.$router.push(`/${path}/${response.data.pk}/`)
        })
    },
    async getFiles() {
      this.equipmentFileList = await this.$axios
        .$get(`${this.endpointAttachment}?equipment=${this.routeId}`)
      this.dataObject.files = this.equipmentFileList.map(file => file.id)
      this.filesList.push(
        {
          name: 'Файлы',
          children: this.equipmentFileList
        }
      )
    }
  }
}
</script>


