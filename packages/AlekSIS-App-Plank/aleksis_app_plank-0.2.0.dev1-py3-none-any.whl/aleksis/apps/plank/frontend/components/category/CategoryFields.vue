<template>
  <div>
    <name-input v-model="innerValue.name" />
    <notes-input v-model="innerValue.notes" />
    <icon-input v-model="innerValue.icon" :icons="formData.icons" />
    <color-input v-model="innerValue.colour" />
  </div>
</template>

<script>
import NotesInput from "../inputs/NotesInput.vue";
import IconInput from "../inputs/IconInput.vue";
import NameInput from "../inputs/NameInput.vue";
import ColorInput from "../inputs/ColorInput.vue";

export default {
  name: "CategoryFields",
  components: { NotesInput, IconInput, NameInput, ColorInput },
  props: {
    value: {
      type: String,
      required: true,
    },
    formData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      innerValue: this.value,
    };
  },
  watch: {
    value(val) {
      this.innerValue = val;
    },
    innerValue(val) {
      this.$emit("input", val);
    },
  },
};
</script>

<style scoped></style>
