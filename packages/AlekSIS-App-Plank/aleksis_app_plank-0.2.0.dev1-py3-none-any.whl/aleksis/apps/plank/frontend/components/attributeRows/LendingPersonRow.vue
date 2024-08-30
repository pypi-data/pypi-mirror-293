<template>
  <attribute-row
    :icon="defaultIcons.person"
    :label="$t('plank.labels.lending_person')"
  >
    {{ data.fullName }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "LendingPersonRow",
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
