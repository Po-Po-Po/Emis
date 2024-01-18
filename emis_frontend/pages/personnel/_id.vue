<template>
  <div>
    <card-view
      :id="routeId"
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
          <v-tab href="#tab-skill">
            Квалификация
          </v-tab>
          <v-tab href="#tab-files">
            Файлы
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item id="tab-main">
            <v-card height="calc(80vh - 70px)" class="overflow-auto">
              <v-card-text>
                <v-form ref="form">
                  <v-text-field
                    v-model="dataObject.name"
                    label="ФИО"
                  ></v-text-field>
                  <date-picker
                    :item="dataObject.birthday"
                    label="Дата рождения"
                    @update="updateBirthday"
                  ></date-picker>
                  <v-text-field
                    v-model="dataObject.position"
                    label="Должность"
                  ></v-text-field>
                  <select-autocomplete
                    endpoint="/api/v1/code/"
                    label="Код ОКЗ"
                    :server-search="true"
                    :no-filter="true"
                    :action="true"
                    :item="dataObject.code"
                    :close-dialog="closeDialogCode"
                    @update="updateCodeName"
                  >
                    <template #default="item">
                      <code-o-k-z-view
                        :id="item.id"
                        @update="closeDialogCode = true"
                        @close="updateCodeName"
                      ></code-o-k-z-view>
                    </template>
                  </select-autocomplete>
                  <select-api
                      :item="dataObject.status"
                      endpoint="/api/v1/personnel_status/"
                      label="Статус"
                      @update="updateStatus"
                  ></select-api>
                  <phone-input
                    :item-value="dataObject.phone"
                    label="Телефон"
                    @update="dataObject.phone = $event"
                  ></phone-input>
                  <phone-input
                    :item-value="dataObject.phone1"
                    label="Доп. телефон 1"
                    @update="dataObject.phone1 = $event"
                  ></phone-input>
                  <phone-input
                    :item-value="dataObject.phone2"
                    label="Доп. телефон 2"
                    @update="dataObject.phone2 = $event"
                  ></phone-input>
                  <v-text-field
                    v-model="dataObject.email"
                    label="Электронная почта:"
                  ></v-text-field>
                  <select-autocomplete
                    label="Отдел"
                    endpoint="/api/v1/department/"
                    :server-search="true"
                    :no-filter="true"
                    :action="true"
                    :item="dataObject.department"
                    :close-dialog="closeDialogDeportment"
                    @update="updateDepartment"
                  >
                    <template #default="item">
                      <deportment-view
                        :id="item.id"
                        @update="closeDialogDeportment = true"
                        @close="updateDepartment"
                      ></deportment-view>
                    </template>
                  </select-autocomplete>
                  <p></p>
                  <h3 v-if="!id">Объект:</h3>
                  <v-list v-if="!id">
                    <v-list-item-group
                      color="primary"
                    >
                      <v-list-item>
                        <v-list-item-icon>
                          <v-icon v-text="`mdi-office-building-cog-outline`"></v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                          <v-list-item-title v-text="dataObject.entity_name"></v-list-item-title>
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
          <v-tab-item id="tab-skill">
            <identity-tab :personnel-id="`${routeId}`"></identity-tab>
            <additional-identity-tab :personnel-id="`${routeId}`"></additional-identity-tab>
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
      v-model="cardEntityOpen"
      max-width="calc(70%)"
    >
      <entity-view :id="cardEntityId" :delete-btn="false"></entity-view>
    </v-dialog>
  </div>
</template>

<script>
import CardView from "@/components/view/CardView";
import FilesView from "~/components/view/FilesView";
import SelectAutocomplete from "~/components/view/SelectAutocomplete";
import IdentityTab from "~/components/personnel/IdentityTab";
import AdditionalIdentityTab from "~/components/personnel/AdditionalIdentityTab";
import PhoneInput from "~/components/field/PhoneInput";
import DeportmentView from "~/components/view/DeportmentView";
import EntityView from "~/pages/entity/_id";
import CodeOKZView from "~/components/view/CodeOKZVue.vue";
import DatePicker from "~/components/view/DatePicker.vue";
import SelectApi from "~/components/view/SelectApi.vue";

export default {
  name: "PersonnelView",
  components: {
    SelectApi,
    DatePicker,
    CodeOKZView,
    EntityView,
    DeportmentView, PhoneInput, AdditionalIdentityTab, IdentityTab, FilesView, CardView, SelectAutocomplete},
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
      closeDialogDeportment: false,
      closeDialogCode: false,
      initiallyOpen: ['Файлы'],
      loading: false,
      dataObject: {
        code_name: null
      },
      departmentList: [],
      additionalIdentityFileList: [],
      identityFileList: [],
      personnelFileList: [],
      endpoint: '/api/v1/personnel/',
      tab: null,
      valid: true,
      filesList: [],
      PageOptions: ([3, 5, 10, 50, 100, -1]),
      endpointAttachment: '/api/v1/attachment/',
      endpointDepartment: '/api/v1/department/',
      fileHeader: [
        {text: 'ФИО', value: 'name'},
        {text: 'Должность', value: 'position'},
        {text: 'Телефон', value: 'phone'},
        {text: 'Почта', value: 'email'},
      ],
      modelsFiles: [
        {
          name: 'Персонал',
          model: 'personnel',
          id: this.routeId
        },
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
    updateCodeName(value) {
      this.dataObject.code = value
      this.closeDialogCode = false
    },
    updateStatus(value) {
      this.dataObject.status = value
    },
    async getDepartment() {
      this.loading = true
      this.departmentList = await this.$serverApi.$get(`${this.endpointDepartment}`)
      this.loading = false
    },
    async getFiles() {
      this.filesList = []
      this.personnelFileList = []
      this.additionalIdentityFileList = []
      this.identityFileList = []

      this.identityFileList = await this.$axios
        .$get(`${this.endpointAttachment}?personnel=${this.routeId}&identity=true`)

      this.filesList.push(
        {
          name: 'Файлы',
          children: this.identityFileList
        }
      )

      this.additionalIdentityFileList = await this.$axios
        .$get(`${this.endpointAttachment}?personnel=${this.routeId}&additional_identity=true`)

      this.filesList.push(
        {
          name: 'Файлы дополнительные',
          children: this.additionalIdentityFileList
        }
      )

      await this.getDepartment()

      this.personnelFileList = await this.$serverApi.$get(`${this.endpointAttachment}?personnel=${this.routeId}`)
      this.filesList.push(
        {
          name: 'Прочие файлы',
          children: this.personnelFileList
        }
      )
    },
    async updateFile() {
      this.filesList = []
      await this.getFiles()
    },
    updateDepartment(value) {
      this.dataObject.department = value
      this.closeDialogDeportment = false
    },
    updateBirthday(value) {
      this.dataObject.birthday = value
    }
  },
}
</script>


