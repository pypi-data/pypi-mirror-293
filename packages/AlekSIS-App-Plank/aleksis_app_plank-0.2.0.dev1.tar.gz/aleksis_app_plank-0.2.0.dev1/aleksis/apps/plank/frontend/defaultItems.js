export default {
  inventory: { name: "", checkOutCreateGroup: null, checkOutGroups: [] },
  category: {
    name: "",
    notes: "",
    colour: "#00000000",
    icon: "",
  },
  manufacturer: { name: "", notes: "" },
  location: { name: "", notes: "", parent: null, item: null },
  itemType: {
    name: "",
    description: "",
    partNumber: "",
    image: "",
    manufacturer: null,
    category: null,
  },
  item: {
    barcode: "",
    name: "",
    notes: "",
    inventory: null,
    category: null,
    itemType: null,
    location: null,
    serialNumber: "",
  },
  checkOutProcess: {
    checkInUntil: null,
    condition: null,
  },
};
