<template>
  <div>
    <card-view
      :id="routeId"
      :endpoint="endpoint"
      :title="dataObject.name"
      :data-object="dataObject"
      :delete-btn="deleteBtn"
    >
      <template #card_content>
        <v-tabs
          v-model="tab"
        >
          <v-tab href="#tab-main">
            Заказчики
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <v-tab-item id="tab-main">
            <v-card>
              <v-card-text>
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-text-field
                    v-model="dataObject.name"
                    label="ФИО заказчика"
                  ></v-text-field>
                </v-form>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </template>
    </card-view>

  </div>
</template>

<script>
import CardView from "~/components/view/CardView";

export default {
  name: "EquipmentView",
  components: {CardView},
  props: {
    id: {
      type: Number,
      default: null
    },
    deleteBtn: {
      type: Boolean,
      default: true
    },
  },
  data() {
    return {
      dataObject: {
        name: null,
      },
      endpoint: '/api/v1/customer/',
      valid: true,
    }
  },
  async fetch() {
    this.dataObject = await this.$serverApi.$get(`${this.endpoint}${this.routeId}/`)
  },
  computed: {
    routeId: {
      get() {
        if (this.id) {
          return this.id
        }
        return this.$route.params.id
      }
    }
  },
  watch: {
    id() {
      this.$fetch()
    }
  },
  methods: {
  }
}
</script>


