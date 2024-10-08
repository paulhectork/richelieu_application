import { fr } from '@formkit/i18n';
import { plugin, defaultConfig, createInput } from '@formkit/vue'

import FormKitSlider from "@components/FormKitSlider.vue";
import FormKitSelect from "@components/FormKitSelect.vue";
import FormKitRadioTabs from "@components/FormKitRadioTabs.vue";
import FormKitBooleanOp from "@components/FormKitBooleanOp.vue";
import FormKitRepeatableText from "@components/FormKitRepeatableText.vue";
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
    fkSlider         : createInput(FormKitSlider, { props: ["minVal", "maxVal", "step", "number"] }),
    fkSelect         : createInput(FormKitSelect, { props: ["placeholder", "options", "multiple"] }),
    fkRadioTabs      : createInput(FormKitRadioTabs, { props: ["options", "value"] }),
    fkBooleanOp      : createInput(FormKitBooleanOp, { props: ["id"] }),
    fkRepeatableText : createInput(FormKitRepeatableText, { props: ["placeholder", "labelText"] }),
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