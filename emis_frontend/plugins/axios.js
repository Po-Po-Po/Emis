export default function ({$axios, store, redirect}, inject) {
    const serverApi = $axios.create()
    serverApi.setBaseURL(store.$config.axios.baseURL)


    serverApi.interceptors.request.use((config) => {
      const token =  localStorage.getItem('auth._token.local')
      const now = new Date().getTime();
      const tokenExpirationTime = new Date(now + 60 * 60 * 24 * 1000)
      localStorage.setItem('tokenExpirationTime', tokenExpirationTime.getTime());
      return {
        ...config,
        headers: { ...config.headers, Authorization: `${token}` }
      }
    })

    const apiList = [
        {
            name: 'serverApi',
            api: serverApi
        }
    ]

    apiList.forEach(item => {
        // item.api.setToken(localStorage.getItem('auth._token.local'))
        item.api.onRequest(request => {
            return request
        })
        item.api.onResponse(response => {
            return response
        })
        item.api.onError(error => {
            const code = parseInt(error.response && error.response.status)
            if (code === 401) {
                store.state.sessionStorage.authUser = null
                return redirect('/login')
            }
            if (code === 400) {
              const keys = Object.keys(error.response.data)
              keys.forEach(key => {
                store.$toast.error(`${key}: ${error.response.data[key]}`)
              })
            }
            if (code > 400) {
              store.$toast.error(error.response.data.detail)
            }
            return error
        })
        inject(item.name, item.api)
    })
}
