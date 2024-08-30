<template>
  <div>
    <form @submit.prevent="doSubmit">
      <v-text-field
        filled
        v-model="innerValue"
        :label="$t('plank.labels.id_barcode')"
        autofocus
        required
        prepend-icon="mdi-barcode"
        ref="scanInput"
        v-bind="$attrs"
      >
        <template #append-outer>
          <v-btn-toggle
            v-model="btnToggleScanner"
            rounded
            color="primary accent-3"
            style="margin-top: -14px"
          >
            <v-btn x-large value="scan">
              <v-icon v-if="openScanner">mdi-chevron-up</v-icon>
              <v-icon v-else>mdi-barcode-scan</v-icon>
            </v-btn>
          </v-btn-toggle>
        </template>
      </v-text-field>
      <v-expand-transition>
        <StreamBarcodeReader
          v-if="openScanner"
          @decode="onDecode"
          @loaded="onLoaded"
        ></StreamBarcodeReader>
      </v-expand-transition>
    </form>
  </div>
</template>

<script>
import rules from "../../rules";
import { StreamBarcodeReader } from "vue-barcode-reader";

export default {
  name: "ScanInput",
  components: { StreamBarcodeReader },
  props: {
    value: {
      type: String,
      required: true,
    },
  },
  computed: {
    openScanner() {
      return this.btnToggleScanner === "scan";
    },
  },
  methods: {
    onDecode(decoded) {
      this.innerValue = decoded;
      this.doSubmit();
    },
    onLoaded() {},
    doSubmit() {
      this.$emit("submit");
    },
    focus() {
      this.$refs.scanInput.focus();
    },
  },
  data() {
    return {
      rules: rules,
      innerValue: this.value,
      btnToggleScanner: false,
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
