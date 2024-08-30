<template>
  <attribute-row
    :icon="defaultIcons.location"
    :label="$t('plank.location.parents')"
  >
    <v-breadcrumbs
      v-if="data"
      :items="
        data.breadcrumbs.slice(0, -1).map((t) => {
          return { text: t };
        })
      "
      class="pa-0"
    ></v-breadcrumbs>

    <span v-else>–</span>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "ParentLocationsRow",
  components: { AttributeRow },
  props: {
    data: {
      type: Object,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
