<template>
  <span>
    {{ item.name }}
    <span v-if="item.itemType || withBarcode">
      (<span v-if="item.itemType"
        >{{ item.itemType.name
        }}<!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text --></span
      ><span v-if="withBarcode && item.itemType">,</span>
      <span v-if="withBarcode">{{ item.barcode }}</span
      >)
    </span>
  </span>
</template>

<script>
export default {
  name: "ItemLabel",
  props: {
    item: {
      type: Object,
      required: true,
    },
    withBarcode: {
      type: Boolean,
      default: true,
    },
  },
};
</script>
