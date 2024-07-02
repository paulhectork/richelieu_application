import { fr } from '@formkit/i18n';
import { plugin, defaultConfig, createInput } from '@formkit/vue'

import FormSelect from "@components/FormSelect.vue";
import FormRadioTabs from "@components/FormRadioTabs.vue";
import FormRepeatableText from "@components/FormRepeatableText.vue";
import { textValidatorMessage
       , dateValidatorMessage
       , dateRangeValidatorMessage
       , textValidator
       , textArrayValidator
       , dateValidator
       , dateRangeValidator } from "@modules/formkitValidationRules";

const config = {
  locales: { fr },
  locale: 'fr',
  inputs: {
    formSelect         : createInput(FormSelect, { props: ["placeholder", "options"] }),
    formRadioTabs      : createInput(FormRadioTabs, { props: ["options", "value"] }),
    formRepeatableText : createInput(FormRepeatableText, { props: ["placeholder", "labelText"] })
  },
  rules: { textValidator
         , textArrayValidator
         , dateValidator
         , dateRangeValidator },
  messages: {
    fr: {
      validation: { textValidator      : textValidatorMessage
                  , textArrayValidator : textValidatorMessage
                  , dateValidator      : dateValidatorMessage
                  , dateRangeValidator : dateRangeValidatorMessage
      }
    }
  }
}

export default config