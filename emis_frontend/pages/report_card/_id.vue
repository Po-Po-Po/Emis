<template>
  <div>
    <card-view
      :id="routeId"
      :endpoint="endpoint"
      :title="dataObject.name"
      :data-object="dataObject"
      :delete-btn="deleteBtn"
      :close-btn="closeBtn"
      @close="closeCard"
      @unclose="uncloseCard"
    >
      <template #action_custom>
        <v-btn :href="`${baseUrl}${endpointPrint}?report_card_id=${routeId}`">
          <v-icon title="Сохранить в xlsx">mdi-file-excel-outline</v-icon>
        </v-btn>
        <v-btn @click="copyReportCard">
          <v-icon title="Копировать табель">mdi-content-copy</v-icon>
        </v-btn>
      </template>
      <template #card_content>
        <v-tabs
          v-model="tab"
        >
          <v-tab href="#tab-main">
            Табель
          </v-tab>
          <v-tab href="#tab-table">
            Таблица
          </v-tab>
          <v-tab href="#tab-files">
            Файлы
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item id="tab-main">
            <v-card>
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-row class="align-center align-md-center justify-start">
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="dataObject.card"
                        v-bind:readonly="disabled"
                        label="Наименование табеля"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <v-text-field
                        v-model="dataObject.period"
                        v-bind:readonly="disabled"
                        label="Период"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" md="4">
                      <select-autocomplete
                        :item="dataObject.entity"
                        endpoint="/api/v1/entity/"
                        label="Объект"
                        :action="false"
                        :is-disabled="disabled"
                        :server-search="true"
                        @update="updateEntityName"
                      ></select-autocomplete>
                    </v-col>
                    <v-col cols="12" md="4">
                      <select-autocomplete
                        :item="dataObject.responsible"
                        endpoint="/api/v1/personnel/"
                        label="Ответственный"
                        :action="false"
                        :is-disabled="disabled"
                        :server-search="true"
                        @update="updatePersonnelName"
                      ></select-autocomplete>
                    </v-col>
                    <v-col cols="12" md="4">
                      <select-autocomplete
                        :item="dataObject.customer"
                        endpoint="/api/v1/personnel/"
                        label="Заказчик"
                        :action="false"
                        :is-disabled="disabled"
                        :server-search="true"
                        @update="updateCustomerName"
                      ></select-autocomplete>
                    </v-col>
                  </v-row>
                  <v-card>
                    <report-card-table
                      v-if="dataObject.period"
                      :is-disabled="disabled"
                      :route-id="routeId"
                      :period="dataObject.period"
                      height="400px"
                      :reload="0"
                    >
                    </report-card-table>
                  </v-card>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>

          <v-tab-item id="tab-table">
            <v-card>
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-card>
                    <table-view
                      :headers="cardTableHeader"
                      :endpoint="`${endpoint_history_table}?report_card=${routeId}`"
                      :count-items="10"
                      :reload="reloadOperation"
                      :actions="true"
                      height="400px"
                    >
                      <template #action_custom="{ item }">
                        <v-icon small @click="printContract(item)">
                          mdi-printer
                        </v-icon>
                      </template>
                    </table-view>
                  </v-card>
                </v-form>
              </v-card-text>
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

  </div>
</template>

<script>
import CardView from "~/components/view/CardView";
import TableView from "~/components/view/TableView";
import FilesView from "~/components/view/FilesView.vue";
import ReportCardTable from "~/components/view/ReportCardTable.vue";
import SelectAutocomplete from "~/components/view/SelectAutocomplete.vue";

export default {
  name: "EquipmentView",
  components: {SelectAutocomplete, FilesView, TableView, CardView, ReportCardTable},
  props: {
    id: {
      type: Number,
      default: null
    },
    deleteBtn: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      cardEntityOpen: false,
      cardEntityId: null,
      dialogOpen: false,
      reloadOperation: false,
      initiallyOpen: ['Файлы'],
      dataObject: {},
      equipmentFileList: [],
      getRole: false,
      closeBtn: null,
      is_active: null,
      disabled: true,
      endpoint: '/api/v1/report_card/',
      endpointPrint: '/print_manager/',
      tab: null,
      valid: true,
      filesList: [],
      PageOptions: ([3, 5, 10, 50, 100, -1]),
      endpointRole: '/api/v1/profile/',
      endpointAttachment: '/api/v1/attachment/',
      endpoint_history_table: '/api/v1/history_table/',
      cardTableHeader: [
        {text: '№', value: 'contract_number', width: 80, sortBy: 'contract_number'},
        {text: 'ФИО', value: 'personnel_name', width: 300, sortBy: 'personnel_name', sortable: false},
        {text: 'Дата рождения', value: 'personnel_birthday', type: 'date', width: 120, format: 'dd.MM.yyyy'},
        {text: 'Дата начала договора', value: 'start_date', type: 'date', width: 120, format: 'dd.MM.yyyy'},
        {text: 'Дата окончания договора', value: 'end_date', type: 'date', width: 120, format: 'dd.MM.yyyy'},
        {text: 'Сумма', value: 'sum', width: 100},
        {text: 'Содержание оказываемых услуг', value: 'position'},
        {text: 'Код ОКЗ', value: 'code', width: 120},
        {text: 'Объект', value: 'entity_name', width: 120},
        {text: 'Заказчик', value: 'customer_name'},
        {text: 'Примечание', value: 'description', sortable: false}
      ],
      fileHeader: [
        {text: 'ФИО', value: 'name'},
        {text: 'Должность', value: 'position'},
        {text: 'Телефон', value: 'phone'},
        {text: 'Почта', value: 'email'},
      ],
      modelsFiles: [
        {
          name: 'Табель',
          model: 'reportcard',
          id: this.routeId
        }
      ]
    }
  },
  async fetch() {
    this.dataObject = await this.$serverApi.$get(`${this.endpoint}${this.routeId}/`).catch(e => {this.$toast.error(e)})
    this.is_active = this.dataObject.is_active
    await this.getFiles()
    await this.getUserRole()
  },
  computed: {
    baseUrl: {
      get() {
        return this.$config.printServerUrl
      }
    },
    routeId: {
      get() {
        if (this.id) {
          return this.id
        }
        return this.$route.params.id
      }
    },
  },
  watch: {
    id() {
      this.$fetch()
    }
  },
  methods: {
    copyReportCard() {
      const data = this.dataObject
      data.card = `${this.dataObject.card} копия`
      this.$serverApi.post(`${this.endpoint}${this.routeId}/clone/`, data)
        .then(response => {
          const path = this.$route.name.split('-id')[0]
          this.$router.push(`/${path}/${response.data.pk}/`)
        })
    },
    closeCard() {
      this.disabled = true
      this.closeBtn = !this.closeBtn
      this.$serverApi.post(`${this.endpoint}${this.routeId}/close_card/`)
    },
    uncloseCard() {
      this.disabled = false
      this.closeBtn = !this.closeBtn
      this.$serverApi.post(`${this.endpoint}${this.routeId}/unclose_card/`)
    },
    updateEntityName(value) {
      this.dataObject.entity = value
    },
    updatePersonnelName(value) {
      this.dataObject.responsible = value
    },
    updateCustomerName(value) {
      this.dataObject.customer = value
    },
    async updateFile() {
      this.filesList = []
      await this.getFiles()
    },
    printContract(item) {
      this.$axios({
        url: `/api/v1/history_tabel/${item.id}/print/`,
        method: "GET",
        responseType: 'blob'
      }).then((response) => {
        const href = URL.createObjectURL(response.data);
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', `Договор ${item.personnel_name}_${item.contract_number}.docx`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(href)
      }).catch(error => this.$toast.error(`${error}: ${error.data}`))
    },
    async getFiles() {
      this.reportCardFileList = await this.$axios
        .$get(`${this.endpointAttachment}?reportcard=${this.routeId}`)
      this.dataObject.files = this.reportCardFileList.map(file => file.id)
      this.filesList.push(
        {
          name: 'Файлы',
          children: this.reportCardFileList
        }
      )
    },
    async getUserRole() {
      const response = await this.$axios.$get(`${this.endpointRole}`)
      this.disabled = !this.is_active
      this.getRole = response.groups.filter(item => item.name == 'Редактор табеля').length > 0
      if (this.getRole) {
        this.closeBtn = this.is_active
      }
    }
  },
  mount() {
  }
}
</script>


