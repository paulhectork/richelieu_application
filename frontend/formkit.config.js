import { fr } from '@formkit/i18n';
import { plugin, defaultConfig, createInput } from '@formkit/vue'

import FormSelectBasic from "@components/FormSelectBasic.vue";
import FormSelectTabs from "@components/FormSelectTabs.vue";

const config = {
  locales: { fr },
  locale: 'fr',
  inputs: {
    formSelectBasic: createInput(FormSelectBasic,
                                { props: [ "placeholder", "options" ] })
    //,
    //formSelectTabs: createInput(FormSelectTabs,
    //                            { props: [ "options" ] }),
  }
}

export default config