export const state = () => ({
  title: 'EMIS-TEST',
})

export const mutations = {
  loggingIn(state) {
    state.auth.loggedIn = true
    this.$router.push('/')
  },
  setTitle(state, payload) {
    state.title = payload
  }
}
