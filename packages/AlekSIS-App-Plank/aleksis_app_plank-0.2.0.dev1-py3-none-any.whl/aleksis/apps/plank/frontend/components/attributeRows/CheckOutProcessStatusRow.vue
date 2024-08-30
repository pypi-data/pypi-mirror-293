<template>
  <attribute-row :icon="defaultIcons.status" :label="$t('plank.labels.status')">
    <check-out-process-status
      :check-out-process="data"
    ></check-out-process-status>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";
import CheckOutProcessStatus from "../check_out_process/CheckOutProcessStatus.vue";

export default {
  name: "CheckOutProcessStatusRow",
  components: { CheckOutProcessStatus, AttributeRow },
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
