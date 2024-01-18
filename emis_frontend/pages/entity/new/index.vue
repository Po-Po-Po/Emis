<template>
  <v-stepper
    v-model="e6"
    vertical
  >
    <v-stepper-step
      :complete="e6 > 1"
      step="1"
    >
      Создание объекта
    </v-stepper-step>

    <v-stepper-content step="1">
      <v-card>
        <v-card-text>
          <v-form ref="form" lazy-validation>
            <v-text-field
              v-model="dataObject.name"
              label="Наименование"
              dense
            ></v-text-field>
            <v-text-field
              v-model="dataObject.directorate"
              label="Дирекция"
              dense
            ></v-text-field>
            <v-text-field
              v-model="dataObject.contractor"
              label="Заказчик"
              dense
            ></v-text-field>
            <v-text-field
              v-model="dataObject.director_lnk"
              label="Руководитель ЛНК"
              dense
            ></v-text-field>
            <v-text-field
              v-model="dataObject.address"
              label="Адрес"
              dense
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
        Создать объект
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
      Выбрать сотрудников
    </v-stepper-step>
    <v-stepper-content step="2">
      <sub-division-tab
        :entity-id="id"
      ></sub-division-tab>
      <v-btn
        color="primary"
        @click="e6 = 3"
      >
        Далее
      </v-btn>
    </v-stepper-content>

    <v-stepper-step
      :complete="e6 > 3"
      step="3"
    >
      Выбрать оборудование
    </v-stepper-step>

    <v-stepper-content step="3">
      <equipment-tab
        v-if="id"
        :entity-id="id"
        :data-object="dataObject"
        :endpoint-entity="endpoint"
        @update="updateEquipment"
      ></equipment-tab>
      <v-btn
        color="primary"
        @click="e6 = 4"
      >
        Далее
      </v-btn>
    </v-stepper-content>

    <v-stepper-step step="4">
      Загрузить файлы
    </v-stepper-step>
    <v-stepper-content step="4">
      <v-card>
        <files-view
          :files-list="filesList"
          :initially-open="initiallyOpen"
          :models="modelsFiles"
          :object-id="id"
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
import EquipmentTab from "~/components/entity/EquipmentTab";
import SubDivisionTab from "~/components/entity/SubDivisionTab";
import createCardMixin from "~/mixin/card"

export default {
  name: "EntityNew",
  components: {
    SubDivisionTab,
    FilesView,
    EquipmentTab
  },
  mixins: [createCardMixin],
  data() {
    return {
      e6: 1,
      step: {
        1: false,
        2: false,
        3: false,
        4: false
      },
      id: null,
      dataObject: {
        name: null,
        directorate: null,
        contractor: null,
        director_lnk: null,
        address: null,
        description: null
      },
      idEquipment: null,
      reloadEquipment: false,
      modelsFiles: [
        {
          name: 'Объект',
          model: 'entity',
        }
      ],
      filesList: [],
      initiallyOpen: ['Файлы'],
      endpoint: '/api/v1/entity/',
      endpointAttachment: '/api/v1/attachment/',
    }
  },
  computed: {
    nextUrl: {
      get() {
        if (this.id) {
          return `/entity/${this.id}/`
        }
        return '/'
      }
    }
  },
  methods: {
    async getFiles() {
      this.identityFileList = await this.$axios
        .$get(`${this.endpointAttachment}?entity=${this.id}`)
      this.filesList.push(
        {
          name: 'Файлы',
          children: this.identityFileList
        }
      )
    },
    updateEquipment(value) {
      this.dataObject.equipment = value
    },
    async updateFile() {
      this.filesList = []
      await this.getFiles()
    },
    close() {
      this.$router.push('/entity/')
    },
    getNextUrl() {

    }
  }
}
</script>


