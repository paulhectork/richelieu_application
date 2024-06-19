import { fr } from '@formkit/i18n';
import { plugin, defaultConfig, createInput } from '@formkit/vue'

import FormSelect from "@components/FormSelect.vue";
import FormRadioTabs from "@components/FormRadioTabs.vue";

const config = {
  locales: { fr },
  locale: 'fr',
  inputs: {
    formSelect: createInput(FormSelect,
                                { props: [ "placeholder", "options" ] })
    ,
    formRadioTabs: createInput(FormRadioTabs,
                                { props: [ "options", "value" ] }),
  }
}

export default config