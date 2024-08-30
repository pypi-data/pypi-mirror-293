<template>
  <detail-page :id="$route.params.id" :gql-query="require('./detail.graphql')">
    <template #title="{ item }">{{ item.name }}</template>
    <template #content="{ item }">
      <v-row>
        <v-col cols="12" lg="6">
          <attributes-table>
            <category-row :data="item.category" />
            <manufacturer-row :data="item.manufacturer" />
            <part-number-row :data="item.partNumber" />
            <description-row :data="item.description" />
          </attributes-table>
        </v-col>
        <v-col cols="12" lg="6">
          <item-base-list
            :item-list="item.items"
            :hide-columns="['locationStatus', 'itemType.name']"
          >
            <template #title>
              <v-toolbar-title>
                <v-icon left>{{ defaultIcons.items }}</v-icon>
                {{ $t("plank.item.title_plural") }}
              </v-toolbar-title>
            </template>
          </item-base-list>
        </v-col>
      </v-row>
    </template>
  </detail-page>
</template>

<script>
import DetailPage from "../DetailPage.vue";
import defaultIcons from "../../defaultIcons";
import AttributesTable from "../AttributesTable.vue";
import CategoryRow from "../attributeRows/CategoryRow.vue";
import PartNumberRow from "../attributeRows/PartNumberRow.vue";
import ItemBaseList from "../item/ItemBaseList.vue";
import DescriptionRow from "../attributeRows/DescriptionRow.vue";
import ManufacturerRow from "../attributeRows/ManufacturerRow.vue";

export default {
  name: "ItemTypeDetail",
  components: {
    PartNumberRow,
    CategoryRow,
    DetailPage,
    AttributesTable,
    ItemBaseList,
    DescriptionRow,
    ManufacturerRow,
  },
  data() {
    return {
      defaultIcons: defaultIcons,
    };
  },
};
</script>
