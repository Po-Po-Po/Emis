<template>
  <card-view
    :endpoint="endpoint"
    title="History"
    :data-object="dataObject"
    :delete-btn="false"
    :no-edit="true"
    min-height="100"
    @edit="update"
  >
    <template #card_content>
      <v-card>
        <v-card-text>
          <v-form ref="form" lazy-validation>
            <select-api
              :item="dataObject.type"
              endpoint="/api/v1/history_type/"
              label="Тип"
              @update="updateType"
            ></select-api>
            <select-autocomplete
              label="Объект"
              endpoint="/api/v1/entity/"
              :action="false"
              @update="updateEntity"
            >
            </select-autocomplete>
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
import SelectApi from "~/components/view/SelectApi";
import SelectAutocomplete from "@/components/view/SelectAutocomplete";

export default {
  name: "HistoryView",
  components: {CardView, SelectApi, SelectAutocomplete},
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
      endpoint: '/api/v1/history/',
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
    updateType(value) {
      this.dataObject.type = value
    },
    updateEntity(value) {
      this.dataObject.entity = value
    },
    update() {
      const formData = new FormData();
      formData.append('equipment', this.equipmentId);
      formData.append('entity', this.dataObject.entity);
      formData.append('type', this.dataObject.type);
      formData.append('comment', this.dataObject.comment);
      formData.append('file', this.dataObject._file);
      this.$serverApi.setHeader('Content-Type', 'multipart/form-data')
      this.$serverApi.$post(this.endpoint, formData).then(() => {
        this.$emit('update')
      })
      this.$serverApi.setHeader('Content-Type', 'application/json')
    }
  }
}
</script>
