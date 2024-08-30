<template>
  <div>
    <manufacturer-input
      v-model="innerValue.manufacturer"
      :manufacturers="formData.manufacturers"
    />
    <category-input
      v-model="innerValue.category"
      :categories="formData.categories"
    />
    <name-input v-model="innerValue.name" />
    <part-number-input v-model="innerValue.partNumber" />
    <description-input v-model="innerValue.description" />
  </div>
</template>

<script>
import NameInput from "../inputs/NameInput.vue";
import PartNumberInput from "../inputs/PartNumberInput.vue";
import CategoryInput from "../inputs/CategoryInput.vue";
import ManufacturerInput from "../inputs/ManufacturerInput.vue";
import DescriptionInput from "../inputs/DescriptionInput.vue";

export default {
  name: "ItemTypeFields",
  components: {
    PartNumberInput,
    CategoryInput,
    ManufacturerInput,
    DescriptionInput,
    NameInput,
  },
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
