<template>
  <div>
    <card-view
      :endpoint="endpoint"
      :title="dataObject.name"
      :data-object="dataObject"
      :delete-btn="deleteBtn"
    >
      <template #card_content>
        <v-tabs
          v-model="tab"
        >
          <v-tab href="#tab-main">
            Основное
          </v-tab>
          <v-tab href="#tab-personnel">
            Персонал
          </v-tab>
          <v-tab href="#tab-equipment">
            Оборудование
          </v-tab>
          <v-tab href="#tab-files">
            Файлы
          </v-tab>
          <v-tab href="#tab-history">
            История
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item id="tab-main">
            <v-card height="calc(80vh - 80px)" class="overflow-auto">
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-text-field
                    v-model="dataObject.name"
                    label="Наименование"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.directorate"
                    label="Дирекция"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.contractor"
                    label="Заказчик"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.director_lnk"
                    label="Руководитель ЛНК"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.address"
                    label="Адрес"
                  ></v-text-field>
                  <textarea-field
                    label="Важная информация"
                    :value="dataObject.description"
                    @update="dataObject.description = $event"
                  ></textarea-field>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item id="tab-personnel">
            <sub-division-tab
              :entity-id="routeId"
            ></sub-division-tab>
          </v-tab-item>
          <v-tab-item id="tab-equipment">
            <equipment-tab
              :entity-id="routeId"
              :data-object="dataObject"
              :endpoint-entity="endpoint"
              @update="updateEquipment"
            ></equipment-tab>
          </v-tab-item>
          <v-tab-item id="tab-files">
            <v-card>
              <files-view
                :files-list="filesList"
                :initially-open="initiallyOpen"
                :models="modelsFiles"
                :object-id="routeId"
                @update="updateFile"
              ></files-view>
            </v-card>
          </v-tab-item>
          <v-tab-item id="tab-history">
            <v-card>
              <table-view
                :headers="historyHeader"
                :endpoint="`${endpoint_history}?entity=${routeId}`"
                :count-items="10"
                height="400px"
              >
              </table-view>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </template>
    </card-view>
  </div>
</template>

<script>
import CardView from "~/components/view/CardView";
import TableView from "~/components/view/TableView";
import FilesView from "~/components/view/FilesView";
import EquipmentTab from "~/components/entity/EquipmentTab";
import SubDivisionTab from "~/components/entity/SubDivisionTab";

export default {
  name: "EntityView",
  components: {
    EquipmentTab,
    SubDivisionTab,
    TableView,
    CardView,
    FilesView
  },
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
      initiallyOpen: ['Файлы'],
      dataObject: {},
      endpoint: '/api/v1/entity/',
      tab: null,
      valid: true,
      subdivisionList: [],
      equipmentList: [],
      filesList: [],
      historyList: [],
      PageOptions: ([3, 5, 10, 50, 100, -1]),
      endpoint_subdivision: '/api/v1/subdivision/',
      endpoint_equipment: '/api/v1/equipment/',
      endpoint_history: '/api/v1/history/',
      endpointAttachment: '/api/v1/attachment/',
      equipmentHeader: [
        {text: 'Тип', value: 'type_name'},
        {text: 'Наименование', value: 'name'},
        {text: 'Заводской номер', value: 'factory_number'},
        {text: 'Инвентарный номер', value: 'inventory_number'},
        {text: 'Метрология', value: 'purpose'},
        {
          text: 'Действие',
          value: 'action',
          type: 'action',
          sortable: false,
          align: 'center',
          width: 100
        }
      ],
      historyHeader: [
        {text: 'Дата', value: 'created_on', type: 'date', width: 150, format: 'HH:MM; dd.MM.yyyy', sourceFormat: 'dd.MM.yyyy HH:mm'},
        {text: 'Ответственный', value: 'user_name', width: 200},
        {text: 'Операция', value: 'type_name'},
        {text: 'Оборудование', value: 'equipment_name'},
        {text: 'Объект', value: 'entity_name'},
        {text: 'Информация', value: 'comment'},
        {
          text: 'Документ',
          value: 'file',
          type: 'file',
          sortable: false,
        },
      ],
      subdivisionHeader: [
        {text: 'ФИО', value: 'name'},
        {text: 'Должность', value: 'position'},
        {text: 'Телефон', value: 'phone'},
        {text: 'Почта', value: 'email'},
        {
          text: 'Действие',
          value: 'action',
          type: 'action',
          sortable: false,
          align: 'center',
          width: 100
        }
      ],
      subdivisionType: [
        {name: 'Руководитель подразделения ЛНК', id: '1'},
        {name: 'Состав подразделения ЛНК', id: '2'},
        {name: 'Персонал взаимодействия', id: '3'},
      ],
      idSubdivisionType: null,
      idPersonnel: [],
      idEquipment: null,
      reloadEquipment: false,
      modelsFiles: [
        {
          name: 'Объект',
          model: 'entity',
          id: this.routeId
        }
      ]
    }
  },
  async fetch() {
    await this.$serverApi.$get(`${this.endpoint}${this.routeId}/`)
      .then((response) => {
        this.dataObject = response
      })
    await this.getFiles()
  },
  computed: {
    routeId: {
      get() {
        if (this.id) {
          return `${this.id}`
        }
        return this.$route.params.id
      }
    }
  },
  methods: {
    searchInString(queryText, itemText) {
      return itemText.toLocaleLowerCase().includes(queryText.toLocaleLowerCase())
    },
    updateEquipment(value) {
      this.dataObject.equipment = value
    },
    async getFiles() {
      this.identityFileList = await this.$axios
        .$get(`${this.endpointAttachment}?entity=${this.routeId}`)
      this.dataObject.files = this.identityFileList.map(file => file.id)
      this.filesList.push(
        {
          name: 'Файлы',
          children: this.identityFileList
        }
      )
    },
    updateIdSubdivisionType(value) {
      this.idSubdivisionType = value
    },
    updateIdPersonnel(value) {
      this.idPersonnel.push(value)
    },
    async updateFile() {
      this.filesList = []
      await this.getFiles()
    },
    addPersonnelToSubdivision() {
      if (this.idSubdivisionType && this.idPersonnel) {
        const subDivision = this.subdivisionList.filter((item) => {
          return item.type === this.idSubdivisionType ? item : null
        })
        const personnelSelected = [...subDivision[0].personnel, ...this.idPersonnel]
        const subDivisionId = subDivision[0].id
        const data = {
          type: this.idSubdivisionType,
          entity: this.routeId,
          personnel: personnelSelected
        }
        this.$serverApi.$put(`/api/v1/subdivision/${subDivisionId}/`, data)
          .then(() => {
            this.idPersonnel = []
            this.$fetch()
            this.$toast.success(`Пользователь добавлен в подразделение: ${subDivision[0].type_name}`)
          })
      }
    },
    deletePersonnelToEntity(personnelId, subdivisionId) {
      this.subdivisionList.forEach(item => {
        if (item.id === subdivisionId) {
          item.personnel = item.personnel.filter(item => item !== personnelId)
          item.personnel_list = item.personnel_list.filter(item => item.id !== personnelId)
          this.$serverApi.$patch(`/api/v1/subdivision/${subdivisionId}/`, {personnel: item.personnel})
          this.$toast.success(`Пользователь удален из подразделения: ${item.type_name}`)
        }
      })
    },
    editData() {
      this.$serverApi.$put(`${this.endpoint}/${this.routeId}/`, this.dataObject)
      return true
    },
    createSubDivisions() {
      const typeSubDivision = [1, 2, 3]
      typeSubDivision.forEach(idx => {
        const dataPut = {
          "type": idx,
          "entity": this.routeId
        }
        this.$serverApi.$post('/api/v1/subdivision/', dataPut)
          .then(() => {
            this.$fetch()
          })
          .catch(() => {

          })
      })
    },
  },
}
</script>


