<template>
  <div>
    <v-btn
      color="primary"
      :disabled="isDisabled"
      elevation="2"
      small
      dark
      class="mb-2"
      @click="dialogOpen=true"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-btn
      v-show="showDeleteButton"
      :disabled="isDisabled"
      color="error"
      elevation="2"
      small
      dark
      class="mb-2"
      @click="deleteSelectedItem()"
    >
      <v-icon>mdi-delete</v-icon>
    </v-btn>
    <v-card>
      <v-data-table
        v-model="selected"
        dense
        :headers="addHeader"
        :items="resultData"
        class="elevation-1"
        :height="height"
        :show-select="true"
      >
        <template #item="{ item }">
          <tr>
            <td class="checkbox"><v-checkbox dense @change="selectedItem($event, item.id)"></v-checkbox></td>
            <td v-for="header in headers" :key="header.value" class="text-start period" @click="actionClickRow(item.id)">
              <div v-if="item[header.value] === 'Р'" :key="item.value" :class="header.rowClass">
                {{ item[header.value] }}
              </div>
              <div v-else-if="item[header.value] === 'H'" :key="item.value" class="default">
                {{ item[header.value] }}
              </div>
              <div v-else-if="item[header.value] === 'В'" :key="item.value" class="v">
                {{ item[header.value] }}
              </div>
              <div v-else-if="header.type === 'date'" :key="header.name">
                {{ item[header.value] | dateFormater(header.format) }}
              </div>
              <div v-else :key="item.value" class="none">
                {{ item[header.value] }}
              </div>
            </td>
          </tr>
        </template>
      </v-data-table>
    </v-card>
    <v-dialog
      v-if="!isDisabled"
      v-model="dialogOpen"
      max-width="490"
    >
        <tabel-view
          ref="tabelViewRef"
          :key="serialNumber"
          :report-card-id="routeId"
          :id-tabel="idTabel"
          :period="period"
          :serial-number="serialNumber"
          @update="updateOperation"
        ></tabel-view>
    </v-dialog>
  </div>
</template>

<script>
import { IsDayOffAPI } from "isdayoff"
import TabelView from "~/components/view/TabelView.vue";
import { convertDateFormat } from '@/utils'
import dateFormater from "~/filters/dateFormater";
const api = new IsDayOffAPI();

export default {
  name: "ReportCardTableView",
  components: {TabelView},
  filters: {
    dateFormater
  },
  props: {
    height: {
      type: String,
      default: '700px'
    },
    routeId: {
      type: String,
      default: null
    },
    isDisabled: {
      type: Boolean,
      default: false
    },
    period: {
      type: String,
      default: null
    },
    reload: {
      type: Number,
      default: 0
    },
  },
  data() {
    return {
      resultData: [],
      calendar: {},
      idTabel: null,
      serialNumber: 1,
      dialogOpen: false,
      showDeleteButton: false,
      url: null,
      endpoint: '/api/v1/history_tabel/',
      selected: [],
      headers: [
        {text: '№ п/п', value: 'number', width: 80, sortBy: 'number', sortable: false},
        {text: 'Фамилия, Имя, Отчество', value: 'personnel_name', width: 300, sortBy: 'personnel_name', sortable: false},
        {text: 'Профессия (должность)', value: 'position', sortable: false, width: 200},
        {text: 'Заработная плата', value: 'salary', sortable: false},
        {text: 'Отработано дней', value: 'work_day', sortBy: 'work_day', sortable: false},
        {text: 'Начало работ', value: 'start_date', type: 'date', width: 120, sortable: false},
        {text: 'Окончание работ', value: 'end_date', type: 'date', width: 120, sortable: false},
        {text: 'Заработная плата за отработанные дни', value: 'salary_work', sortable: false},
        {text: 'Оплата медицинского обследования, проезда', value: 'payment', sortable: false},
        {text: 'Премия', value: 'award', sortable: false},
        {text: 'Штраф', value: 'penalty', sortable: false},
        {text: 'Начислено', value: 'accrued', sortable: false}
      ],
    }
  },
  async fetch() {
    // ToDo refactory, this temp code
    this.resultData = []

    const period = this.period.split(".", 2)
    const calendar = await api.month({
      year: parseInt(period[1]),
      month: parseInt(period[0]) - 1
    }).then((response) => response).catch(e => {this.$toast.error(e)})

    calendar.forEach((item, i) => {
      this.calendar = {...{[i+1]: item}, ...this.calendar}
    })

    await this.$serverApi.$get(this.baseUrl + this.endpoint + '?report_card=' + this.routeId).then(response => {
      const period = this.period.split(".", 2)
      const days = new Date(period[1], period[0], 0).getDate()

      if (response.results.length > 0) {
        this.serialNumber = response.results.length + 1
      }
      let report_card_number = 1
      response.results.forEach(value => {
        const startDate = convertDateFormat(value.start_date, 'dd.MM.yyyy', 'yyyy-MM-dd')
        const endDate = convertDateFormat(value.end_date, 'dd.MM.yyyy', 'yyyy-MM-dd')

        for (let i = 1; i < days + 1; i++) {
          const date = `${period[1]}-${period[0]}-${i}`
          const keyDate = `${i}.${period[0]}.${period[1]}`
          if (this.calendar[i] === 1){
            value[keyDate] = 'В'
          } else if (this.$moment(date).isBetween(startDate, endDate, null, '[]')) {
            value[keyDate] = 'Р'
          } else {
            value[keyDate] = 'H'
          }
        }
        value.number = report_card_number
        report_card_number += 1
        this.resultData.push(value)
      })
    }).catch(e => {
      this.$toast.error(e)
    })
  },
  computed: {
    baseUrl() {
      return this.$config.axios.baseURL
    },
    addHeader: {
      get() {
        const dateArr = String(this.period).split(".", 2)
        if (dateArr.length >= 2) {
          const days = new Date(dateArr[1], dateArr[0], 0).getDate()
          for (let i = 1; i < days + 1; i++) {
            const date = `${i}.${dateArr[0]}.${dateArr[1]}`
            // eslint-disable-next-line vue/no-side-effects-in-computed-properties
            this.headers.splice(3 + i, 0, {
              text: date,
              value: date,
              width: 1,
              sortable: false,
              class: 'orientation',
              rowClass: 'test'
            })
          }
        }
        return this.headers
      }
    }
  },
  watch: {
    dialogOpen: {
      handler(value) {

        if (value === false) {
          this.idTabel = null
        }
      }
    },
    reload: {
      handler(value) {
        if (value) {
          setTimeout(() => {
            this.$fetch()
          }, '1000')
        }
      },
      deep: true
    },
    selected: {
      handler(value) {
        if (value.length > 0){
          this.showDeleteButton = true
        } else {
          this.showDeleteButton = false
        }
      },
      deep: true
    }
  },
  methods: {
    actionClickRow(id) {
      this.idTabel = id
      this.dialogOpen = true
    },
    updateOperation() {
      this.reload += 1
      this.dialogOpen = false
    },
    selectedItem(event, id) {
      if (event) {
        this.selected.push(id)
      } else {
        this.selected = this.selected.filter(item => item !== id)
      }
    },
    async deleteSelectedItem() {
      await this.selected.forEach(id => {
        this.$serverApi.$delete(`${this.endpoint}${id}/`).then(response => {
          this.$fetch()
        }).catch(e => {this.$toast.error(e)})
      })
      this.$toast.success('Удалено')
    }
  }
}
</script>
<style>
  .orientation {
    padding: 0;
  }
  .orientation span {
    writing-mode: vertical-rl;
    text-orientation: revert;
    max-width: 5px;
  }
  td.text-start{
    max-width: 5px;
  }
  td.period {
    padding: 0 !important;
  }
  td.text-start .default{
    background-color: #a8a8a8;
    color: white;
    text-align: center;
  }
  td.text-start .test {
    background-color: #009fff;
    text-align: center;
    padding: 0 !important;
    color: white;
  }
  td.text-start .v {
    background-color: #a8a8a8;
    color: white;
    text-align: center;
    padding: 0 !important;
  }
  td.text-start .none{
    padding: 0 15px;
  }
  .checkbox * *{
    height: 0;
  }
</style>

