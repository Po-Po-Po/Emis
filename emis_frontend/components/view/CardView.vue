<template>
  <v-card :min-height="minHeight" light>
    <v-card-actions class="align-end">
      <v-spacer></v-spacer>
      <slot name="action_custom"></slot>
      <slot name="action">
        <v-btn class="primary" @click="editDataObject">Сохранить</v-btn>
        <v-btn v-if="deleteBtn" class="error" @click="dialog = true">Удалить</v-btn>
      </slot>
      <slot>
        <template v-if="closeBtn != null">
          <v-btn v-if="closeBtn" class="close" @click="closeDataObject">Закрыть</v-btn>
          <v-btn v-else class="edit" @click="uncloseDataObject">Редактировать</v-btn>
        </template>
      </slot>
    </v-card-actions>
    <v-card-text>
      <slot name="card_content">
      </slot>
    </v-card-text>
    <v-dialog
      v-model="dialog"
      persistent
      max-width="290"
    >

      <v-card>
        <v-card-title class="text-h5">
          Удалить?
        </v-card-title>
        <v-card-text>
          {{ dataObject.name }}
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="error darken-1"
            text
            @click="dialog = false"
          >
            Нет
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="deleteDataObject"
          >
            Да
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import {mapMutations} from 'vuex'

export default {
  name: "CardView",
  props: {
    id: {
      type: String && Number,
      default: null
    },
    endpoint: {
      type: String,
      default: ''
    },
    title: {
      type: String,
      default: 'EMIS'
    },
    dataObject: {
      type: Object,
      default: () => {
      }
    },
    deleteBtn: {
      type: Boolean,
      default: true
    },
    closeBtn: {
      type: Boolean,
      default: null
    },
    noEdit: {
      type: Boolean,
      default: false
    },
    minHeight: {
      type: String,
      default: "calc(100vh - 95px)"
    }
  },
  data() {
    return {
      message: 'Message text',
      errorObject: [],
      dialog: false
    }
  },
  watch: {
    title: {
      handler() {
        this.setTitle(this.title)
      },
      deep: true,
    },
  },
  mounted() {

  },
  methods: {
    ...mapMutations({
      setTitle: 'setTitle',
    }),
    getId() {
      if (this.id) {
        return this.id
      } else {
        return this.$route.params.id
      }
    },
    editDataObject() {
      if (!this.noEdit) {
        this.$serverApi.$put(`${this.endpoint}${this.getId()}/`, this.dataObject)
          .then(() => {
            this.$toast.success('Сохранено')
          })
      } else {
        this.$emit('edit')
      }
    },
    closeDataObject() {
      this.$emit('close')
    },
    uncloseDataObject() {
      this.$emit('unclose')
    },
    deleteDataObject() {
      this.dialog = false
      if (!this.noEdit) {
        const url = this.$route.path.replace(`/${this.getId()}/`, '')
        this.$serverApi.$delete(`${this.endpoint}${this.getId()}/`)
          .then(() => {
            this.$router.push(url)
          })
      } else {
        this.$emit('delete')
      }
    }
  }
}
</script>

<style>
.edit-button {
  display: flex;
  flex-wrap: wrap;
}
</style>
