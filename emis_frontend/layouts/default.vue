<template>
  <v-app dark>
    <v-navigation-drawer
      v-if="logging"
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      class="menu-background"
      :width="220"
      fixed
      app
      dark
    >
      <v-btn
        block
        @click.stop="miniVariant = !miniVariant"
      >
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <emis-logo :size=80 :center=true></emis-logo>
      <v-list>
        <div v-for="(item, i) in items" :key="i">
          <v-list-item
            v-if="!item.subLinks"
            :key="i"
            :to="item.to"
            router
            exact
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"/>
            </v-list-item-content>
          </v-list-item>

          <v-list-group
            v-else
            :key="i"
            class="group-list"
          >
            <template #activator>
              <v-list-item
              :to="item.to"
              >
                <v-list-item-action>
                  <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title v-text="item.title"/>
                </v-list-item-content>
              </v-list-item>
            </template>

            <v-list-item
              v-for="sublink in item.subLinks"
              :key="sublink.title"
              :to="sublink.to"
              class="sublink-list-item"
            >
              <v-list-item-action>
                <v-icon>{{ sublink.icon }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title v-text="sublink.title"/>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
        </div>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
      v-if="logging"
      :clipped-left="clipped"
      fixed
      app
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
      {{ title }}
      <v-spacer/>
      <div class="username">
        {{ $auth.user.last_name }} {{ $auth.user.first_name }}
      </div>
      <v-menu offset-y>
        <template #activator="{ on, attrs }">
          <v-btn
            color="primary"
            fab
            small
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="(item, i) in itemsMenu"
                       :key="i"
                       :to="item.to"
                       router
                       exact
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title v-text="item.title"/>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-btn outlined block @click="logout">Выход</v-btn>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-main>
      <v-container :fluid="true">
        <Nuxt/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import {mapMutations} from 'vuex'

export default {
  data() {
    return {
      clipped: false,
      drawer: true,
      fixed: true,
      itemsMenu: [
        {
          icon: 'mdi-desktop-mac-dashboard',
          title: 'Профиль пользователя',
          to: '/profile'
        },
      ],
      items: [
        {
          icon: 'mdi-monitor',
          title: 'Рабочий стол',
          to: '/'
        },
        {
          icon: 'mdi-office-building-cog-outline',
          title: 'Обьекты',
          to: '/entity'
        },
        {
          icon: 'mdi-badge-account-horizontal-outline',
          title: 'Персонал',
          to: '/personnel',
          subLinks: [
            {
              icon: 'mdi-content-paste',
              to: '/report_card',
              title: 'ГПД',
            }
          ]
        },
        {
          icon: 'mdi-diving-scuba-tank-multiple',
          title: 'Оборудование',
          to: '/equipment'
        },
        {
          icon: 'mdi-tune',
          title: 'Настройки',
          to: '/settings'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
    }
  },
  computed: {
    logging() {
      return this.$store.state.auth.loggedIn
    },
    title() {
      return this.$store.state.title
    }
  },
  watch: {
    title: {
      handler() {
        this.$store.commit('setTitle', this.title)
      },
      deep: true,
    },
  },
  methods: {
    ...mapMutations({
      setTitle: 'setTitle',
    }),
    async logout() {
      await this.$auth.logout()
      await this.$router.push('/login')
    }
  },
}
</script>
<style scoped>
.username{
  padding-right: 15px;
}
.group-list *{
  padding: 0 !important;
}
.sublink-list-item {
  padding: 0 40px !important;
}
</style>
