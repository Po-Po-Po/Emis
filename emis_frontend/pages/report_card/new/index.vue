<template>
  <v-stepper
    v-model="e6"
    vertical
  >
    <v-stepper-step
      :complete="e6 > 1"
      step="1"
    >
      Создать табель
    </v-stepper-step>

    <v-stepper-content step="1">
      <v-card>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="dataObject.card"
              label="Наименование табеля"
            ></v-text-field>
            <v-text-field
              v-model="dataObject.period"
              label="Период"
              placeholder="04.2023"
            ></v-text-field>
            <select-autocomplete
              :item="dataObject.entity"
              endpoint="/api/v1/entity/"
              label="Объект"
              :action="false"
              @update="updateEntityName"
            ></select-autocomplete>
            <select-autocomplete
              :item="dataObject.responsible"
              endpoint="/api/v1/personnel/"
              label="Ответственный"
              :action="false"
              @update="updatePersonnelName"
            ></select-autocomplete>
            <select-autocomplete
              :item="dataObject.customer"
              endpoint="/api/v1/personnel/"
              label="Заказчик"
              :action="false"
              @update="updateCustomerName"
            ></select-autocomplete>
          </v-form>
        </v-card-text>
      </v-card>

      <v-btn
        color="success"
        @click="sendingRequest"
      >
        Создать
      </v-btn>
      <v-btn
        @click="close"
      >
        Отмена
      </v-btn>
    </v-stepper-content>
  </v-stepper>
</template>

<script>
import SelectAutocomplete from "~/components/view/SelectAutocomplete.vue";

export default {
  name: "ReportCardNew",
  components: {SelectAutocomplete},
  mixins: [],
  data() {
    return {
      closeDialogDeportment: false,
      e6: 1,
      id: null,
      dataObject: {
        card: null,
        period: null,
        entity: null,
        personnel: null,
        customer: null
      },
      endpoint: '/api/v1/report_card/',
    }
  },
  computed: {
  },
  methods: {
    updateEntityName(value) {
      this.dataObject.entity = value
    },
    updatePersonnelName(value) {
      this.dataObject.responsible = value
    },
    updateCustomerName(value) {
      this.dataObject.customer = value
    },
    sendingRequest() {


      const arrD = this.dataObject.period.split(".");
      if (arrD.length !== 2) {
        this.$toast.error("Период вводится в формате %m.%YYYY")
        return
      }
      arrD[0] -= 1;
      const d = new Date(arrD[1], arrD[0], 1);
      if (d.toString() === 'Invalid Date') {
        this.$toast.error("Период введен некорректно")
        return
      }
      if (this.dataObject.period && this.dataObject.entity && this.dataObject.responsible && this.dataObject.customer) {
        this.$serverApi.$post(`${this.endpoint}`, this.dataObject).then((response) => {
          this.dataObject = response
        }).then(() => {
          this.$router.push('/report_card/')
        }).catch(e => {this.$toast.error(e)})
      }
    },
    close() {
      this.$router.push('/report_card/')
    }
  }
}
</script>
