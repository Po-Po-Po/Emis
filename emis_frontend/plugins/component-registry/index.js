import Vue from 'vue'
import EquipmentView from "~/pages/equipment/_id";
import PersonnelView from "~/pages/personnel/_id";
import TextareaField from "~/components/field/TextareaField";

const components = { EquipmentView, PersonnelView, TextareaField}

Object.entries(components).forEach(([name, component]) => {
    Vue.component(name, component)
})
