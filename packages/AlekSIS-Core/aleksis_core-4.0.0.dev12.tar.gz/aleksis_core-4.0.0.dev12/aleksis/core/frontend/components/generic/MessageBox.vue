<script>
export default {
  name: "MessageBox",
  // Due to this component being a wrapper to a v-alert, all props of this can be used (and overridden).
  extends: "v-alert",
};
</script>

<template>
  <v-alert border="left" text v-bind="$attrs" v-on="$listeners">
    <slot />
  </v-alert>
</template>
