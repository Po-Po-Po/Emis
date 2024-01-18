<template>
  <card-view
    :id="dataObject.id"
    :endpoint="endpoint"
    :data-object="dataObject"
    min-height="100"
  >
    <template #action>
      <v-btn class="primary" @click="editItem">Сохранить</v-btn>
      <v-btn @click="$emit('close')">Закрыть</v-btn>
    </template>
    <template #card_content>
      <v-card>
        <v-card-text>
          <v-form>
            <v-text-field
              v-model="dataObject.name"
              label="Наименование"
            ></v-text-field>
            <v-text-field
              v-model="dataObject.number"
              label="Номер"
            ></v-text-field>
            <date-picker
              label="Дата выдачи"
              :item="dataObject.date1"
              @update="updateDate1"
            ></date-picker>
            <date-picker
              label="Дата окончания"
              :item="dataObject.date2"
              @update="updateDate2"
            ></date-picker>
            <v-text-field
              v-model="dataObject.cert_center"
              label="Аттестационный центр"
            ></v-text-field>
            <v-file-input id="identity_file" v-model="selectedFile" label="Выберите файл"></v-file-input>
            <a v-if="dataObject.file" :href="dataObject.file" target="_blank">Скачать файл</a>
          </v-form>
        </v-card-text>
      </v-card>
    </template>
  </card-view>
</template>

<script>
import CardView from "~/components/view/CardView";
import DatePicker from "~/components/view/DatePicker";

export default {
  name: "AdditionalIdentityView",
  components: {CardView, DatePicker},
  props: {
    idItem: {
      type: String && Number,
      default: null
    },
    personnelId: {
      type: String,
      default: null
    },
  },
  data() {
    return {
      endpoint: '/api/v1/additional_identity/',
      dataObject: {
        name: null,
        number: null,
        date1: null,
        date2: null,
        cert_center: null,
        file: null,
      },
      selectedFile: null
    }
  },
  async fetch() {
    if (this.idItem) {
      await this.$serverApi.$get(`${this.endpoint}${this.idItem}/`)
        .then((response) => {
          this.dataObject = response
        })
    }
  },
  computed: {
    userId() {
      return this.$auth.user.id
    }
  },
  watch: {
    idItem: {
      handler() {
        if (this.idItem) {
          this.$fetch()
        } else {
          this.dataObject = {}
        }
      },
      deep: true
    }
  },
  methods: {
    createForm() {
      const formData = new FormData();
      Object.keys(this.dataObject).forEach(key => {
        let value = this.dataObject[key]
        if (value && typeof value === 'object') {
          value = JSON.stringify(value)
        }
        formData.append(key, value);
      })
      return formData
    },
    editItem() {
      this.$serverApi.setHeader('Content-Type', 'multipart/form-data')
      if (this.dataObject.id) {
        const form = this.createForm()
        form.append('attachment', this.selectedFile)
        this.$serverApi.$put(`${this.endpoint}${this.dataObject.id}/`, form)
          .then(() => {
            this.$toast.success('Сохранено')
            this.$emit('save')
          })
      } else {
        this.dataObject.personnel = this.personnelId
        const form = this.createForm()
        form.append('attachment', this.selectedFile)
        this.$serverApi.$post(`${this.endpoint}`, form)
          .then(() => {
            this.$toast.success('Создано')
            this.$emit('save')
            this.dataObject = {
              name: null,
              number: null,
              date1: null,
              date2: null,
              cert_center: null,
              file: null,
            }
          })
      }
      this.$serverApi.setHeader('Content-Type', 'application/json')
    },
    updateDate1(value) {
      this.dataObject.date1 = value
    },
    updateDate2(value) {
      this.dataObject.date2 = value
    },
  }
}
</script>
