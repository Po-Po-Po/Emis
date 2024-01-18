const title = {
  created() {
    let title = this.title
    if (!this.title) {
      title = this.$store.state.title
    }
    this.$store.commit('setTitle', title)
  },
}


export default title

