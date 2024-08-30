export default {
  meta: {
    inMenu: true,
    titleKey: "plank.menu_title",
    icon: "mdi-warehouse",
    permission: "plank.view_menu_rule",
  },
  children: [
    {
      path: "inventories/",
      component: () => import("./components/inventory/InventoryList.vue"),
      name: "plank.inventories",
      meta: {
        inMenu: true,
        titleKey: "plank.inventory.menu_title",
        toolbarTitle: "plank.inventory.title_plural",
        icon: "mdi-folder-home-outline",
        iconActive: "mdi-folder-home",
        permission: "plank.view_inventories_rule",
      },
    },
    {
      path: "inventories/:id(\\d+)/",
      component: () => import("./components/inventory/InventoryDetail.vue"),
      name: "plank.inventory",
    },
    {
      path: "categories/",
      component: () => import("./components/category/CategoryList.vue"),
      name: "plank.categories",
      meta: {
        inMenu: true,
        titleKey: "plank.category.menu_title",
        toolbarTitle: "plank.category.title_plural",

        icon: "mdi-label-multiple-outline",
        iconActive: "mdi-label-multiple",
        permission: "plank.view_categories_rule",
      },
    },
    {
      path: "manufacturers/",
      component: () => import("./components/manufacturer/ManufacturerList.vue"),
      name: "plank.manufacturers",
      meta: {
        inMenu: true,
        titleKey: "plank.manufacturer.menu_title",
        toolbarTitle: "plank.manufacturer.title_plural",
        icon: "mdi-factory",
        permission: "plank.view_manufacturers_rule",
      },
    },
    {
      path: "manufacturers/:id(\\d+)/",
      component: () =>
        import("./components/manufacturer/ManufacturerDetail.vue"),
      name: "plank.manufacturer",
    },
    {
      path: "locations/",
      component: () => import("./components/location/LocationList.vue"),
      name: "plank.locations",
      meta: {
        inMenu: true,
        titleKey: "plank.location.menu_title",
        toolbarTitle: "plank.location.title_plural",
        icon: "mdi-map-marker-multiple-outline",
        iconActive: "mdi-map-marker-multiple",
        permission: "plank.view_locations_rule",
      },
    },
    {
      path: "locations/:id(\\d+)/",
      component: () => import("./components/location/LocationDetail.vue"),
      name: "plank.location",
    },
    {
      path: "locations/:id(\\d+)/completeness/",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "plank.locationCompleteness",
    },
    {
      path: "item_types/",
      component: () => import("./components/item_type/ItemTypeList.vue"),
      name: "plank.itemTypes",
      meta: {
        inMenu: true,
        titleKey: "plank.item_type.menu_title",
        toolbarTitle: "plank.item_type.title_plural",
        icon: "mdi-shape-outline",
        iconActive: "mdi-shape",
        permission: "plank.view_itemtypes_rule",
      },
    },
    {
      path: "item_types/:id(\\d+)/",
      component: () => import("./components/item_type/ItemTypeDetail.vue"),
      name: "plank.itemType",
    },
    {
      path: "items/",
      component: () => import("./components/item/PlankItemList.vue"),
      name: "plank.items",
      meta: {
        inMenu: true,
        titleKey: "plank.item.menu_title",
        toolbarTitle: "plank.item.title_plural",
        icon: "mdi-inbox-multiple-outline",
        iconActive: "mdi-inbox-multiple",
        permission: "plank.view_items_rule",
        fullWidth: true,
      },
    },
    {
      path: "items/:id(\\d+)/",
      component: () => import("./components/item/ItemDetail.vue"),
      name: "plank.item",
    },
    {
      path: "inventory/",
      component: () =>
        import("./components/inventory_process/InventoryForm.vue"),
      name: "plank.inventoryForm",
      meta: {
        inMenu: true,
        titleKey: "plank.item.inventory_process.menu_title",
        toolbarTitle: "plank.item.inventory_process.title",
        icon: "mdi-import",
        permission: "plank.create_item_rule",
      },
    },
    {
      path: "checks/out/",
      component: () => import("./components/check_out/CheckOutPage.vue"),
      name: "plank.checkOut",
      meta: {
        inMenu: true,
        titleKey: "plank.check_out.menu_title",
        toolbarTitle: "plank.check_out.title",
        icon: "mdi-cart-arrow-down",
        permission: "plank.check_out_rule",
      },
    },
    {
      path: "checks/:id(\\d+)/check-out-form.pdf",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "plank.checkOutForm",
    },
    {
      path: "checks/",
      component: () =>
        import("./components/check_out_process/CheckOutProcessList.vue"),
      name: "plank.checkOutProcesses",
      meta: {
        inMenu: true,
        titleKey: "plank.check_out_process.menu_title",
        toolbarTitle: "plank.check_out_process.title_plural",
        icon: "mdi-cart-outline",
        iconActive: "mdi-cart",
        permission: "plank.view_checkoutprocesses_rule",
      },
    },
    {
      path: "checks/:id(\\d+)/",
      component: () =>
        import("./components/check_out_process/CheckOutProcessDetail.vue"),
      name: "plank.checkOutProcess",
    },
    {
      path: "checks/:id(\\d+)/check-in-form.pdf",
      component: () => import("aleksis.core/components/LegacyBaseTemplate.vue"),
      name: "plank.checkInForm",
    },
    {
      path: "checks/in/",
      component: () => import("./components/check_in/CheckInPage.vue"),
      name: "plank.checkIn",
      meta: {
        inMenu: true,
        titleKey: "plank.check_in.menu_title",
        toolbarTitle: "plank.check_in.title",
        icon: "mdi-cart-arrow-up",
        permission: "plank.check_in_rule",
      },
    },
  ],
};
