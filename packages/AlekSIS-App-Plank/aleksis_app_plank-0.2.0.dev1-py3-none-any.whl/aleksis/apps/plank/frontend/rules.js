export default {
  name: [
    (v) => !!v || "Name is required",
    (v) => v.length <= 255 || "Name must be less than 255 characters",
  ],
  inventory: [(v) => !!v || "Inventory is required"],
  category: [(v) => !!v || "Category is required"],
  manufacturer: [],
  partNumber: [],
  serialNumber: [],
  itemType: [],
  location: [],
  person: [(v) => !!v || "Person is required"],
  checkOutCondition: [],
  checkInUntil: [
    (v) => !v || new Date(v) >= new Date() || "Date has to be after today",
  ],
  item: [],
};
