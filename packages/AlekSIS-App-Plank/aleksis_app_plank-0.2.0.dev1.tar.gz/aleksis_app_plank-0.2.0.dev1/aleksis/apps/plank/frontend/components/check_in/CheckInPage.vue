<template>
  <v-row>
    <v-col cols="12" lg="6">
      <v-card>
        <v-card-title>{{ $t("plank.check_in.process.title") }}</v-card-title>
        <v-card-text>
          <ApolloMutation
            :mutation="require('./checkIn.graphql')"
            :variables="{ idOrBarcode }"
            @done="checkedIn"
          >
            <template #default="{ mutate, loading, error }">
              <scan-input
                v-model="idOrBarcode"
                :hint="$t('plank.check_in.process.scan_hint')"
                ref="scanInput"
                persistent-hint
                @submit="mutate"
              />
              <v-btn color="primary" @click="mutate" class="mb-4">
                {{ $t("plank.check_in.process.check_in") }}
              </v-btn>
            </template>
          </ApolloMutation>
        </v-card-text>
      </v-card>
    </v-col>

    <v-col cols="12" lg="6">
      <v-card v-if="checkedOutItems.length > 0">
        <v-card-title>
          <v-icon left color="success">mdi-check-circle-outline</v-icon>
          {{ $t("plank.check_in.process.checked_in_successfully") }}
        </v-card-title>
        <v-card-text>
          <p
            class="text-body-1"
            v-for="checkedOutItem in checkedOutItems"
            :key="checkedOutItem.id"
          >
            {{ checkedOutItem.item.name }} (#{{ checkedOutItem.item.id }})
          </p>
        </v-card-text>
        <v-card-actions>
          <v-btn
            color="primary"
            :href="checkedOutItems[0].process.checkInForm"
            target="_blank"
          >
            <v-icon left>mdi-file-pdf-box</v-icon>
            {{ $t("plank.check_in.process.download_form") }}
          </v-btn>
          <v-btn color="primary">
            {{ $t("plank.check_in.process.show_process") }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
    <v-snackbar :color="snackbarColor" v-model="snackbar">
      <v-icon left v-if="snackbarColor === 'success'">
        mdi-check-circle-outline
      </v-icon>
      <v-icon left v-else> mdi-alert-circle-outline </v-icon>
      <span v-if="snackbarStatus === 'not_found'">
        {{ $t("plank.check_in.process.messages.not_found") }}
      </span>
      <span v-else-if="snackbarStatus === 'not_checked_out'">
        {{ $t("plank.check_in.process.messages.not_checked_out") }}
      </span>
      <span v-else-if="snackbarStatus === 'checked_in'">
        {{ $t("plank.check_in.process.messages.checked_in") }}
      </span>
      <v-btn text @click="snackbar = false">
        {{ $t("plank.actions.close") }}
      </v-btn>
    </v-snackbar>
  </v-row>
</template>

<script>
import ScanInput from "../inputs/ScanInput.vue";

export default {
  name: "CheckInPage",
  components: {
    ScanInput,
  },
  data() {
    return {
      idOrBarcode: "",
      snackbar: false,
      snackbarStatus: "",
      checkedOutItems: [],
    };
  },
  computed: {
    snackbarColor() {
      return this.snackbarStatus === "checked_in" ? "success" : "error";
    },
  },
  methods: {
    focusScanInput() {
      this.$refs.scanInput.focus();
    },
    clearScanInput() {
      this.idOrBarcode = "";
      this.focusScanInput();
    },
    checkedIn({ data }) {
      const { status, checkedOutItems } = data.checkIn;
      this.snackbarStatus = status;
      this.snackbar = true;
      if (checkedOutItems?.length > 0) {
        this.checkedOutItems = checkedOutItems;
      }
    },
  },
};
</script>
