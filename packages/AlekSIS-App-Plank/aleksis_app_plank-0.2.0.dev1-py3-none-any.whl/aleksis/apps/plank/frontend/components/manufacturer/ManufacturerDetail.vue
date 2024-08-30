<template>
  <detail-page :id="$route.params.id" :gql-query="require('./detail.graphql')">
    <template #title="{ item }">{{ item.name }}</template>
    <template #content="{ item }">
      <v-row>
        <v-col cols="12" lg="6">
          <attributes-table>
            <notes-row :data="item.notes" />
          </attributes-table>
        </v-col>
        <v-col cols="12" lg="6">
          <v-card>
            <v-card-title>{{
              $t("plank.item_type.title_plural")
            }}</v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </detail-page>
</template>

<script>
import DetailPage from "../DetailPage.vue";
import defaultIcons from "../../defaultIcons";
import AttributesTable from "../AttributesTable.vue";
import NotesRow from "../attributeRows/NotesRow.vue";

export default {
  name: "ManufacturerDetail",
  components: { NotesRow, DetailPage, AttributesTable },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
