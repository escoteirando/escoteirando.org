<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-container>
        <b-navbar-brand href="#">
          <b-img class="logo" src="/flor_de_lis_sombra.svg"></b-img>&nbsp;Escoteirando
        </b-navbar-brand>
        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <NotifyNB right></NotifyNB>
            <b-nav-item-dropdown right v-if="this.isLogged">
              <template slot="button-content">
                <b-icon-person-fill></b-icon-person-fill>
              </template>
              <MappaLogin v-if="this.mappaCreds"></MappaLogin>
              <b-dropdown-item href="#">Perfil</b-dropdown-item>
              <b-dropdown-item href="#">Sair</b-dropdown-item>
            </b-nav-item-dropdown>
            <LoginNB v-else></LoginNB>
          </b-navbar-nav>
        </b-collapse>
      </b-container>
    </b-navbar>
  </div>
</template>
<script>
import LoginNB from "./LoginNB.vue";
import NotifyNB from "./NotifyNB.vue";
import MappaLogin from "./MappaLogin.vue";
import mappa from "../shared/mappa";
export default {
  data() {
    return {
      meal: ""
    };
  },
  methods: {
    getMeal() {
      alert("Entrou?");
    }
  },
  computed: {
    isLogged() {
      return true;
    },
    mappaCreds() {
      return !mappa.credentials_ok();
    }
  },
  components: {
    LoginNB,
    NotifyNB,
    MappaLogin
  }
};
</script>
<style scoped>
img.logo {
  height: 2em;
}
</style>