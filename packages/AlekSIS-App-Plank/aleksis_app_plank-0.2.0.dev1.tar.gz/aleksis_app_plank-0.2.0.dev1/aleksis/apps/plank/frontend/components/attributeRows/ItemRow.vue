<template>
  <attribute-row :icon="defaultIcons.item" :label="$t('plank.item.title')">
    <router-link
      v-if="data"
      :to="{ name: 'plank.item', params: { id: data.id } }"
    >
      {{ data.name }}
    </router-link>
    <container-chip v-if="data" class="ml-2" />
    <span v-if="!data">–</span>
  </attribute-row>
</template>

<script>
import AttributeRow from "./AttributeRow.vue";
import defaultIcons from "../../defaultIcons";
import ContainerChip from "../item/ContainerChip.vue";

export default {
  name: "ItemRow",
  components: { ContainerChip, AttributeRow },
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
