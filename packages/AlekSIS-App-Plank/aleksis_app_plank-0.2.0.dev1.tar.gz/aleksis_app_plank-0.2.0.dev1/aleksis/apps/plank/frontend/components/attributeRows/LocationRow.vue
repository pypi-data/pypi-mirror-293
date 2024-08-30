<template>
  <attribute-row
    :icon="defaultIcons.location"
    :label="$t('plank.location.title')"
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
  name: "LocationRow",
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
