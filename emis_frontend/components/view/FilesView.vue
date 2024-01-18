<template>
  <v-card>
    <v-container>
      <v-row class="align-center">
        <v-col cols="12" md="3">
          <v-text-field v-model="fileName" label="Название файла"></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-file-input v-model="attachment" label="Выберите файл"></v-file-input>
        </v-col>
        <v-col cols="12" md="3">
          <v-select
            v-model="selectedItem"
            :items="models"
            :return-object="true"
            item-text="name"
            item-value="model"
            :disabled="disable"
            label="Раздел для файлов"
          >

          </v-select>
        </v-col>
        <v-col cols="12" md="2">
          <v-btn
            color="primary"
            elevation="2"
            small
            dark
            class="mb-2"
            @click="addAttachment"
          >
            <v-icon>mdi-upload</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
    <v-treeview
      v-model="tree"
      :open="initiallyOpen"
      :items="filesList"
      activatable
      item-key="name"
      open-on-click
    >
      <template #prepend="{ item, open }">
        <v-icon v-if="!item.file">
          {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
        </v-icon>
        <v-icon v-else>
          {{ files[item.file] }}
        </v-icon>
      </template>
      <template #label="{ item }">
        <a v-if="item.file" :href="item.attachments" target="_blank">{{ item.name }}.{{ item.file }}</a>
        <div v-else>
          {{ item.name }}
        </div>
        <v-icon v-if="item.file" @click="deleteAttachment(item.id)">
          mdi-delete
        </v-icon>
      </template>
    </v-treeview>
  </v-card>
</template>

<script>
export default {
  name: "FilesView",
  props: {
    filesList: {
      type: Array,
      default: () => []
    },
    initiallyOpen: {
      type: Array,
      default: () => []
    },
    models: {
      type: Array,
      default: () => []
    },
    objectId: {
      type: String,
      default: null
    },
    disable: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      files: {
        html: 'mdi-language-html5',
        js: 'mdi-nodejs',
        json: 'mdi-code-json',
        md: 'mdi-language-markdown',
        pdf: 'mdi-file-pdf',
        png: 'mdi-file-image',
        txt: 'mdi-file-document-outline',
        xls: 'mdi-file-excel',
      },
      tree: [],
      selected: null,
      attachment: null,
      fileName: null,
      endpoint: '/api/v1/attachment/'
    }
  },
  computed: {
    baseUrl() {
      return this.$config.axios.baseURL
    },
    selectedItem: {
      get(){
        if (!this.selected && this.models.length > 0){
          // eslint-disable-next-line vue/no-side-effects-in-computed-properties
          this.selected = this.models[0]
          return this.models[0]
        } else {
          return this.selected
        }
      },
      set(value){
        this.selected = value
      }
    }
  },
  methods: {
    addAttachment() {
      if (!this.selected) {
        this.$toast.error('Выбирете раздел для файлов')
      } else {
        const formData = new FormData();
        formData.append('attachments', this.attachment);
        formData.append('model', this.selected.model);
        formData.append('id', this.objectId);
        formData.append('filename', this.fileName);
        this.$serverApi.setHeader('Content-Type', 'multipart/form-data')
        this.$serverApi.$post(this.endpoint, formData).then(() => {
          this.$emit('update')
        })
        this.$serverApi.setHeader('Content-Type', 'application/json')
      }
    },
    deleteAttachment(id){
      this.$serverApi.delete(`${this.endpoint}${id}/`).then(() => {
        this.$emit('update')
      })
    }
  }
}
</script>

<style scoped>
#files_view {
  width: auto;
}
</style>
