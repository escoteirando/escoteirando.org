<template>
  <div>
      <b-dropdown-item v-b-modal.login_mappa href="#">Login MAPPA</b-dropdown-item>    
    <b-modal
      id="login_mappa"
      ref="modal"
      title="Login MAPPA"
      @show="resetModal"
      @hidden="resetModal"
      @ok="handleOk"
    >
      <form ref="form" @submit.stop.prevent="handleSubmit">
        <b-form-group
          :state="usuarioState"
          label="Usuário MAPPA"
          label-for="usuario-input"
          invalid-feedback="Usuário é requerido"
        >
          <b-form-input id="usuario-input" v-model="usuario" :state="usuarioState" required></b-form-input>
        </b-form-group>
        <b-form-group
          :state="senhaState"
          label="Senha MAPPA"
          title="Sua senha não será armazenada neste sistema"
          label-for="senha-input"
          invalid-feedback="Senha é requerida"
        >
          <b-form-input
            id="senha-input"
            type="password"
            v-model="senha"
            :state="senhaState"
            required
          ></b-form-input>
          <p id="popover-target-mappa">Por quê preciso informar isso?</p>
          <b-popover target="popover-target-mappa" triggers="hover" placement="top">
            <template v-slot:title>Credenciais mAPPa</template>
            Suas credenciais serão utilizadas para comunicar diretamente com os servidores do aplicativo mAPPa e não serão registradas neste sistema!
            Este acesso é necessário para que você possa visualizar seu grupo escoteiro, sua seção e seus jovens.
          </b-popover>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import mappa from "../shared/mappa.js";
export default {
  data() {
    return {
      usuario: "",
      usuarioState: null,
      senha: "",
      senhaState: null,
      submittedNames: []
    };
  },
  methods: {
    checkFormValidity() {
      const valid = this.$refs.form.checkValidity();
      this.usuarioState = valid;
      return valid;
    },
    resetModal() {
      this.usuario = "";
      this.usuarioState = null;
      this.senha = "";
      this.senhaState = null;
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault();
      // Trigger submit handler
      this.handleSubmit();
    },
    handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return;
      }
      // Push the name to submitted names
      if (mappa.login(this.usuario, this.senha)) {
        alert("Login MAPPA OK");
      }
      // Hide the modal manually
      this.$nextTick(() => {
        this.$bvModal.hide("modal-prevent-closing");
      });
    }
  }
};
</script>

<style>
</style>