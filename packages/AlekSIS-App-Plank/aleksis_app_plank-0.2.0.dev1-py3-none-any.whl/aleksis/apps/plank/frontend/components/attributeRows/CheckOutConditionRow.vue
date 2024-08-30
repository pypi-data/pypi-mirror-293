<template>
  <attribute-row
    :icon="defaultIcons.checkOutCondition"
    :label="$t('plank.check_out_condition.title')"
  >
    {{ data ? data.text : "–" }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "CheckOutConditionRow",
  components: { AttributeRow },
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
