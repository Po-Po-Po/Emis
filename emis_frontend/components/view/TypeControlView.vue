<template>
  <card-view
    :endpoint="endpoint"
    title="History"
    :data-object="dataObject"
    :delete-btn="false"
    :no-edit="true"
    @edit="update"
  >
    <template #card_content>
      <v-card>
        <v-card-text>
          <v-form ref="form" lazy-validation>
            <v-textarea
              v-model="dataObject.comment"
              outlined
              name="input-7-4"
              label="Комментарий"
            ></v-textarea>
            <v-file-input v-model="dataObject._file" label="Выберите файл"></v-file-input>
          </v-form>
        </v-card-text>
      </v-card>
    </template>
  </card-view>
</template>

<script>
import CardView from "~/components/view/CardView";

export default {
  name: "TypeControlView",
  components: {CardView},
  props: {
    id: {
      type: String,
      default: null
    },
    equipmentId: {
      type: String,
      default: null
    },
  },
  data() {
    return {
      endpoint: '/api/v1/identity/',
      dataObject: {
        user: null,
        equipment: null,
        entity: null,
        type: null,
        comment: null,
        _file: null,
      }
    }
  },
  async fetch() {
    if (this.id) {
      this.dataObject = await this.$serverApi.$get(`${this.endpoint}${this.id}/`)
    }
  },
  computed: {
    userId() {
      return this.$auth.user.id
    }
  },
  methods: {
    update() {

    }
  }
}
</script>
