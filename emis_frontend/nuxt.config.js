import colors from 'vuetify/es5/util/colors'
import ru from 'vuetify/lib/locale/ru'

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  publicRuntimeConfig: {
    printServerUrl: process.env.PUBLIC_API_URL || 'http://localhost:8000',
    permission: {
      "all": ['/', '/login'],
      "Персонал": ['/report_card', '/fund', '/personnel', '/control'],
      "Обьекты": ['/entity'],
      "Оборудование": ['/equipment'],
      "Администратор": ['/']
    },
    axios: {
      baseURL: process.env.PUBLIC_API_URL || 'http://localhost:8000',
      proxyHeaders: false,
      credentials: false
    },
  },
  ssr: false,
  server: {
    host: '0.0.0.0',
    port: '3000'
  },

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - emis-frontend',
    title: 'emis-frontend',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1'},
      {hid: 'description', name: 'description', content: ''},
      {name: 'format-detection', content: 'telephone=no'}
    ],
    link: [
      {rel: 'icon', type: 'image/x-icon', href: '/favicon.ico'}
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    '@/assets/css/main.sass'
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '@/plugins/phone-input',
    '@/plugins/component-registry',
    '@/plugins/axios'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/stylelint
    '@nuxtjs/stylelint-module',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
    '@nuxtjs/date-fns',
    '@nuxtjs/moment'
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/dotenv',
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/toast'
  ],

  toast: {
    position: 'bottom-right',
    duration: 5000,
    fullWidth: false,
    register: [ // Register custom toasts
      {
        name: 'my-error',
        message: 'Oops...Something went wrong',
        options: {
          type: 'error'
        }
      }
    ]
  },

  router: {
    middleware: ['auth', 'permission']
  },

  auth: {
    strategies: {
      local: {
        scheme: 'refresh',
        token: {
          property: 'access',
          required: true,
          maxAge: 1800,
          type: 'Bearer',
          global: true,
        },
        user: {
          property: false,
          autoFetch: true
        },
        refreshToken: {
          property: 'refresh',
          data: 'refresh',
          maxAge: 60 * 60 * 24
        },
        endpoints: {
          login: {url: '/api/login/', method: 'post'},
          refresh: {url: '/api/login/refresh/', method: 'post'},
          user: {url: '/api/v1/profile/', method: 'get'},
          logout: {url: '/api/logout/', method: 'post'},
        },
        tokenRequired: true,
        autoLogout: true
      }
    },
    watchLoggedIn: true,
    redirect: {
      login: '/login',
      logout: '/',
      callback: false,
      home: '/'
    },
    fullPathRedirect: true
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
    lang: {
      locales: {ru},
      current: 'ru',
    },
    theme: {
      dark: false,
      default: 'light',
      disable: false,
      options: {
        // cspNonce: undefined,
        customProperties: true,
        // minifyTheme: undefined,
        // themeCache: true,
      },
      themes: {
        dark: {
          background: '#333333',
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        },
        light: {
          background: '#e0e0e0',
          primary: '#1d428a',
        },
      }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {}
}
