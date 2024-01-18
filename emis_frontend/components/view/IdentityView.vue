<template>
  <card-view
    :id="dataObject.id"
    :endpoint="endpoint"
    :data-object="dataObject"
    min-height="100"
  >
    <template #action>
      <small v-if="changed" class="align-center error--text" style="padding-right: 10px;">Yдостоверение изменено,
        сохраните его</small>

      <v-btn class="primary" @click="editItem">Сохранить</v-btn>
      <v-btn @click="$emit('close')">Закрыть</v-btn>
    </template>
    <template #card_content>


      <v-container>
        <v-row class="align-top">
          <v-col cols="12" md="4">
            <v-card>
              <v-card-text>
                <v-form>
                  <v-text-field
                    v-model="dataObject.number"
                    label="Номер"
                  ></v-text-field>
                  <date-picker
                    label="Дата окончания поверки"
                    :item="dataObject.date_of_issue"
                    @update="updateDateOfIssue"
                  ></date-picker>
                  <v-text-field
                    v-model="dataObject.level"
                    label="Уровень"
                  ></v-text-field>
                  <v-text-field
                    v-model="dataObject.cert_center"
                    label="Аттестационный центр"
                  ></v-text-field>
                  <v-file-input id="identity_file" v-model="selectedFile" label="Выберите файл"></v-file-input>
                  <a v-if="dataObject.file" :href="dataObject.file" target="_blank">Скачать файл</a>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="8">
            <v-container>
              <v-row class="align-center" justify="space-around">
                <v-col cols="12" md="3">
                  <v-text-field
                    v-model="item.row1"
                    label="Вид контроля"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="4">
                  <date-picker
                    :item="item.row2"
                    label="Дата окончания"
                    @update="updateRow2"
                  ></date-picker>
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="item.row3"
                    label="Объекты контроля"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" md="1">
                  <v-btn
                    color="primary"
                    elevation="2"
                    small
                    dark
                    class="mb-2"
                    @click="addItem"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-container>
            <v-data-table
              dense
              :headers="header"
              :items="itemsList"
              :items-per-page="10"
              class="elevation-1"
              height="251px"
            >
              <template #item.action="{ item }">
                <v-icon small @click="deleteItem(item)">
                  mdi-delete
                </v-icon>
              </template>
              <template #[`item.${field}`]="props" v-for="field in ['row1', 'row2', 'row3']">
                <v-edit-dialog
                  :return-value="props.item[field]"
                  :key="field"
                  save-text="Сохранить"
                  cancel-text="Отмена"
                  large
                >
                  <div v-if="field === 'row2'">
                    {{ dateReturn(props.item[field]) }}
                  </div>
                  <div v-else> {{ props.item[field] }} </div>
                  <template #input>
                    <v-text-field
                      v-if="field !== 'row2'"
                      v-model="props.item[field]"
                      label="Edit"
                      single-line
                    ></v-text-field>
                    <date-picker
                      v-else
                      :item="props.item[field]"
                      label="Дата окончания"
                      @update="props.item[field] = $event"
                    ></date-picker>
                  </template>
                </v-edit-dialog>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </card-view>
</template>

<script>
import CardView from "~/components/view/CardView";
import DatePicker from "~/components/view/DatePicker";

export default {
  name: "IdentityView",
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
      endpoint: '/api/v1/identity/',
      changed: false,
      dataObject: {
        user: null,
        number: null,
        date_of_issue: null,
        control: null,
        cert_center: null,
        file: null,
      },
      itemsList: [],
      deleteList: [],
      item: {
        row1: null,
        row2: null,
        row3: null,
      },
      header: [
        {text: 'Вид контроля', value: 'row1'},
        {text: 'Дата окончания', value: 'row2', type: 'date'},
        {text: 'Объекты контроля', value: 'row3'},
        {
          text: 'Действие',
          value: 'action',
          type: 'action',
          sortable: false,
          align: 'center',
          width: 100
        }
      ],
      selectedFile: null
    }
  },
  async fetch() {
    this.itemsList = []
    this.dataObject = {}
    if (this.idItem) {
      await this.$serverApi.$get(`${this.endpoint}${this.idItem}/`)
        .then((response) => {
          this.dataObject = response
          this.itemsList = response.control
        })
    }
  },
  computed: {
    userId() {
      return this.$auth.user.id
    },
  },
  watch: {
    idItem: {
      handler() {
        if (this.idItem) {
          this.$fetch()
        } else {
          this.dataObject = {}
          this.itemsList = []
        }
      },
      deep: true
    },
    itemsList: {
      handler(_, oldValue) {
        if (oldValue.length > 0){
          this.changed = true
        }
      },
      deep: true
    }
  },
  methods: {
    update() {

    },
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
        this.dataObject.control = this.itemsList
        const form = this.createForm()
        form.append('attachment', this.selectedFile)
        this.$serverApi.$post(`${this.endpoint}`, form)
          .then(() => {
            this.$toast.success('Создано')
            this.$emit('save')
            if (!this.idItem) {
              this.dataObject = {
                user: null,
                number: null,
                date_of_issue: null,
                control: null,
                cert_center: null,
                file: null,
              }
              this.itemsList = []
            }
          })
      }
      if (this.deleteList.length > 0) {
        this.deleteList.forEach(item => {
          if (item.id) {
            this.$serverApi.$delete(`/api/v1/type_control/${item.id}/`)
          }
        })
        this.deleteList = []
      }
      this.changed = false
      this.$serverApi.setHeader('Content-Type', 'application/json')
    },
    updateDateOfIssue(value) {
      this.dataObject.date_of_issue = value
    },
    updateRow2(value) {
      this.item.row2 = value
    },
    addItem() {
      const valid = []
      Object.keys(this.item).forEach(key => {
        if (this.item[key] !== null) {
          valid.push(key)
        } else {
          this.$toast.error(`Поле ${key} не заполненно`)
        }
      })
      if (valid.length === 3) {
        this.itemsList.push(this.item)
        this.dataObject.control = this.itemsList
        this.item = {
          row1: null,
          row2: null,
          row3: null
        }
      }
      this.changed = true

    },
    deleteItem(value) {
      this.deleteList.push(value)
      this.itemsList = this.itemsList.filter(item => item !== value)
      this.dataObject.control = this.itemsList
      this.changed = true
    },
    dateReturn(value) {
        return value
    }
  }
}
</script>
