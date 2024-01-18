<template>
  <v-stepper
    v-model="e6"
    vertical
  >
    <v-stepper-step
      :complete="e6 > 1"
      step="1"
    >
      Создать сотрудника
      <small>Summarize if needed</small>
    </v-stepper-step>

    <v-stepper-content step="1">
      <v-card>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="dataObject.name"
              label="ФИО"
            ></v-text-field>
            <v-text-field
              v-model="dataObject.birthday"
              label="Дата рождения"
            ></v-text-field>
            <v-text-field
              v-model="dataObject.position"
              label="Должность"
            ></v-text-field>
            <select-autocomplete
              :item="dataObject.entity"
              endpoint="/api/v1/entity/"
              label="Объект"
              :action="false"
              :server-search="true"
              @update="updateEntityName"
            ></select-autocomplete>
            <select-autocomplete
              :item="dataObject.code"
              endpoint="/api/v1/code/"
              label="Код ОКЗ"
              :action="false"
              @update="updateCodeName"
            ></select-autocomplete>
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
        Создать сотрудника
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
      Квалификация
    </v-stepper-step>
    <v-stepper-content step="2">
      <div v-if="id">
        <identity-tab :personnel-id="id"></identity-tab>
        <additional-identity-tab :personnel-id="id"></additional-identity-tab>
      </div>
      <v-btn
        color="primary"
        @click="e6 = 3"
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
          @update="updateFile"
        ></files-view>
      </v-card>
      <v-btn
        color="success"
        :to="nextUrl"
      >
        Завершить создание объекта
      </v-btn>
    </v-stepper-content>
  </v-stepper>
</template>

<script>
import FilesView from "~/components/view/FilesView";
import SelectAutocomplete from "~/components/view/SelectAutocomplete";
import IdentityTab from "~/components/personnel/IdentityTab";
import AdditionalIdentityTab from "~/components/personnel/AdditionalIdentityTab";
import PhoneInput from "~/components/field/PhoneInput";
import createCardMixin from "~/mixin/card"
import DeportmentView from "~/components/view/DeportmentView";
import SelectApi from "~/components/view/SelectApi.vue";

export default {
  name: "PersonnelNew",
  components: {SelectApi, SelectAutocomplete, IdentityTab, AdditionalIdentityTab, FilesView, PhoneInput, DeportmentView},
  mixins: [createCardMixin],
  data() {
    return {
      closeDialogDeportment: false,
      e6: 1,
      id: null,
      dataObject: {
        name: null,
        birthday: null,
        code: null,
        position: null,
        phone: null,
        phone1: null,
        phone2: null,
        email: null,
        department: null,
        description: null
      },
      idEquipment: null,
      reloadEquipment: false,
      modelsFiles: [
        {
          name: 'Персоннал',
          model: 'personnel',
        }
      ],
      filesList: [],
      initiallyOpen: ['Файлы'],
      endpoint: '/api/v1/personnel/',
      endpointAttachment: '/api/v1/attachment/',
    }
  },
  computed: {
    nextUrl: {
      get() {
        if (this.id) {
          return `/personnel/${this.id}/`
        } else {
          return null
        }
      }
    }
  },
  methods: {
    async getFiles() {
      this.identityFileList = await this.$axios
        .$get(`${this.endpointAttachment}?personnel=${this.id}`)
      this.filesList.push(
        {
          name: 'Файлы',
          children: this.identityFileList
        }
      )
    },
    updateCodeName(value) {
      this.dataObject.code = value
    },
    updateEntityName(value) {
      this.dataObject.entity = value
    },
    updateStatus(value) {
      this.dataObject.status = value
    },
    updateDepartment(value) {
      this.dataObject.department = value
      this.closeDialogDeportment = false
    },
    async updateFile() {
      this.filesList = []
      await this.getFiles()
    },
    close() {
      this.$router.push('/personnel/')
    },
    getNextUrl() {

    }
  }
}
</script>
