<template>
  <attribute-row
    :icon="defaultIcons.category"
    :label="$t('plank.category.title')"
  >
    {{ data.name }}
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "CategoryRow",
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
