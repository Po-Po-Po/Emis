<template>
  <card-view
    :endpoint="endpoint"
    title="ReportCard"
    :data-object="dataObject"
    :delete-btn="false"
    :no-edit="true"
    min-height="100"
    @edit="update"
  >
    <template #card_content>
      <v-skeleton-loader>
        <v-card>
          <v-card-text>
            <v-form ref="form" lazy-validation>
              <v-text-field
                v-model="dataObject.contract_number"
                label="Номер договора"
              ></v-text-field>
              <select-autocomplete
                :item="dataObject.personnel"
                endpoint="/api/v1/personnel/"
                label="ФИО"
                :action="false"
                @update="updatePersonnelName"
              ></select-autocomplete>
              <v-text-field
                v-model="dataObject.salary"
                label="Заработная плата"
                type="number"
                @wheel="disableWheel"
              ></v-text-field>
              <v-btn v-if="shodCalculateButton" class="primary" block @click="calculateFields">Заполнить</v-btn>
              <date-picker
                :item="dataObject.start_date"
                label="Начало работы"
                @update="updateStartDate"
              ></date-picker>
              <date-picker
                :item="dataObject.end_date"
                label="Окончание работы"
                @update="updateEndDate"
              ></date-picker>
              <v-text-field
                v-model="dataObject.salary_work"
                label="Зар. плата за отработанные дни"
                type="number"
                @wheel="disableWheel"
              ></v-text-field>
              <v-text-field
                v-model="dataObject.payment"
                label="Оплата медицинского обследования, проезда"
                type="number"
                @wheel="disableWheel"
              ></v-text-field>
              <v-text-field
                v-model="dataObject.award"
                label="Премия"
                type="number"
                @wheel="disableWheel"
              ></v-text-field>
              <v-text-field
                v-model="dataObject.penalty"
                label="Штраф"
                type="number"
                @wheel="disableWheel"
              ></v-text-field>
              <v-text-field
                v-model="dataObject.accrued"
                label="Начислено"
                type="number"
                @wheel="disableWheel"
              ></v-text-field>
              <v-textarea
                v-model="dataObject.description"
                label="Примечание"
              ></v-textarea>
            </v-form>
          </v-card-text>
        </v-card>
      </v-skeleton-loader>
    </template>
  </card-view>
</template>

<script>
import { IsDayOffAPI } from "isdayoff"
import CardView from "~/components/view/CardView";
import SelectAutocomplete from "@/components/view/SelectAutocomplete";
import DatePicker from "~/components/view/DatePicker.vue";
const api = new IsDayOffAPI();

export default {
  name: "TabelView",
  components: {DatePicker, CardView, SelectAutocomplete},
  props: {
    reportCardId: {
      type: String && Number,
      default: null
    },
    idTabel: {
      type: String && Number,
      default: null
    },
    period: {
      type: String,
      default: null
    },
    serialNumber: {
      type: Number,
      default: 1
    }
  },
  data() {
    return {
      endpoint: '/api/v1/history_tabel/',
      shodCalculateButton: false,
      dataObject: {
        user: null,
        number: null,
        contract_number: null,
        start_date: null,
        salary_work: 0,
        payment: 0,
        award: 0,
        penalty: 0,
        description: '',
        accrued: 0,
        end_date: null,
        salary: 0,
        personnel: null,
        type: null
      }
    }
  },
  fetch() {
    if (this.idTabel !== null) {
      this.$serverApi.$get(`${this.endpoint}${this.idTabel}/`).then(response => {
        this.dataObject = response
      }).catch(e => {this.$toast.error(e)})
    }
  },
  computed: {
  },
  watch: {
    idTabel: {
      async handler() {
        await this.$fetch()
      },
      deep: true
    },
    period() {
      this.actionCalculate()
    },
    dataObject: {
      handler() {
        this.actionCalculate()
      },
      deep: true
    },
  },
  methods: {
    actionCalculate() {
      if (this.period && this.dataObject.start_date && this.dataObject.end_date && this.dataObject.salary > 0){
        this.shodCalculateButton = true
      } else {
        this.shodCalculateButton = false
      }
    },
    async calculateFields() {
      if (this.period && this.dataObject.start_date && this.dataObject.end_date && this.dataObject.salary > 0){
        const period = this.period.split(".", 2)
        const workingDays = await api.month({
          year: parseInt(period[1]),
          month: parseInt(period[0]) - 1
        }).then((response) => response).catch(e => {this.$toast.error(e)})
        let days = 0
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        workingDays.forEach((item) => { if(item === 0){days++} })
        const workingDaysPeriod = await api.period({
          start: this.$dateFns.parse(this.dataObject.start_date, 'dd.MM.yyyy', new Date()),
          end: this.$dateFns.parse(this.dataObject.end_date, 'dd.MM.yyyy', new Date())
        }).then((response) => response).catch(e => {this.$toast.error(e)})
        let daysPeriod = 0
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        workingDaysPeriod.forEach((item) => { if(item === 0){daysPeriod++} })
        this.dataObject.salary_work = (this.dataObject.salary / days) * daysPeriod
        this.dataObject.accrued = parseInt(this.dataObject.salary_work)
          + parseInt(this.dataObject.award) + parseInt(this.dataObject.payment) - parseInt(this.dataObject.penalty)
      } else {
        this.$toast.error('Не заполненно одно из полей: Период, Начало работы, Окончание работы, Заработная плата')
      }
    },
    updateStartDate(value) {
      this.dataObject.start_date = value;
    },
    updateEndDate(value) {
      this.dataObject.end_date = value;
    },
    updatePersonnelName(value) {
      this.dataObject.personnel = value;
    },
    disableWheel(event) {
      event.preventDefault();
    },
    update() {
      const formData = new FormData();
      formData.append('number', this.serialNumber);
      formData.append('contract_number', this.dataObject.contract_number);
      formData.append('start_date', this.dataObject.start_date);
      formData.append('end_date', this.dataObject.end_date);
      formData.append('salary', this.dataObject.salary);
      formData.append('salary_work', this.dataObject.salary_work);
      formData.append('payment', this.dataObject.payment);
      formData.append('personnel', this.dataObject.personnel);
      formData.append('award', this.dataObject.award);
      formData.append('penalty', this.dataObject.penalty)
      formData.append('accrued', this.dataObject.accrued);
      formData.append('description', this.dataObject.description);
      formData.append('report_card', this.reportCardId);
      this.$serverApi.setHeader('Content-Type', 'multipart/form-data')
      if (this.idTabel === null){
        this.$serverApi.$post(this.endpoint, formData).then(() => {
        }).catch(e => {this.$toast.error(e)})
      } else {
        this.$serverApi.$put(`${this.endpoint}${this.idTabel}/`, formData).then(() => {
        }).catch(e => {this.$toast.error(e)})
      }
      this.$fetch()
      this.$emit('update')
      this.$serverApi.setHeader('Content-Type', 'application/json')
    }
  },
}
</script>
