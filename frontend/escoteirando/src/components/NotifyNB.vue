<template>
  <b-nav-item-dropdown right v-if="notifications.length>0">
    <template slot="button-content">
      <b-icon-bell-fill variant="warning"></b-icon-bell-fill>
      <b-badge variant="light">{{ ntf_count(notifications.length) }}</b-badge>
    </template>
    <b-dropdown-item
      v-for="notification in notifications"
      :key="notification"
      :data-id="notification.id"
      @click="notification_click(notification.id)"
    >{{ notification.msg}}</b-dropdown-item>
  </b-nav-item-dropdown>
  <b-nav-item v-else>
    <b-icon-bell></b-icon-bell>
  </b-nav-item>
</template>

<script>
export default {
  data() {
    return {
      notifications: []
    };
  },
  methods: {
    ntf_count(c) {
      if (c < 10) {
        return c;
      }
      return "9+";
    },
    notification_click(e) {
      // TODO: Usar axios para notificar o backend de que a notificação foi clicada

      this.notifications = this.notifications.filter(x => x.id != e);
    }
  },
  mounted() {
    // Usar axios para obter as notificações do usuário
    this.notifications = [
      { msg: "Notificação 1", id: 1 },
      { msg: "Notificação 2", id: 2 },
      { msg: "Notificação 3", id: 3 },
      { msg: "Notificação 4", id: 4 },
      { msg: "Notificação 5", id: 5 },
      { msg: "Notificação 6", id: 6 },
      { msg: "Notificação 7", id: 7 },
      { msg: "Notificação 8", id: 8 },
      { msg: "Notificação 9", id: 9 },
      { msg: "Notificação 10", id: 10 },
      { msg: "Notificação 11", id: 11 },
      { msg: "Notificação 12", id: 12 },
      { msg: "Notificação 13", id: 13 },
      { msg: "Notificação 14", id: 14 }
    ];
  }
};
</script>

<style>
</style>