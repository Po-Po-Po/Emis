const cardCreateMixin = {
  methods: {
    create() {
      this.$serverApi.$post(this.endpoint, this.dataObject).then((response) => {
        this.dataObject = response
        this.id = `${response.id}`
        this.e6 = 2
      }).catch(error => {
        if (error.response) {
          if (error.response.status === 400) {
            const keys = Object.keys(error.response.data)
            keys.forEach(key => {
              this.$toast.error(`${key}: ${error.response.data[key]}`)
            })
          }
        } else {
          this.$toast.error(error)
        }
      })
    },
  }
}

export default cardCreateMixin
