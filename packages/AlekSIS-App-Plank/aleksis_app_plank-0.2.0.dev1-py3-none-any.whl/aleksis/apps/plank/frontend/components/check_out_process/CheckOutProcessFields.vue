<template>
  <div>
    <check-in-until-input v-model="innerValue.checkInUntil" />
    <check-out-condition-input
      :check-out-conditions="formData.checkOutConditions"
      v-model="innerValue.condition"
    />
  </div>
</template>

<script>
import CheckOutConditionInput from "../inputs/CheckOutConditionInput.vue";
import CheckInUntilInput from "../inputs/CheckInUntilInput.vue";

export default {
  name: "CheckOutProcessFields",
  components: { CheckInUntilInput, CheckOutConditionInput },
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
