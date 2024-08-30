<template>
  <attribute-row
    :icon="defaultIcons.containedIn"
    :label="$t('plank.labels.is_location')"
  >
    <router-link
      v-if="data"
      :to="{ name: 'plank.location', params: { id: data.id } }"
    >
      {{ data.name }}
    </router-link>
    <span v-else>–</span>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";

export default {
  name: "IsLocationRow",
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
