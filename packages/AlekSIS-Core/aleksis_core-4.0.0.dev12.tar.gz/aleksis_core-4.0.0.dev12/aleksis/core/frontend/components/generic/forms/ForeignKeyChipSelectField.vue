<script setup>
import ForeignKeyField from "./ForeignKeyField.vue";
</script>

<template>
  <foreign-key-field
    v-bind="{ ...$props, ...$attrs }"
    v-on="$listeners"
    rounded
    hide-details
    filled
    :height="height"
    class="chip-select-field"
  >
    <template #prepend-inner>
      <slot name="prepend-inner" />
    </template>
    <template #item="data">
      <slot name="item" v-bind="data" />
    </template>
    <template #selection="data">
      <slot name="selection" v-bind="data" />
    </template>
    <template #createComponent="{ attrs, on, createMode }">
      <slot
        name="selection"
        v-bind="{ ...attrs, createMode: createMode }"
        v-on="on"
      ></slot>
    </template>
  </foreign-key-field>
</template>

<script>
export default {
  name: "ForeignKeyChipSelectField",
  extends: ForeignKeyField,
  data() {
    return {
      heights: {
        "x-small": 16,
        small: 24,
        default: 32,
        large: 54,
        "x-large": 66,
      },
    };
  },
  props: {
    size: {
      type: String,
      required: false,
      default: "default",
    },
  },
  computed: {
    height() {
      return Object.hasOwn(this.heights, this.size)
        ? this.heights[this.size]
        : this.heights.default;
    },
    heightString() {
      return `${this.height}px`;
    },
    progressPadding() {
      return `${this.height / 2}px`;
    },
  },
};
</script>

<style lang="scss">
.chip-select-field {
  & .v-input__control > .v-input__slot {
    min-height: auto !important;
    padding: 0px 12px;
    cursor: pointer !important;
  }
  & .v-input__slot > .v-progress-linear {
    margin-left: v-bind(progressPadding);
    width: calc(100% - v-bind(heightString));
    top: calc(100% - 2px);
  }
  & .v-input__slot > .v-select__slot > .v-input__append-inner {
    margin-top: 0;
    align-self: center !important;
  }
  & .v-input__append-outer {
    margin-top: 0;
    margin-bottom: 0;
    align-self: center !important;
  }
}
</style>
