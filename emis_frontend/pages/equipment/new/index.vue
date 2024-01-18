<template>
  <v-stepper
    v-model="e6"
    vertical
  >
    <v-stepper-step
      :complete="e6 > 1"
      step="1"
    >
      Создать оборудование
      <small>Основное</small>
    </v-stepper-step>

    <v-stepper-content step="1">
      <v-card>
        <v-card-text>
          <v-form ref="form" lazy-validation>
            <select-api
              :item="dataObject.type"
              endpoint="/api/v1/equipment_type/"
              label="Тип"
              @update="updateType"
            ></select-api>
            <select-autocomplete
              :item="dataObject.entity"
              endpoint="/api/v1/entity/"
              label="Объект"
              :action="false"
              :server-search="true"
              @update="updateEntityName"
            ></select-autocomplete>
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
              v-model="dataObject.name"
              label="Наименование"
            ></v-text-field>
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
            <textarea-field
              label="Важная информация"
              :value="dataObject.description"
              @update="dataObject.description = $event"
            ></textarea-field>
          </v-form>
        </v-card-text>
      </v-card>
      <v-btn
        color="primary"
        @click="create"
      >
        Создать оборудование
      </v-btn>
      <v-btn
        @click="close"
      >
        Отмена
      </v-btn>
    </v-stepper-content>

    <v-stepper-step
      :complete="e6 > 2"
      step="2"
    >
      Метрология
    </v-stepper-step>
    <v-stepper-content step="2">
      <v-card>
        <v-card-text>
          <v-form ref="form" lazy-validation>
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
      <v-btn
        color="primary"
        @click="update"
      >
        Далее
      </v-btn>
    </v-stepper-content>


    <v-stepper-step step="3">
      Загрузить файлы
    </v-stepper-step>
    <v-stepper-content step="3">
      <v-card>
        <files-view
          :files-list="filesList"
          :initially-open="initiallyOpen"
          :models="modelsFiles"
          :disable="true"
          :object-id="id"
          @update="updateFile"
        ></files-view>
      </v-card>
      <v-btn
        color="success"
        :to="nextUrl"
      >
        Завершить создание оборудования
      </v-btn>
    </v-stepper-content>
  </v-stepper>
</template>

<script>
import SelectApi from "~/components/view/SelectApi";
import DatePicker from "~/components/view/DatePicker";
import FilesView from "~/components/view/FilesView";
import createCardMixin from "~/mixin/card"
import SelectAutocomplete from "~/components/view/SelectAutocomplete.vue";

export default {
  name: "EquipmentNew",
  components: {SelectAutocomplete, SelectApi, DatePicker, FilesView},
  mixins: [createCardMixin],
  data() {
    return {
      e6: 1,
      id: null,
      dataObject: {
        type: null,
        name: null,
        closeDialogDeportment: false,
        factory_number: null,
        inventory_number: null,
        purpose: null,
        year_of_manufacture: null,
        manufacture: null,
        owner: null,
        status: null,
        place_of_verification: null,
        date_of_verification: null,
        validity: null,
        description: null,
      },
      idEquipment: null,
      reloadEquipment: false,
      modelsFiles: [
        {
          name: 'Оборудование',
          model: 'equipment',
        }
      ],
      filesList: [],
      initiallyOpen: ['Файлы'],
      endpoint: '/api/v1/equipment/',
      endpointAttachment: '/api/v1/attachment/',
    }
  },
  computed: {
    nextUrl: {
      get() {
        if (this.id) {
          return `/equipment/${this.id}/`
        } else {
          return null
        }
      }
    }
  },
  methods: {
    update() {
      this.$serverApi.$patch(`${this.endpoint}${this.id}/`, this.dataObject).then((response) => {
        this.dataObject = response
        this.id = `${response.id}`
        this.e6 = 3
      })
    },

    async getFiles() {
      this.identityFileList = await this.$axios
        .$get(`${this.endpointAttachment}?equipment=${this.id}`)
      this.filesList.push(
        {
          name: 'Файлы',
          children: this.identityFileList
        }
      )
    },
    updateType(value) {
      this.dataObject.type = value
    },
    updateDepartment(value) {
      this.dataObject.department = value
      this.closeDialogDeportment = false
    },
    updateEntityName(value) {
      this.dataObject.entity = value
    },
    async updateFile() {
      this.filesList = []
      await this.getFiles()
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
    close() {
      this.$router.push('/equipment/')
    }
  }
}
</script>
