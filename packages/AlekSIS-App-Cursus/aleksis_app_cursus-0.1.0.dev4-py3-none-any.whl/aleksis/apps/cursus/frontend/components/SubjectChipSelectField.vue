<script setup>
import SubjectChip from "./SubjectChip.vue";
</script>

<template>
  <chip-select-field
    v-bind="{ ...$props, ...$attrs }"
    v-on="$listeners"
    :background-color="value?.colourBg"
    :color="value?.colourFg"
    return-object
    item-text="name"
    item-value="id"
  >
    <template #item="{ item }">
      <subject-chip :subject="item" :style="{ cursor: 'pointer' }" />
    </template>
  </chip-select-field>
</template>

<script>
import ChipSelectField from "aleksis.core/components/generic/forms/ChipSelectField.vue";

export default {
  name: "SubjectChipSelectField",
  extends: ChipSelectField,
  components: { ChipSelectField },
};
</script>

<style scoped></style>
