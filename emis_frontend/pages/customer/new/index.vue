<template>
  <v-stepper
    v-model="e6"
    vertical
  >
    <v-stepper-step
      :complete="e6 > 1"
      step="1"
    >
      Создать заказчика
    </v-stepper-step>

    <v-stepper-content step="1">
      <v-card>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="dataObject.name"
              label="ФИО заказчика"
            ></v-text-field>
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

export default {
  name: "CustomerNew",
  components: {},
  mixins: [],
  data() {
    return {
      closeDialogDeportment: false,
      e6: 1,
      id: null,
      dataObject: {
        name: null
      },
      endpoint: '/api/v1/customer/',
    }
  },
  computed: {
  },
  methods: {
    sendingRequest() {
      if (this.dataObject.name) {
        this.$serverApi.$post(`${this.endpoint}`, this.dataObject).then((response) => {
          this.dataObject = response
        })
        this.$router.push('/customer/')
      }
    },
    close() {
      this.$router.push('/customer/')
    }
  }
}
</script>
