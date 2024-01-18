<template>
  <card-view
    :id="id"
    :endpoint="endpoint"
    title="Отдел"
    :data-object="dataObject"
    :delete-btn="false"
    :no-edit="true"
    min-height="100"
    @edit="update"
  >
    <template #card_content>
      <v-card>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="dataObject.name"
              label="Название отдела"
            ></v-text-field>
          </v-form>
        </v-card-text>
      </v-card>
    </template>
  </card-view>
</template>

<script>
import CardView from "./CardView";

export default {
  name: "DeportmentView",
  components: {CardView},
  props: {
    id: {
      type: Number,
      default: null
    },
  },
  data() {
    return {
      endpoint: '/api/v1/department/',
      dataObject: {
        name: null,
      }
    }
  },
  async fetch() {
    if (this.id) {
      this.dataObject = await this.$serverApi.$get(`${this.endpoint}${this.id}/`)
    } else {
      this.dataObject = {
        name: null
      }
    }
  },
  computed: {
    userId() {
      return this.$auth.user.id
    }
  },
  updated() {
    this.$fetch()
  },
  methods: {
    updateType(value) {
      this.dataObject.type = value
    },
    closeDialog(value) {
      this.$emit('update', value)
      setTimeout(() => {
        this.$emit('close', value)
      }, 100)
    },
    update() {
      if (this.id) {
        this.$serverApi.$put(`${this.endpoint}${this.id}/`, this.dataObject).then(() => {
          this.closeDialog()
        })
      } else {
        this.$serverApi.$post(this.endpoint, this.dataObject).then((response) => {
          this.closeDialog(response.id)
        })
      }
    }
  }
}
</script>
