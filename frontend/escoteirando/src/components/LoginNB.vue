<template>
  <b-nav-form>
    <b-form-input size="sm" class="mr-sm-2" placeholder="usuário" v-model="user"></b-form-input>
    <b-form-input size="sm" class="mr-sm-2" placeholder="senha" v-model="senha" type="password"></b-form-input>
    <b-button size="sm" class="my-2 my-sm-0" type="submit" @click.prevent="signIn">Entrar</b-button>
  </b-nav-form>
</template>

<script>
export default {
  methods: {
    signIn() {
      alert("Executou signIn");
    }
  }
};
</script>

<style>
</style>